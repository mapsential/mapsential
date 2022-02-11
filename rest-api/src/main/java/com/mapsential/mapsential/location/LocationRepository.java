package com.mapsential.mapsential.location;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LocationRepository extends JpaRepository<LocationResource, Long> {

    @Query(value = "SELECT * FROM locations WHERE type = ?1", nativeQuery = true)
    List<LocationResource> findByLocationType(String locationType);

    @Query(value = "SELECT * FROM locations WHERE type IN ?1", nativeQuery = true)
    List<LocationResource> findByLocationTypes(String[] locationType);

    @Query(value = "SELECT * FROM locations WHERE longitude >= ?1 AND longitude <= ?2 AND latitude >= ?3 AND latitude <= ?4", nativeQuery = true)
    List<LocationResource> findLocationInChunk(Double longitude, Double longitudePlusChunk, Double latitude, Double latitudePlusChunk);
}
