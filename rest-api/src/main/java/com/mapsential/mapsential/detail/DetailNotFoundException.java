package com.mapsential.mapsential.detail;

public class DetailNotFoundException extends RuntimeException {

    private String detailType;
    private Long detailId;

    DetailNotFoundException(String type, Long detailId) {
        super(
                "Could not find " + type.replace("_", " ") + " details "
                        + " with id \"" + detailId + "\""
        );

        this.detailType = type;
        this.detailId = detailId;
    }

    public String getDetailType() {
        return detailType;
    }

    public Long getDetailId() {
        return detailId;
    }
}
