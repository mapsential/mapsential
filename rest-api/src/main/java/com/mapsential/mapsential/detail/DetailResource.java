package com.mapsential.mapsential.detail;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.io.Serializable;

@NoArgsConstructor
@AllArgsConstructor
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@Entity
@Table(name = "details")
public class DetailResource implements Serializable {

    @Id
    @Column(name = "id")
    private Long detailId;

    @Column(name = "opening_times")
    private String openingTime;


//    @Column(name = "location_id")
//    private Long locationId;
//
//    @Column(name = "review_list")
//    private List<Long> locationReviewList;
//
//    @Column(name = "reviewCount")
//    private Long locationReviewCount;


}
