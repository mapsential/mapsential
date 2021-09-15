package com.mapsential.mapsential.detail;

import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@NoArgsConstructor
@RestController
public class DetailController {
    @Autowired
    DetailService detailService;

    @Autowired
    DetailRepository detailRepository;

    @GetMapping(path = "/api/details/{detailId}", produces = "application/json")
    public Object getDetailsById(@PathVariable Long detailId) {
        Optional<DetailResource> detailResourceOptional = detailService.findById(detailId);
        if (!detailResourceOptional.isPresent()){
            return ("Details with ID " + detailId + " could not be found");
        }
        return detailResourceOptional;
    }

}