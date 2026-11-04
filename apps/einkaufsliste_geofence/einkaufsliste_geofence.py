"""Einkaufsliste Geofence – dynamische Filial-Sensoren.

Erkennt automatisch originale Einkaufslisten-Sensoren und erstellt
pro Filiale einen dynamischen Sensor mit GPS-Koordinaten und
Geofence-Attributen.

Beispiel:
    sensor.einkaufsliste_zone_coop_6900

Keine Binary-Sensoren.
Keine Tracker-Überwachung.
Keine Änderungen an bestehenden Home-Assistant-Zonen.

Logging:
    INFO    nur bei Änderungen (neue/geänderte/entfernte Filiale)
    DEBUG   jeder Durchlauf (Details pro Filiale)
    WARNING Geocoding-Probleme (pro Adresse höchstens einmal je Wiederholungsintervall)
"""

import json
import os
import re
import time
import unicodedata
import urllib.parse
import urllib.request

import appdaemon.plugins.hass.hassapi as hass

# Fehlgeschlagene Geocoding-Versuche erst nach dieser Zeit wiederholen (Sekunden).
FAILED_RETRY_SECONDS = 3600


class EinkaufslisteGeofence(hass.Hass):

    def initialize(self):

        self.sensor_prefix = self.args.get(
            "sensor_prefix",
            "sensor.einkaufsliste_"
        )

        self.output_prefix = self.args.get(
            "output_prefix",
            "sensor.einkaufsliste_zone_"
        )

        self.radius = float(
            self.args.get("radius", 35)
        )

        self.update_interval = int(
            self.args.get("update_interval", 60)
        )

        self.cache_file = self.args.get(
            "cache_file",
            "/config/appdaemon/apps/einkaufsliste_geofence/geocode_cache.json"
        )

        self.geocode_cache = {}
        self.last_geocode = 0

        # Zustand für sparsames Logging
        self.failed_geocodes = {}      # cache_key -> Zeitpunkt des Fehlversuchs
        self.known_store_ids = None    # None = erster Durchlauf
        self.warned_collisions = set()

        self._load_cache()

        # Cache-Datei sofort anlegen, damit Pfad-/Rechteprobleme
        # direkt beim Start im Log sichtbar werden.
        if not os.path.exists(self.cache_file):
            self._save_cache()

        self.log(
            f"Einkaufsliste Geofence gestartet. "
            f"Standardradius: {self.radius} m, "
            f"Intervall: {self.update_interval} s, "
            f"Cache: {self.cache_file} "
            f"({len(self.geocode_cache)} Einträge)"
        )

        self.run_every(
            self.update,
            self.datetime(),
            self.update_interval
        )

    # ---------------------------------------------------------
    # Hilfsfunktionen
    # ---------------------------------------------------------

    @staticmethod
    def slugify(value):

        value = str(value or "").strip().lower()
        value = value.replace("ß", "ss")

        value = unicodedata.normalize(
            "NFKD",
            value
        )

        value = "".join(
            char for char in value
            if not unicodedata.combining(char)
        )

        value = re.sub(
            r"[^a-z0-9]+",
            "_",
            value
        )

        return value.strip("_")

    # ---------------------------------------------------------
    # Cache
    # ---------------------------------------------------------

    def _load_cache(self):

        try:

            if os.path.exists(self.cache_file):

                with open(
                    self.cache_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.geocode_cache = json.load(file)

        except Exception as exc:

            self.log(
                f"Geocoding-Cache konnte nicht geladen werden: {exc}",
                level="WARNING"
            )

    def _save_cache(self):

        try:

            directory = os.path.dirname(
                self.cache_file
            )

            os.makedirs(
                directory,
                exist_ok=True
            )

            temporary = self.cache_file + ".tmp"

            with open(
                temporary,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.geocode_cache,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            os.replace(
                temporary,
                self.cache_file
            )

        except Exception as exc:

            self.log(
                f"Cache konnte nicht gespeichert werden: {exc}",
                level="WARNING"
            )

    # ---------------------------------------------------------
    # Geocoding
    # ---------------------------------------------------------

    def geocode(
        self,
        address,
        plz="",
        ort="",
        land="CH"
    ):

        full_address = ", ".join(
            str(part).strip()
            for part in (address, land)
            if part
        )

        cache_key = full_address.lower()

        if cache_key in self.geocode_cache:
            return self.geocode_cache[cache_key]

        # Fehlgeschlagene Adressen nicht bei jedem Durchlauf neu abfragen.
        failed_at = self.failed_geocodes.get(cache_key)

        if (
            failed_at is not None
            and time.time() - failed_at < FAILED_RETRY_SECONDS
        ):
            return None

        wait = 1.1 - (
            time.time() - self.last_geocode
        )

        if wait > 0:
            time.sleep(wait)

        params = {
            "q": full_address,
            "format": "jsonv2",
            "limit": 1
        }

        if land:
            params["countrycodes"] = str(land).lower()

        url = (
            "https://nominatim.openstreetmap.org/search?"
            + urllib.parse.urlencode(params)
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "EinkaufslisteGeofence/2.0"
            }
        )

        try:

            self.last_geocode = time.time()

            with urllib.request.urlopen(
                request,
                timeout=15
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

            if not result:

                self.failed_geocodes[cache_key] = time.time()

                self.log(
                    f"Keine GPS-Koordinaten gefunden: "
                    f"{full_address} "
                    f"(neuer Versuch in {FAILED_RETRY_SECONDS // 60} min)",
                    level="WARNING"
                )

                return None

            coordinates = {
                "latitude": float(result[0]["lat"]),
                "longitude": float(result[0]["lon"])
            }

            self.geocode_cache[cache_key] = coordinates
            self.failed_geocodes.pop(cache_key, None)

            self._save_cache()

            self.log(
                f"Adresse geocodiert: {full_address} -> "
                f"{coordinates['latitude']}, "
                f"{coordinates['longitude']}"
            )

            return coordinates

        except Exception as exc:

            self.failed_geocodes[cache_key] = time.time()

            self.log(
                f"Geocoding-Fehler ({full_address}): {exc} "
                f"(neuer Versuch in {FAILED_RETRY_SECONDS // 60} min)",
                level="WARNING"
            )

            return None

    # ---------------------------------------------------------
    # Einkaufslisten-Sensoren erkennen
    # ---------------------------------------------------------

    def discover_stores(self):

        states = self.get_state() or {}

        stores = {}

        for entity_id, entity in states.items():

            # Nur originale Einkaufslisten-Sensoren erkennen.
            if not entity_id.startswith(self.sensor_prefix):
                continue

            # Selbst erzeugte Filial-Sensoren ausschliessen.
            if entity_id.startswith(self.output_prefix):
                continue

            if not isinstance(entity, dict):
                continue

            attributes = entity.get(
                "attributes",
                {}
            )

            if not isinstance(attributes, dict):
                continue

            address = attributes.get("adresse")
            store_name = attributes.get("geschaeft")
            plz = attributes.get("plz")
            ort = attributes.get("ort")
            land = attributes.get("land", "CH")

            if not address or not store_name or not plz:
                continue

            slug = self.slugify(store_name)
            zip_slug = self.slugify(plz)

            if not slug or not zip_slug:
                continue

            sensor_id = f"{slug}_{zip_slug}"

            # Kollision: zwei Quellsensoren ergeben dieselbe Sensor-ID.
            if sensor_id in stores:

                collision_key = (
                    sensor_id,
                    stores[sensor_id]["source_sensor"],
                    entity_id
                )

                if collision_key not in self.warned_collisions:

                    self.warned_collisions.add(collision_key)

                    self.log(
                        f"Doppelte Filiale {sensor_id}: "
                        f"{stores[sensor_id]['source_sensor']} und "
                        f"{entity_id}. Es wird nur der erste verwendet.",
                        level="WARNING"
                    )

                continue

            stores[sensor_id] = {
                "name": str(store_name).strip(),
                "address": str(address).strip(),
                "plz": str(plz).strip(),
                "ort": str(ort or "").strip(),
                "land": str(land or "CH").strip(),
                "source_sensor": entity_id
            }

        return stores

    # ---------------------------------------------------------
    # Filial-Sensoren erstellen / aktualisieren
    # ---------------------------------------------------------

    def _current_attributes(self, entity_id):
        """Aktuelle Attribute des Sensors in HA, oder None."""

        try:

            current = self.get_state(
                entity_id,
                attribute="all"
            )

            if isinstance(current, dict):
                return current.get("attributes") or {}

        except Exception:
            pass

        return None

    def create_store_sensor(
        self,
        sensor_id,
        store
    ):

        coordinates = self.geocode(
            store["address"],
            store["plz"],
            store["ort"],
            store["land"]
        )

        if coordinates is None:
            return False

        entity_id = (
            f"{self.output_prefix}{sensor_id}"
        )

        radius = float(
            self.args.get(
                f"radius_{sensor_id}",
                self.radius
            )
        )

        attributes = {
            "friendly_name": (
                f"{store['name']} {store['plz']}"
            ),
            "icon": "mdi:cart-outline",
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "radius": radius,
            "passive": False,
            "geschaeft": store["name"],
            "adresse": store["address"],
            "plz": store["plz"],
            "ort": store["ort"],
            "land": store["land"],
            "source_sensor": store["source_sensor"]
        }

        # Nur schreiben, wenn der Sensor fehlt oder sich etwas geändert hat.
        # Der Vergleich erfolgt mit dem echten HA-Zustand, damit der Sensor
        # nach einem HA-Neustart automatisch wieder angelegt wird.
        current = self._current_attributes(entity_id)

        if current is not None and all(
            current.get(key) == value
            for key, value in attributes.items()
        ):

            self.log(
                f"Filial-Sensor unverändert: {entity_id}",
                level="DEBUG"
            )

            return True

        is_new = current is None

        try:

            self.set_state(
                entity_id,
                state="ready",
                attributes=attributes
            )

            self.log(
                f"Filial-Sensor {'erstellt' if is_new else 'geändert'}: "
                f"{entity_id} "
                f"({coordinates['latitude']}, "
                f"{coordinates['longitude']}, "
                f"Radius {radius:g} m) "
                f"Quelle: {store['source_sensor']}"
            )

            return True

        except Exception as exc:

            self.log(
                f"Fehler beim Erstellen von "
                f"{entity_id}: {exc}",
                level="ERROR"
            )

            return False

    # ---------------------------------------------------------
    # Aktualisierung
    # ---------------------------------------------------------

    def update(self, kwargs):

        try:

            stores = self.discover_stores()

            current_ids = set(stores)

            # Änderungen an der Filialliste melden (INFO),
            # sonst nur DEBUG.
            if self.known_store_ids is None:

                self.log(
                    f"{len(stores)} Filiale(n) erkannt: "
                    f"{', '.join(sorted(current_ids)) or '-'}"
                )

            elif current_ids != self.known_store_ids:

                added = sorted(current_ids - self.known_store_ids)
                removed = sorted(self.known_store_ids - current_ids)

                if added:
                    self.log(
                        f"Neue Filiale(n): {', '.join(added)}"
                    )

                if removed:
                    self.log(
                        f"Filiale(n) nicht mehr vorhanden: "
                        f"{', '.join(removed)}"
                    )

            else:

                self.log(
                    f"{len(stores)} Filiale(n) erkannt.",
                    level="DEBUG"
                )

            self.known_store_ids = current_ids

            for sensor_id, store in sorted(
                stores.items()
            ):

                self.log(
                    f"Filiale erkannt: {store['name']} "
                    f"({store['plz']} {store['ort']}) "
                    f"Quelle: {store['source_sensor']}",
                    level="DEBUG"
                )

                self.create_store_sensor(
                    sensor_id,
                    store
                )

        except Exception as exc:

            self.log(
                f"Fehler bei der Filial-Aktualisierung: "
                f"{exc}",
                level="ERROR"
            )

    # ---------------------------------------------------------
    # Beenden
    # ---------------------------------------------------------

    def terminate(self):

        self._save_cache()

        self.log(
            "Einkaufsliste Geofence beendet."
        )
