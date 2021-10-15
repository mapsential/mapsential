package com.mapsential.mapsential.detail;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.mapsential.mapsential.location.LocationType;
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
@Table(name = "details")
public class DetailResource implements Serializable {

    @Id
//    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long detailId;

    @Column(name = "opening_time")
    private Long openingTime;

    @Column(name = "closing_time")
    private Long closingTime;


//    @Column(name = "location_id")
//    private Long locationId;
//
//    @Column(name = "review_list")
//    private List<Long> locationReviewList;
//
//    @Column(name = "reviewCount")
//    private Long locationReviewCount;


}