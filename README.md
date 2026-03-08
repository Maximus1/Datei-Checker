# Datei Checker - Dateisignatur & Wiederherstellung

**Datei Checker** ist ein leistungsstarkes Tool zur Dateiwiederherstellung und -restaurierung, das Dateitypen automatisch anhand von Binärsignaturen (Magic Bytes) erkennt und fehlende oder falsche Dateierweiterungen wiederherstellt.

## Funktionen

- **Automatische Dateityperkennung**: Identifiziert Dateien basierend auf ihren internen Binärsignaturen (Magic Bytes).
- **Dateiwiederherstellung**: Stellt Dateierweiterungen und Originalnamen basierend auf den erkannten Dateitypen wieder her.
- **GUI- & CLI-Modi**:
    - **GUI**: Eine benutzerfreundliche Oberfläche mit Tkinter für einfache Ordnerauswahl und Fortschrittskontrolle.
    - **CLI**: Eine Befehlszeilenschnittstelle für schnelle und automatisierte Verarbeitung.
- **Vorschau-Modus (Dry-Run)**: Zeigt Änderungen an, bevor sie tatsächlich auf die Dateien angewendet werden.
- **Echtzeit-Fortschritt**: Visuelle Fortschrittsbalken und Statusaktualisierungen in GUI und CLI.

## Projektstruktur

- `core/`: Enthält die Kernlogik für Dateityperkennung, Verarbeitung und Umbenennung.
- `ui/`: Umfasst sowohl die grafische Benutzeroberfläche (Tkinter) als auch die Befehlszeilenschnittstelle.
- `tests/`: Automatisierte Tests zur Sicherstellung der Korrektheit und Zuverlässigkeit.
- `main.py`: Der zentrale Einstiegspunkt für die Anwendung.

## Installation

1. Stellen Sie sicher, dass Python installiert ist.
2. Klonen Sie dieses Repository.
3. Derzeit sind keine externen Abhängigkeiten erforderlich (verwendet Standardbibliothek und interne Module).

## Verwendung

### GUI-Modus (Standard)
Um die grafische Benutzeroberfläche zu starten:
```bash
python main.py
```

### CLI-Modus
Um die Anwendung in der Befehlszeile auszuführen:
```bash
python main.py <verzeichnis_pfad> -cli
```
*Alternativ kann das CLI-Skript direkt ausgeführt werden:*
```bash
python ui/cli.py <verzeichnis_pfad>
```

### Vorschau-Modus (Dry-Run)
Um zu sehen, welche Änderungen vorgenommen würden, ohne Dateien tatsächlich umzubenennen, fügen Sie das Flag `-d` oder `--dry-run` hinzu:
```bash
python main.py <verzeichnis_pfad> -cli --dry-run
```

## Funktionsweise

1. **Scannen**: Das Tool scannt das angegebene Verzeichnis nach Dateien.
2. **Erkennung**: Es liest die "Magic Bytes" (Header) jeder Datei, um das tatsächliche Format zu bestimmen.
3. **Verarbeitung**: Es vergleicht den erkannten Typ mit der aktuellen Erweiterung.
4. **Wiederherstellung**: Wenn die Erweiterung fehlt oder falsch ist, wird die Datei mit der entsprechenden Erweiterung umbenannt.

## Lizenz

Dieses Projekt lizenziert unter der MIT-Lizenz.
