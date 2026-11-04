# Einkaufsliste Geofence für Home Assistant

🇩🇪 Deutsch · [🇬🇧 English](README.en.md)

Erkennt automatisch, wenn du dich in der Nähe eines Geschäfts aus deiner Home-Assistant-Einkaufsliste befindest. Die App erstellt dafür dynamische Binary-Sensoren auf Basis der Geschäftsadressen und deiner Smartphone-Standorte.

## Installation

Es muss nichts von Hand kopiert werden. Repository über HACS hinzufügen und die App konfigurieren:

1. App über HACS: Voraussetzung ist, dass in HACS die Kategorie AppDaemon apps aktiviert ist (Einstellungen → Geräte & Dienste → HACS → Konfigurieren). Dann auf den Button HACS-Repository öffnen klicken und Herunterladen wählen. Ohne Button: HACS → ⋮ → Benutzerdefinierte Repositories → `https://github.com/rudiratlos/einkaufsliste-geofence`, Kategorie AppDaemon.
2. AppDaemon: Die App wird von HACS im AppDaemon-Verzeichnis installiert.
3. `apps.yaml` von AppDaemon ergänzen und AppDaemon neu starten

## Geofencing-Konfiguration

Die Geofencing-App wird über folgenden Eintrag in `apps.yaml` konfiguriert:

    einkaufsliste_geofence:
      module: einkaufsliste_geofence.einkaufsliste_geofence
      class: EinkaufslisteGeofence
      # Standardradius in Metern
      radius: 35
      # Aktualisierung alle 30 Sekunden
      update_interval: 30
      # Optional: nur bestimmte Smartphones
      # trackers:
      #   - device_tracker.iphone
      #   - device_tracker.android
      # Optional: individueller Radius pro Filiale
      # radius_<geschaeft>_<plz>: 50

Die App erkennt Geschäfte anhand der Attribute der Einkaufssensoren. Für die Standortbestimmung werden die Geschäftsadressen geocodiert.

Voraussetzungen: Home Assistant OS oder Supervised, AppDaemon Add-on (4.5), HACS, Einkaufssensoren mit Geschäfts- und Adressattributen sowie Smartphone-Tracker mit GPS-Koordinaten.

**Konfigurationsoptionen:**

Option | Standard | Bedeutung
--- | --- | ---
`radius` | `35` | Standardradius des Geofence in Metern
`update_interval` | `30` | Aktualisierungsintervall in Sekunden
`trackers` | automatisch | Liste der zu überwachenden Smartphone-Tracker
`radius_<geschaeft>_<plz>` | `radius` | Individueller Radius pro Filiale in Metern


## Erzeugte Binary-Sensoren

Für jede erkannte Filiale wird ein eigener Binary-Sensor erstellt.

Entity-ID:

    binary_sensor.einkaufsliste_bei_<geschaeft>_<plz>

Zustände:

- `on`: Mindestens ein überwachtes Smartphone befindet sich innerhalb des Geofence.
- `off`: Kein überwachtes Smartphone befindet sich innerhalb des Geofence.

Die Sensoren enthalten zusätzliche Attribute mit den Filial- und Standortinformationen sowie den ermittelten Entfernungen.

## Fehlersuche

Beobachtung | Lösung
--- | ---
App kann nicht importiert werden | Modulpfad und Verzeichnisstruktur prüfen
Kein Binary-Sensor vorhanden | AppDaemon-Log auf Fehler beim Start und bei der Filialerkennung prüfen
Keine GPS-Koordinaten | Geschäftsadresse und Geocoding prüfen
Sensor bleibt `off` | Smartphone-Tracker und dessen GPS-Koordinaten prüfen
Keine Filialen erkannt | Einkaufssensoren und Attribute `geschaeft`, `adresse`, `plz`, `ort` und `land` prüfen

Logs: `ha apps logs a0d7b954_appdaemon` (AppDaemon).

## Updates

Updates werden über GitHub Releases bereitgestellt.

AppDaemon-App: Updates über HACS installieren.

Nach einem Update gegebenenfalls AppDaemon neu starten.

Repository: https://github.com/rudiratlos/einkaufsliste-geofence

Release Notes: https://github.com/rudiratlos/einkaufsliste-geofence/releases

## Rechtliches

Diese App ist ein unabhängiges Open-Source-Projekt und steht in keiner Verbindung zu den genannten Handelsunternehmen.

Eigener Code: MIT License.
