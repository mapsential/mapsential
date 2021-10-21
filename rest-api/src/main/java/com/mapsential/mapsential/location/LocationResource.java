package com.mapsential.mapsential.location;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.io.Serializable;
import java.util.List;

@NoArgsConstructor //zum erzeugen der Constructors ohne Argumente
@AllArgsConstructor
@Data //erzeugt autom. alle getter und setter
@JsonInclude(JsonInclude.Include.NON_NULL) //alle Werte mit null werden ignoriert
@Entity
@Table(name = "locations") //Name der Tabelle
public class LocationResource implements Serializable {

    @Id //Pimärschlüssel
    @Column(name = "id") //Name der Spalte
    private Long locationId;

    @JsonIgnore
    @Column(name = "details_id")//Name der Spalte
    private Long detailsId;

    @Column(name = "type")
    private String locationType;

    @Column(name = "name")
    private String locationName;

    @Column(name = "address")
    private String locationAddress;

    @Column(name = "longitude") //längengrad → north south
    private Long longitude;

    @Column(name = "latitude") //breitengrad → east west
    private Long latitude;
}