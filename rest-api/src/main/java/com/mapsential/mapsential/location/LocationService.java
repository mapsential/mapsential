package com.mapsential.mapsential.location;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class LocationService {

    @Autowired
    private LocationRepository locationRepository;

    public Optional<LocationResource> findById(Long locationId) {
        return locationRepository.findById(locationId);
    }

    public List<LocationResource> getAllLocations() {
        return locationRepository.findAll();
    }

    public List<LocationResource> getLocationsByType(LocationType locationType) {
        return locationRepository.findByLocationType(locationType);
    }

    public List<LocationResource> getLocationsByTypes(LocationType[] locationType) {
        return locationRepository.findByLocationTypes(locationType);
    }

}
