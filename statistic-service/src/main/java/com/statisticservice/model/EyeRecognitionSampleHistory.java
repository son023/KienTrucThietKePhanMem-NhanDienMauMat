package com.statisticservice.model;

public class EyeRecognitionSampleHistory {
    private int id;
    private EyeRecognitionSample eyeRecognitionSample;
    private String notes;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public EyeRecognitionSample getEyeRecognitionSample() {
        return eyeRecognitionSample;
    }

    public void setEyeRecognitionSample(EyeRecognitionSample eyeRecognitionSample) {
        this.eyeRecognitionSample = eyeRecognitionSample;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }
}