package com.mapsential.mapsential.detail;

import com.mapsential.mapsential.location.LocationType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DetailRepository extends JpaRepository<DetailResource, Long>{
}