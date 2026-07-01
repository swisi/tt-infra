# UI Standard: CRUD Tabellen (Defacto)

Status: Accepted (Defacto)
Owner: Platform Team
Gilt fuer: tt-auth, tt-members, tt-agenda, tt-analytics, tt-attendance

## Ziel
Ein einheitliches Muster fuer tabellarische CRUD-Ansichten in allen Microservices.

## Referenz
Aktuelle Referenz-Implementierung:
- tt-auth/app/templates/master_data_positions.html

## Scope
Der Standard gilt fuer alle Verwaltungslisten mit tabellarischer Darstellung, insbesondere fuer Stammdaten, Benutzer-/Mitgliederlisten und Admin-Listen.

## Muss-Kriterien
1. Header-Actions rechts:
- Eintragszaehler
- Button Neu
- Button Speichern

2. Footer-Actions rechts:
- Button Neu
- Button Speichern

3. Create-Flow:
- Kein dauerhaft sichtbarer grosser Create-Block oberhalb der Tabelle
- Neu oeffnet ein einklappbares Inline-Panel direkt ueber der Tabelle
- Panel hat Abbrechen und Speichern

4. Read-Flow:
- Tabelle mit klaren Spaltenkoepfen
- Einheitliche Spalte Aktionen rechts

5. Update-Flow:
- Zeilenbasierte Bearbeitung (Inline-Edit-Zeile oder Modal)
- Abbrechen + Speichern

6. Delete-Flow:
- Delete-Action in Spalte Aktionen
- Bestaetigung vor Loeschen

7. Sortierung (wenn vorhanden):
- Keine redundante Textzeile "Sortierung X" in der Bezeichnung
- Nur kompakte Zahl vor dem Schluessel
- Speichern-Button fuer Sortier-Aenderungen nur aktiv, wenn Reihenfolge geaendert wurde

8. Mobile/Responsive:
- Header- und Footer-Actions bleiben erreichbar
- Tabellen duerfen horizontal scrollen

## Soll-Kriterien
- Gleiches Tailwind-Pattern fuer Buttons (Neu sekundar, Speichern primaer)
- Konsistente Icon-Nutzung (plus/check/pencil/trash)
- Einheitliche Abstaende und Badges fuer Schluessel + Sortierzahl

## Nicht-Ziele
- Ersetzen jeder Tabelle durch dieses Muster (z. B. Reporting- oder Pivot-Tabellen)
- Forcierte Echtzeit-Synchronisierung zwischen Services

## Rollout-Empfehlung
1. Referenz aus tt-auth als Basis uebernehmen.
2. Pro Service eine wiederverwendbare Include-Datei anlegen:
- app/templates/includes/crud_table_actions.html
- app/templates/includes/crud_table_shell.html
3. Bestehende Tabellen iterativ migrieren:
- tt-members: members.html, team_manager.html
- tt-agenda: admin_*.html Tabellen
- tt-analytics: Admin-/Run-Listen mit CRUD-Charakter
4. Definition of Done pro Migration:
- Muss-Kriterien erfuellt
- Dark Mode geprueft
- Mobile-Breakpoints geprueft
- Delete-Confirm vorhanden

## QA Checkliste
- Neu zeigt/verbirgt Panel korrekt
- Speichern fuer Sortierung ist initial deaktiviert
- Drag/Sort aktiviert Speichern
- Nach Speichern ist Zustand wieder deaktiviert
- Create/Update/Delete Endpunkte liefern erwartete Flash-Messages

## Governance
Aenderungen am Standard erfolgen per PR auf diese Datei mit kurzer Begruendung und Screenshot vorher/nachher.
