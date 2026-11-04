# Einkaufsliste Geofence

[🇩🇪 Deutsch](README.md) · [🇬🇧 English](README.en.md)

Diese App für AppDaemon erstellt automatisch dynamische Sensoren für Geschäfte, die in der Home-Assistant-Einkaufsliste hinterlegt sind.

Die App erkennt Geschäfte anhand der Attribute der Einkaufslisten-Sensoren, ermittelt die GPS-Koordinaten über OpenStreetMap Nominatim und stellt diese als dynamische Sensoren in Home Assistant bereit.

Beispiele:
- `sensor.denner_1234`
- `sensor.coop_6900`
- `sensor.migros_6900`

Die Sensoren dienen als geografische Referenzpunkte für die automatische Zuordnung von Geschäften durch andere Integrationen oder die Einkaufsliste-Card.

## Features

- Automatische Erkennung von Geschäften anhand der Einkaufslisten-Sensoren
- Automatische Geocodierung der Geschäftsadressen
- Dynamische Erstellung eines Sensors pro Geschäft und Filiale
- GPS-Koordinaten als Sensorattribute
- Konfigurierbarer Geofence-Radius
- Lokaler Geocoding-Cache
- Automatische Aktualisierung bei Änderungen der Geschäftsdaten
- Unterstützung mehrerer Geschäfte und Filialen

**Wichtig:** Die App erstellt keine Binary-Sensoren und überwacht keine Smartphone-Tracker. Sie stellt ausschließlich die geografischen Informationen der Geschäfte bereit. Die Erkennung, ob sich ein Benutzer innerhalb eines Geofence befindet, übernimmt die verwendete Integration bzw. die Einkaufsliste-Card.

## Verwandte Projekte

- [Einkaufsliste](https://github.com/misterm2310/einkaufslisten-card) – Home-Assistant-Einkaufsliste mit Geschäftserkennung.
- [SwissGroceries AppDaemon](https://github.com/rudiratlos/swissgroceries-appdaemon/blob/main/README.md) – AppDaemon-Integration für Schweizer Supermarktaktionen.

## Installation über HACS

1. HACS öffnen.
2. Zu **Integrationen** bzw. **Benutzerdefinierte Repositories** wechseln.
3. Dieses Repository hinzufügen:

   `https://github.com/rudiratlos/einkaufsliste-geofence`

4. Als Kategorie **AppDaemon** auswählen.
5. Repository installieren.
6. Die AppDaemon-Konfiguration ergänzen.
7. AppDaemon neu starten.

**HACS-Kategorie:** AppDaemon

## Konfiguration

In der AppDaemon-Datei `apps.yaml`:

```yaml
einkaufsliste_geofence:
  module: einkaufsliste_geofence
  class: EinkaufslisteGeofence
  radius: 35
  update_interval: 60
```

### Konfigurationsoptionen

| Option | Standard | Beschreibung |
|---|---:|---|
| `radius` | `35` | Standardradius in Metern |
| `update_interval` | `60` | Aktualisierungsintervall in Sekunden |
| `sensor_prefix` | `sensor.einkaufsliste_` | Präfix der Einkaufslisten-Sensoren |
| `radius_<geschaeft>_<plz>` | `radius` | Individueller Radius pro Geschäft |

Beispiel mit individuellen Radien:

```yaml
einkaufsliste_geofence:
  module: einkaufsliste_geofence
  class: EinkaufslisteGeofence
  radius: 35
  radius_denner_1234: 50
  radius_coop_6900: 45
  update_interval: 60
```

## Voraussetzungen

- Home Assistant OS oder Home Assistant Supervised
- AppDaemon 4.5 oder neuer
- HACS
- Einkaufsliste-Sensoren mit den erforderlichen Geschäftsattributen
- Internetverbindung für OpenStreetMap Nominatim


## Dynamisch erzeugte Sensoren

Für jedes erkannte Geschäft wird automatisch ein Sensor erstellt.

Beispiel:

`sensor.denner_1234`

Der Sensor enthält folgende Attribute:

| Attribut | Beispiel |
|---|---|
| `friendly_name` | Denner 1234 |
| `latitude` | 45.0 |
| `longitude` | 8.0 |
| `radius` | 35 |
| `passive` | false |
| `icon` | mdi:cart-outline |
| `geschaeft` | Denner |
| `adresse` | Strasse nr., Postcode Ort |
| `plz` | 1234 |
| `ort` | Ort |
| `land` | Laendercode |
| `source_sensor` | sensor.einkaufsliste_denner |

Der Sensor stellt die geografischen Informationen der jeweiligen Filiale zur Verfügung.

### Geofence

Die App berechnet selbst keine Entfernungen und überwacht keine Personen.

Sie stellt lediglich die Koordinaten und den Radius der Filiale bereit.

Die Einkaufsliste-Card bzw. eine andere Integration kann diese Informationen verwenden, um festzustellen, ob sich ein Smartphone innerhalb des Geofence befindet.

Es werden keine personenbezogenen oder tracker-spezifischen Sensoren erstellt.

### Bestehende Home-Assistant-Zonen

Die App verändert keine bestehenden Home-Assistant-Zonen.

Eine zusätzliche `zone:`-Konfiguration in der `configuration.yaml` ist nicht erforderlich.

## Geocoding und Cache

Für die Ermittlung der GPS-Koordinaten wird OpenStreetMap Nominatim verwendet.

Erfolgreich ermittelte Koordinaten werden lokal gespeichert:

`/config/appdaemon/apps/einkaufsliste_geofence/geocode_cache.json`

Bereits geocodierte Adressen werden aus dem Cache geladen, um unnötige Anfragen zu vermeiden.

Nominatim-Anfragen werden auf maximal eine Anfrage pro Sekunde begrenzt.

## Fehlerbehebung

| Problem | Lösung |
|---|---|
| App kann nicht importiert werden | Modulpfad und Verzeichnisstruktur prüfen |
| Kein Geschäftssensor vorhanden | AppDaemon-Logs und Geschäftsattribute prüfen |
| Keine GPS-Koordinaten | Adresse und Internetverbindung prüfen |
| Falsche GPS-Koordinaten | Geschäftsadresse überprüfen |
| Individueller Radius wird nicht übernommen | Konfiguration `radius_<geschaeft>_<plz>` prüfen |
| Keine Geschäfte erkannt | Attribute `geschaeft`, `adresse` und `plz` prüfen |

## Updates

Updates werden über GitHub Releases bereitgestellt.

AppDaemon-App-Updates können über HACS installiert werden.

Nach einem Update AppDaemon bei Bedarf neu starten.

- [GitHub Repository](https://github.com/rudiratlos/einkaufsliste-geofence)
- [Releases](https://github.com/rudiratlos/einkaufsliste-geofence/releases)

## Lizenz

Dieses Projekt ist unabhängig und steht in keiner geschäftlichen Verbindung zu den genannten Supermarktketten.

MIT License.
