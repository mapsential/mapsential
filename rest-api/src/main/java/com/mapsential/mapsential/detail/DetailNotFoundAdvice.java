package com.mapsential.mapsential.detail;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.LinkedHashMap;
import java.util.Map;

@ControllerAdvice
public class DetailNotFoundAdvice {

    @ExceptionHandler(DetailNotFoundException.class)
    ResponseEntity<Object> detailsNotFoundHandler(DetailNotFoundException exception) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("detailType", exception.getDetailType());
        body.put("detailId", exception.getDetailId());
        body.put("errorMessage", exception.getMessage());

        return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
    }
}
