package com.mapsential.mapsential.location;

import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@NoArgsConstructor
@RestController
public class LocationController {
    @Autowired
    LocationService locationService;

    @Autowired
    LocationRepository locationRepository;

    @GetMapping(path = "/api/location/{locationId}", produces = "application/json")
    public Object getLocationById(@PathVariable Long locationId) {
//        try {
//            if (!locationService.findById(locationId).isPresent()){
//                return MyResourceNotFoundException.notFound("Location with ID " + locationId + " could not be found");
//            }
//        } catch (Exception e){
//            return MyResourceNotFoundException.badRequest(e);
//        }
        return locationService.findById(locationId);
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
    public List<LocationResource> getLocationsByType(@RequestParam LocationType[] locationTypes) {
        return locationService.getLocationsByType(locationTypes);
    }

}
