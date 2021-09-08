package com.mapsential.mapsential.location;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LocationRepository extends JpaRepository<LocationResource, Long>{

    @Query("SELECT * FROM locations WHERE type = ?1")
    List<LocationResource> findByLocationType(LocationType locationType);
}