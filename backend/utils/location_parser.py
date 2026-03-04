import re


def detect_location_type(location_str):
    """
    Detect the type of location input.

    Returns:
        "gps"
        "us_zip"
        "ca_postal"
        "text"
    """

    location_str = location_str.strip()

    # GPS coordinates
    if "," in location_str:
        parts = location_str.split(",")
        if len(parts) == 2:
            try:
                float(parts[0])
                float(parts[1])
                return "gps"
            except ValueError:
                pass

    # US ZIP code (5 digits)
    if re.fullmatch(r"\d{5}", location_str):
        return "us_zip"

    # Canadian postal code
    if re.fullmatch(r"[A-Za-z]\d[A-Za-z]\d[A-Za-z]\d", location_str.replace(" ", "")):
        return "ca_postal"

    # Default: city / landmark text
    return "text"