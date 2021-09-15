package com.mapsential.mapsential.detail;

import com.mapsential.mapsential.location.LocationType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class DetailService {

    @Autowired
    private DetailRepository detailRepository;

    public Optional<DetailResource> findById(Long detailId) {
        return detailRepository.findById(detailId);
    }
}
