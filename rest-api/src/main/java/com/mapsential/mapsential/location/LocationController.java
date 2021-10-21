package com.mapsential.mapsential.location;

import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.swing.text.html.Option;
import java.util.List;
import java.util.Optional;

@NoArgsConstructor
@RestController
public class LocationController {
    @Autowired
    LocationService locationService;

    @Autowired
    LocationRepository locationRepository;

    @GetMapping(path = "/api/location/{locationId}", produces = "application/json")
    public Object getLocationById(@PathVariable Long locationId) {
        Optional<LocationResource> locationResourceOptional = locationService.findById(locationId);
        if (!locationResourceOptional.isPresent()){
            return ("Location with ID " + locationId + " could not be found");
        }
        return locationResourceOptional;
    }

    @GetMapping(value = "/api/location", produces = "application/json")
    public List<LocationResource> getAllLocations() {
        return locationService.getAllLocations();
    }

    @GetMapping(value = "/api/location/{locationType}", produces = "application/json")
    public List<LocationResource> getLocationsByType(@PathVariable LocationType locationType) {
        return locationService.getLocationsByType(locationType);
    }

    @GetMapping(value = "/api/locations/{locationTypes}", produces = "application/json")
    public List<LocationResource> getLocationsByTypes(@RequestParam LocationType[] locationTypes) {
        return locationService.getLocationsByTypes(locationTypes);
    }

}
