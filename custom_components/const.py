"""Constants for the FT0360 Weather Station integration."""

DOMAIN = "ft0360"

CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 30
MIN_SCAN_INTERVAL = 5
MAX_SCAN_INTERVAL = 300

ENDPOINT_RECORD = "/client?command=record"
ENDPOINT_ABOUT = "/client?command=about"

MANUFACTURER = "Landi"
MODEL = "FT0360"
