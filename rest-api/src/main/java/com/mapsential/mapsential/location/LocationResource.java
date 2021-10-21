package com.mapsential.mapsential.location;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.io.Serializable;
import java.util.List;

@NoArgsConstructor
@AllArgsConstructor
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@Entity
@Table(name = "locations")
public class LocationResource implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long locationId;

    @Column(name = "details_id")
    private Long detailsId;

    @Column(name = "type")
    private LocationType locationType;

    @Column(name = "name")
    private String locationName;

    @Column(name = "address")
    private String locationAddress;

    @Column(name = "longitude") //längengrad → north south
    private Long longitude;

    @Column(name = "latitude") //breitengrad → east west
    private Long latitude;
}
