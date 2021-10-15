package com.mapsential.mapsential.location;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LocationRepository extends JpaRepository<LocationResource, Long>{

    @Query("SELECT l.name FROM locations l WHERE l.type = ?1")
    List<LocationResource> findByLocationType(LocationType locationType);

    @Query("SELECT l.name FROM locations l WHERE l.type IN ?1") //Ob der Type im Array ist
    List<LocationResource> findByLocationTypes(LocationType[] locationType);
}

//https://stackoverflow.com/questions/47276262/unexpected-tokenwhere-when-using-spring-data-jpa-with-hibernate
