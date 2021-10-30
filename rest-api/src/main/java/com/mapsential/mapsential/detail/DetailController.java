package com.mapsential.mapsential.detail;

import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin(origins = "*", allowedHeaders = "*")
@NoArgsConstructor
@RestController
public class DetailController {

    @Autowired
    DetailDefibrillatorRepository detailDefibrillatorRepository;

    @Autowired
    DetailDrinkingFountainRepository detailDrinkingFountainRepository;

    @Autowired
    DetailSoupKitchenRepository detailSoupKitchenRepository;

    @Autowired
    DetailToiletRepository detailToiletRepository;

    @GetMapping(path = "/api/details/defibrillator/{detailId}", produces = "application/json")
    public DetailDefibrillatorResource getDetailDefibrillatorById(@PathVariable Long detailId) {
        return detailDefibrillatorRepository.findById(
                detailId
        ).orElseThrow(() -> new DetailNotFoundException("defibrillator", detailId));
    }

    @GetMapping(path = "/api/details/drinking_fountain/{detailId}", produces = "application/json")
    public DetailDrinkingFountainResource getDetailDrinkingFountainById(@PathVariable Long detailId) {
        return detailDrinkingFountainRepository.findById(
                detailId
        ).orElseThrow(() -> new DetailNotFoundException("drinking_fountain", detailId));
    }

    @GetMapping(path = "/api/details/soup_kitchen/{detailId}", produces = "application/json")
    public DetailSoupKitchenResource getDetailSoupKitchenById(@PathVariable Long detailId) {
        return detailSoupKitchenRepository.findById(
                detailId
        ).orElseThrow(() -> new DetailNotFoundException("soup_kitchen", detailId));
    }

    @GetMapping(path = "/api/details/toilet/{detailId}", produces = "application/json")
    public DetailToiletResource getDetailToiletById(@PathVariable Long detailId) {
        return detailToiletRepository.findById(
                detailId
        ).orElseThrow(() -> new DetailNotFoundException("toilet", detailId));
    }
}
