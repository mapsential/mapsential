package com.mapsential.mapsential.location;

public class LocationNotFoundException extends RuntimeException {

    private final Long locationId;

    LocationNotFoundException(Long locationId) {
        super(
                "Could not find location with id \"" + locationId + "\""
        );

        this.locationId = locationId;
    }

    public Long getLocationId() {
        return locationId;
    }
}
