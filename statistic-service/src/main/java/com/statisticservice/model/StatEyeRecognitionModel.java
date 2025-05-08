package com.statisticservice.model;

import java.util.Date;
import java.util.List;

public class StatEyeRecognitionModel {
    private EyeRecognitionModel model_stats;
    private Date startDate;
    private Date endDate;
    private List<RecognitionEvent> recognitionEvent;
    private float falsePositiveRate;
    private float accuracyRate;
    private int success;
    private int fail;

    public EyeRecognitionModel getModel_stats() {
        return model_stats;
    }

    public void setModel_stats(EyeRecognitionModel model_stats) {
        this.model_stats = model_stats;
    }

    public Date getStartDate() {
        return startDate;
    }

    public void setStartDate(Date startDate) {
        this.startDate = startDate;
    }

    public Date getEndDate() {
        return endDate;
    }

    public void setEndDate(Date endDate) {
        this.endDate = endDate;
    }

    public List<RecognitionEvent> getRecognitionEvent() {
        return recognitionEvent;
    }

    public void setRecognitionEvent(List<RecognitionEvent> recognitionEvent) {
        this.recognitionEvent = recognitionEvent;
    }

    public float getFalsePositiveRate() {
        return falsePositiveRate;
    }

    public void setFalsePositiveRate(float falsePositiveRate) {
        this.falsePositiveRate = falsePositiveRate;
    }

    public float getAccuracyRate() {
        return accuracyRate;
    }

    public void setAccuracyRate(float accuracyRate) {
        this.accuracyRate = accuracyRate;
    }

    public int getSuccess() {
        return success;
    }

    public void setSuccess(int success) {
        this.success = success;
    }

    public int getFail() {
        return fail;
    }

    public void setFail(int fail) {
        this.fail = fail;
    }
}