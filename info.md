# Einkaufsliste Geofence

AppDaemon-App für Home Assistant zur standortbasierten Erkennung von Geschäften aus der Einkaufsliste.

Die App erkennt Filialen anhand der Attribute der Einkaufssensoren und erstellt dynamische Binary-Sensoren, die anzeigen, ob sich ein überwachtes Smartphone innerhalb des konfigurierten Geofence-Radius befindet.

## Funktionen

- Automatische Erkennung von Geschäften anhand der Einkaufssensoren
- Geocoding der Geschäftsadressen zur Ermittlung der GPS-Koordinaten
- Dynamische Erstellung von Binary-Sensoren pro Filiale
- Individuell konfigurierbarer Geofence-Radius
- Überwachung ausgewählter Smartphone-Tracker
- Konfigurierbares Aktualisierungsintervall

## Voraussetzungen

- Home Assistant
- HACS
- AppDaemon Add-on
- Einkaufssensoren mit Geschäfts- und Adressattributen
- Smartphone-Tracker mit GPS-Koordinaten

## Installation

1. Repository über HACS als AppDaemon-Repository hinzufügen.
2. AppDaemon-App installieren.
3. Die Geofencing-App in `apps.yaml` konfigurieren.
4. AppDaemon neu starten.

## Repository

https://github.com/rudiratlos/einkaufsliste-geofence

## Lizenz

Siehe [LICENSE](LICENSE).

