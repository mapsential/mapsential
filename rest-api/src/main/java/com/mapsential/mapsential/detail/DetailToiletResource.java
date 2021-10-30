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
@Table(name = "details_toilet")
public class DetailToiletResource implements Serializable {

    @Id
    @Column(name = "id")
    private Long detailId;

    @Column(name = "operator")
    private String operator;

    @Column(name = "opening_times")
    private String openingTimes;

    @Column(name = "has_fee")
    private Boolean hasFee;

    @Column(name = "is_customer_only")
    private Boolean isCustomerOnly;

    @Column(name = "female")
    private Boolean female;

    @Column(name = "male")
    private Boolean male;

    @Column(name = "unisex")
    private Boolean unisex;

    @Column(name = "child")
    private Boolean child;

    @Column(name = "has_seated")
    private Boolean hasSeated;

    @Column(name = "has_urinal")
    private Boolean hasUrinal;

    @Column(name = "has_squat")
    private Boolean hasSquat;

    @Column(name = "change_table")
    private String changeTable;

    @Column(name = "wheelchair_accessible")
    private String wheelchairAccessible;

    @Column(name = "wheelchair_access_info")
    private String wheelchairAccessInfo;

    @Column(name = "has_hand_washing")
    private Boolean hasHandWashing;

    @Column(name = "has_soap")
    private Boolean hasSoap;

    @Column(name = "has_hand_disinfectant")
    private Boolean hasHandDisinfectant;

    @Column(name = "has_hand_creme")
    private Boolean hasHandCreme;

    @Column(name = "has_hand_drying")
    private Boolean hasHandDrying;

    @Column(name = "hand_drying_method")
    private String handDryingMethod;

    @Column(name = "has_paper")
    private Boolean hasPaper;

    @Column(name = "has_hot_water")
    private Boolean hasHotWater;

    @Column(name = "has_drinking_water")
    private Boolean hasDrinkingWater;
}