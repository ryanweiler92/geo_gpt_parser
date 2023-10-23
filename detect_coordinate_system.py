def detect_coordinate_system(dataset):
    def _guess_system(lat, lon):
        # Guess the coordinate system based on latitude and longitude.
        if (-90 <= lat <= 90) and (-180 <= lon <= 180):
            return "EPSG:4326"
        else:
            return "EPSG:3857"

    # Counters for the two systems
    epsg_4326_count = 0
    epsg_3857_count = 0

    # Check each item in the dataset
    for item in dataset:
        lat = item["latitude"]
        lon = item["longitude"]

        system = _guess_system(lat, lon)
        if system == "EPSG:4326":
            epsg_4326_count += 1
        else:
            epsg_3857_count += 1

    # Compare the two counts and return the majority system
    if epsg_4326_count > epsg_3857_count:
        return "EPSG:4326"
    else:
        return "EPSG:3857"
