package com.statisticservice.model;

import java.util.Date;

public class EyeRecognitionSample {
    private int id;
    private int memberId;
    private String eyeImageLink;
    private String label;
    private boolean isActive;
    private Date captureDate;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getMemberId() {
        return memberId;
    }

    public void setMemberId(int memberId) {
        this.memberId = memberId;
    }

    public String getEyeImageLink() {
        return eyeImageLink;
    }

    public void setEyeImageLink(String eyeImageLink) {
        this.eyeImageLink = eyeImageLink;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    public Date getCaptureDate() {
        return captureDate;
    }

    public void setCaptureDate(Date captureDate) {
        this.captureDate = captureDate;
    }
}