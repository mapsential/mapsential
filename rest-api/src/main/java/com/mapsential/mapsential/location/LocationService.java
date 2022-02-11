package com.mapsential.mapsential.location;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class LocationService {

    public static final Double CHUNK_SIZE = 1.0;

    @Autowired
    private LocationRepository locationRepository;

    public Optional<LocationResource> findById(Long locationId) {
        return locationRepository.findById(locationId);
    }

    public List<LocationResource> getAllLocations() {
        return locationRepository.findAll();
    }

    public List<LocationResource> getLocationsByType(String locationType) {
        return locationRepository.findByLocationType(locationType);
    }

    public List<LocationResource> getLocationsByTypes(String[] locationType) {
        return locationRepository.findByLocationTypes(locationType);
    }

    public List<LocationResource> getLocationsInChunk(Double longitude, Double latitude) {
        return locationRepository.findLocationInChunk(longitude, longitude + CHUNK_SIZE, latitude, latitude + CHUNK_SIZE);
    }
}
