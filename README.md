# FT0360 Weather Station – Home Assistant Integration

Home Assistant Custom Component für die **Landi FT0360** Wetterstation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

---

## Sensoren

| Sensor | Einheit |
|---|---|
| Innentemperatur | °C |
| Innenluftfeuchtigkeit | % |
| Aussentemperatur | °C |
| Aussenluftfeuchtigkeit | % |
| Luftdruck absolut | hPa |
| Luftdruck relativ | hPa |
| Windgeschwindigkeit | m/s |
| Windböe | m/s |
| Max. Tagesböe | m/s |
| Windrichtung | ° |
| Windrichtung (Text) | N / NO / O … |
| Ø Wind 2 Minuten | m/s |
| Ø Wind 10 Minuten | m/s |
| Regenrate | mm/h |
| Regen letzte Stunde | mm |
| Regen heute | mm |
| Regen diese Woche | mm |
| Regen diesen Monat | mm |
| Regen dieses Jahr | mm |
| Regen gesamt | mm |
| Solarstrahlung | W/m² |
| UV-Index | – |

---

## Installation

### Via HACS (empfohlen)

1. Repository in HACS hinzufügen: [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DeadMonkey428&repository=ha_ft0360&category=integration)
2. Integration in HACS suchen und installieren
3. Home Assistant neu starten

### Manuell

Den Ordner `custom_components/ft0360` in dein Home Assistant Verzeichnis `config/custom_components/` kopieren und HA neu starten.

---

## Einrichtung

Integration über die UI einrichten: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ft0360)

- **Host**: IP-Adresse oder Hostname der Wetterstation (z. B. `192.168.1.100`)
- **Abfrageintervall**: Polling-Intervall in Sekunden (Standard: 30 s, Min: 5 s, Max: 300 s)

Die Station muss im lokalen Netzwerk erreichbar sein und die Endpunkte `/client?command=record` sowie `/client?command=about` bereitstellen.

---

## Voraussetzungen

- Home Assistant ≥ 2026.5.4
- Wetterstation im selben Netzwerk wie HA erreichbar

---

## Entwicklungsumgebung

Entwickelt und getestet auf:

| Komponente | Version |
|---|---|
| Home Assistant OS | 17.3 |
| Home Assistant Core | 2026.5.4 |
| Supervisor | 2026.05.1 |
| Frontend | 20260429.4 |
| Installationsmethode | Home Assistant OS |
