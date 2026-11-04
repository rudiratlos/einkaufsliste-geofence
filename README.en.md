# Einkaufsliste Geofence for Home Assistant

[🇩🇪 Deutsch](README.md) · 🇬🇧 English

Automatically detects when you are near a store listed in your Home Assistant shopping list. The app creates dynamic binary sensors based on store addresses and smartphone locations.

## Installation

Nothing has to be copied by hand. Add the repository through HACS and configure the app:

1. App via HACS: Make sure the AppDaemon apps category is enabled in HACS (Settings → Devices & services → HACS → Configure). Then click Open in HACS and choose Download. Without the button: HACS → ⋮ → Custom repositories → `https://github.com/rudiratlos/einkaufsliste-geofence`, category AppDaemon.
2. AppDaemon: HACS installs the app in the AppDaemon directory.
3. Extend AppDaemon's `apps.yaml` and restart AppDaemon:

## Geofencing-Configuration

The Geofencing-App config entry in `apps.yaml`:

    einkaufsliste_geofence:
      module: einkaufsliste_geofence
      class: EinkaufslisteGeofence
      # Std. radius in Meter
      radius: 35
      update_interval: 30
      # Optional: for specific smartphones only
      # trackers:
      #   - device_tracker.iphone
      #   - device_tracker.android
      # Optional: individuell radius per shop
      # radius_<store>_<zip>: 50


The app detects stores using the attributes of the shopping list sensors. Store addresses are geocoded to determine their locations.

Requirements: Home Assistant OS or Supervised, AppDaemon add-on (4.5), HACS, shopping list sensors with store and address attributes, and smartphone trackers providing GPS coordinates.

## Options (all optional)

Option | Default | Meaning
--- | --- | ---
`radius` | `35` | Default geofence radius in meters
`update_interval` | `30` | Update interval in seconds
`trackers` | automatic | List of smartphone trackers to monitor
`radius_<store>_<zip>` | `radius` | Individual radius per store in meters


## Generated Binary Sensors

A separate binary sensor is created for each detected store.

Entity ID:

    binary_sensor.einkaufsliste_bei_<store>_<zip>

States:

- `on`: At least one monitored smartphone is within the geofence.
- `off`: No monitored smartphone is within the geofence.

The sensors include additional attributes containing store and location information as well as calculated distances.

## Troubleshooting

Observation | Fix
--- | ---
App cannot be imported | Check the module path and directory structure
No binary sensor available | Check AppDaemon logs for startup and store detection errors
No GPS coordinates | Check the store address and geocoding
Sensor remains `off` | Check the smartphone tracker and its GPS coordinates
No stores detected | Check shopping list sensors and the attributes `geschaeft`, `adresse`, `plz`, `ort` and `land`

Logs: `ha apps logs a0d7b954_appdaemon` (AppDaemon).

## Updates

Updates are provided through GitHub Releases.

AppDaemon app: Install updates through HACS.

Restart AppDaemon after an update if necessary.

Repository: https://github.com/rudiratlos/einkaufsliste-geofence

Release Notes: https://github.com/rudiratlos/einkaufsliste-geofence/releases

## Legal

This app is an independent open-source project and is not affiliated with any of the mentioned supermarket chains.

Own code: MIT License.
