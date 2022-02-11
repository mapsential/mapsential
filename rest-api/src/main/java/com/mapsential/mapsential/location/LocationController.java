package com.mapsential.mapsential.location;

import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@CrossOrigin(origins = "*", allowedHeaders = "*")
@NoArgsConstructor
@RestController
public class LocationController {
    @Autowired
    LocationService locationService;

    @Autowired
    LocationRepository locationRepository;

    @GetMapping(path = "/api/location/{locationId}", produces = "application/json")
    public LocationResource getLocationById(@PathVariable Long locationId) {
        return locationService.findById(locationId).orElseThrow(
                () -> new LocationNotFoundException(locationId)
        );
    }

    @GetMapping(value = "/api/location", produces = "application/json")
    public List<LocationResource> getAllLocations() {
        return locationService.getAllLocations();
    }

    @GetMapping(value = "/api/filter_location/{locationType}", produces = "application/json")
    public List<LocationResource> getLocationsByType(@PathVariable String locationType) {
        return locationService.getLocationsByType(locationType);
    }

    @GetMapping(value = "/api/filter_locations/{locationTypes}", produces = "application/json")
    public List<LocationResource> getLocationsByTypes(@PathVariable String[] locationTypes) {
        return locationService.getLocationsByTypes(locationTypes);
    }

    @GetMapping(value = "/api/location/{latitude}/{longitude}", produces = "application/json")
    public List<LocationResource> getLocationsInChunk(@PathVariable Double longitude, @PathVariable Double latitude){
        return locationService.getLocationsInChunk(longitude, latitude);
    }

}
