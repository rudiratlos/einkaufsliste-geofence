# Shopping List Geofence

[🇩🇪 Deutsch](README.md) · [🇬🇧 English](README.en.md)

**!! do not use it for einkaufsliste, it's already in included since Version v2.76.26 !!**

This AppDaemon app automatically creates dynamic sensors for stores configured in your Home Assistant shopping list.

The app discovers stores using shopping list sensor attributes, geocodes their addresses via OpenStreetMap Nominatim and exposes their GPS coordinates as dynamic Home Assistant sensors.

Examples:
- `sensor.einkaufsliste_zone_denner_1234`
- `sensor.einkaufsliste_zone_coop_6900`
- `sensor.einkaufsliste_zone_migros_6900`

These sensors provide geographic reference points for automatic store matching by other integrations or the Shopping List Card.

## Features

- Automatic store discovery from shopping list sensors
- Automatic geocoding of store addresses
- Dynamic sensor creation for each store and branch
- GPS coordinates exposed as sensor attributes
- Configurable geofence radius
- Local geocoding cache
- Automatic updates when store information changes
- Support for multiple stores and branches

**Important:** This app does not create binary sensors or monitor smartphone trackers. It only provides geographic information about stores. Determining whether a user is within a geofence is handled by the consuming integration or the Shopping List Card.

## Related projects

- [Shopping List](https://github.com/misterm2310/einkaufslisten-card) – Home Assistant shopping list with store detection.
- [SwissGroceries AppDaemon](https://github.com/rudiratlos/swissgroceries-appdaemon/blob/main/README.md) – AppDaemon integration for Swiss supermarket promotions.

## Installation via HACS

1. Open HACS.
2. Navigate to **Integrations** or **Custom repositories**.
3. Add this repository:

   `https://github.com/rudiratlos/einkaufsliste-geofence`

4. Select **AppDaemon** as the category.
5. Install the repository.
6. Add the AppDaemon configuration.
7. Restart AppDaemon.

**HACS category:** AppDaemon

## Configuration

Add the following to AppDaemon's `apps.yaml`:

```yaml
einkaufsliste_geofence:
  module: einkaufsliste_geofence
  class: EinkaufslisteGeofence
  radius: 35
  update_interval: 60
```

### Configuration options

| Option | Default | Description |
|---|---:|---|
| `radius` | `35` | Default geofence radius in meters |
| `update_interval` | `60` | Update interval in seconds |
| `sensor_prefix` | `sensor.einkaufsliste_zone_` | Shopping list sensor prefix |
| `radius_[store]_[zip]` | `radius` | Individual radius per store |

Example with individual radii:

```yaml
einkaufsliste_geofence:
  module: einkaufsliste_geofence
  class: EinkaufslisteGeofence
  radius: 35
  radius_denner_1234: 50
  radius_coop_6900: 45
  update_interval: 60
```

## Requirements

- Home Assistant OS or Home Assistant Supervised
- AppDaemon 4.5 or newer
- HACS
- Shopping list sensors with the required store attributes
- Internet access for OpenStreetMap Nominatim geocoding

Shopping list sensors must provide the following attributes:

| Attribute | Example |
|---|---|
| `geschaeft` | Denner |
| `adresse` | Address |
| `plz` | 1234 |
| `ort` | city |
| `land` | countrycode |

## Dynamically generated sensors

For every detected store a sensor is automatically created in the format sensor.einkaufsliste_zone_[store]_[plz]

Example:

`sensor.einkaufsliste_zone_denner_1234`

The sensor provides the following attributes:

| Attribute | Example |
|---|---|
| `friendly_name` | Denner 1234 |
| `latitude` | 45.0 |
| `longitude` | 8.0 |
| `radius` | 35 |
| `passive` | false |
| `icon` | mdi:cart-outline |
| `geschaeft` | Denner |
| `adresse` | address |
| `plz` | 1234 |
| `ort` | city |
| `land` | countrycode |
| `source_sensor` | sensor.einkaufsliste_denner |

The sensor provides geographic information for the corresponding store branch.

### Geofencing

The app does not calculate distances or monitor people itself.

It only provides the coordinates and radius of each store.

The Shopping List Card or another integration can use this information to determine whether a smartphone is within the geofence.

No person-specific or tracker-specific sensors are created.

### Existing Home Assistant zones

The app does not modify existing Home Assistant zones.

No additional `zone:` configuration in `configuration.yaml` is required.

## Geocoding and cache

OpenStreetMap Nominatim is used to retrieve GPS coordinates.

Successfully resolved coordinates are stored locally:

`/config/appdaemon/apps/einkaufsliste_geofence/geocode_cache.json`

Previously resolved addresses are loaded from the cache to avoid unnecessary requests.

Nominatim requests are limited to a maximum of one request per second.

## Troubleshooting

| Problem | Solution |
|---|---|
| App cannot be imported | Check module path and directory structure |
| No store sensor available | Check AppDaemon logs and store attributes |
| No GPS coordinates | Check address and internet connection |
| Incorrect GPS coordinates | Verify store address |
| Individual radius not applied | Check `radius_[store]_[zip]` configuration |
| No stores detected | Check `geschaeft`, `adresse` and `plz` attributes |

## Updates

Updates are provided through GitHub Releases.

AppDaemon app updates can be installed through HACS.

Restart AppDaemon after an update if necessary.

- [GitHub Repository](https://github.com/rudiratlos/einkaufsliste-geofence)
- [Releases](https://github.com/rudiratlos/einkaufsliste-geofence/releases)

## License

This is an independent open-source project and is not affiliated with any of the mentioned supermarket chains.

MIT License.
