package com.mapsential.mapsential.location;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LocationRepository extends JpaRepository<LocationResource, Long>{

    @Query(value = "SELECT * FROM locations WHERE type = ?1", nativeQuery = true)
    List<LocationResource> findByLocationType(String locationType);

    @Query(value = "SELECT * FROM locations WHERE type IN ?1", nativeQuery = true) //Ob der Type im Array ist
    List<LocationResource> findByLocationTypes(String[] locationType);
}
