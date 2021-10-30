package com.mapsential.mapsential.detail;

public class DetailNotFoundException extends RuntimeException {

    private String detailType;
    private Long detailId;

    DetailNotFoundException(String type, Long id) {
        super(
                "Could not find " + type.replace("_", " ") + " details "
                        + " with id \"" + id + "\""
        );

        this.detailType = type;
        this.detailId = id;
    }

    public String getDetailType() {
        return detailType;
    }

    public Long getDetailId() {
        return detailId;
    }
}
