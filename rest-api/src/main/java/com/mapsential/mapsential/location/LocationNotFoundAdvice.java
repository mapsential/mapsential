package com.mapsential.mapsential.location;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.LinkedHashMap;
import java.util.Map;

@ControllerAdvice
public class LocationNotFoundAdvice {

    @ExceptionHandler(LocationNotFoundException.class)
    ResponseEntity<Object> detailsNotFoundHandler(LocationNotFoundException exception) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("locationId", exception.getLocationId());
        body.put("errorMessage", exception.getMessage());

        return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
    }
}
