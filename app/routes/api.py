import re

from flask import Blueprint, current_app, jsonify, request

from ..extensions import db
from ..models import PositionGroup

bp = Blueprint('api', __name__, url_prefix='/api')

KEY_RE = re.compile(r'^[A-Z0-9_-]{1,40}$')


def _authorized():
    expected = current_app.config.get('INTERNAL_API_SECRET')
    provided = request.headers.get('X-TT-Internal-Secret')
    return bool(expected and provided and provided == expected)


def _require_auth():
    if not _authorized():
        return jsonify({'error': 'unauthorized'}), 401
    return None


def _parse_payload():
    payload = request.get_json(silent=True) or {}
    key = (payload.get('key') or '').strip().upper()
    label = (payload.get('label') or '').strip()
    sort_order = payload.get('sort_order', 0)
    is_active = payload.get('is_active', True)
    try:
        sort_order = int(sort_order)
    except (TypeError, ValueError):
        sort_order = 0
    return key, label, sort_order, bool(is_active)


@bp.route('/health')
def health():
    return {'status': 'ok'}, 200


@bp.route('/master-data/positions', methods=['GET', 'POST'])
def positions():
    unauthorized = _require_auth()
    if unauthorized:
        return unauthorized

    if request.method == 'GET':
        include_inactive = (request.args.get('include_inactive') or '').strip().lower() in {'1', 'true', 'yes', 'y'}
        query = PositionGroup.query
        if not include_inactive:
            query = query.filter(PositionGroup.is_active.is_(True))
        rows = query.order_by(PositionGroup.sort_order, PositionGroup.label, PositionGroup.key).all()
        return jsonify({'positions': [row.to_dict() for row in rows]}), 200

    key, label, sort_order, is_active = _parse_payload()
    if not key or not KEY_RE.match(key):
        return jsonify({'error': 'invalid_key'}), 400
    if not label:
        return jsonify({'error': 'label_required'}), 400
    if db.session.get(PositionGroup, key):
        return jsonify({'error': 'already_exists'}), 409

    row = PositionGroup(key=key, label=label, sort_order=sort_order, is_active=is_active)
    db.session.add(row)
    db.session.commit()
    return jsonify({'status': 'created', 'position': row.to_dict()}), 201


@bp.route('/master-data/positions/<string:key>', methods=['GET', 'PUT', 'DELETE'])
def position_detail(key):
    unauthorized = _require_auth()
    if unauthorized:
        return unauthorized

    normalized_key = (key or '').strip().upper()
    row = db.session.get(PositionGroup, normalized_key)
    if not row:
        return jsonify({'error': 'not_found'}), 404

    if request.method == 'GET':
        return jsonify({'position': row.to_dict()}), 200

    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()
        return jsonify({'status': 'deleted', 'key': normalized_key}), 200

    payload_key, label, sort_order, is_active = _parse_payload()
    if payload_key and payload_key != normalized_key:
        return jsonify({'error': 'key_immutable'}), 400
    if not label:
        return jsonify({'error': 'label_required'}), 400

    row.label = label
    row.sort_order = sort_order
    row.is_active = is_active
    db.session.commit()
    return jsonify({'status': 'updated', 'position': row.to_dict()}), 200
