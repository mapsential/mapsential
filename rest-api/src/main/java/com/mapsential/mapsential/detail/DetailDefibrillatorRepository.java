package com.mapsential.mapsential.detail;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DetailDefibrillatorRepository extends JpaRepository<DetailDefibrillatorResource, Long> {
}