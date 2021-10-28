package com.mapsential.mapsential.location;

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
@Table(name = "locations")
public class LocationResource implements Serializable {

    @Id
    @Column(name = "id")
    private Long locationId;

    @Column(name = "details_id")
    private Long detailsId;

    @Column(name = "type")
    private String locationType;

    @Column(name = "name")
    private String locationName;

    @Column(name = "address")
    private String locationAddress;

    @Column(name = "longitude")
    private Double longitude;

    @Column(name = "latitude")
    private Double latitude;
}
