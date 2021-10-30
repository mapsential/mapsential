package com.mapsential.mapsential.detail;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.io.Serializable;

@NoArgsConstructor
@AllArgsConstructor
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@Entity
@Table(name = "details_defibrillator")
public class DetailDefibrillatorResource implements Serializable {

    @Id
    @Column(name = "id")
    private Long detailId;

    @Column(name = "operator")
    private String operator;

    @Column(name = "opening_times")
    private String opening_times;
}