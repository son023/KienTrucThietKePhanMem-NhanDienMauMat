package com.statisticservice.model;

import java.util.Date;
import java.util.List;

public class EyeRecognitionModel {
    private int id;
    private String modelLink;
    private String eyeModelName;
    private List<EyeRecognitionSampleHistory> eyeRecognitionSampleTrain;
    private float accuracy;
    private boolean isActive;
    private int epochs;
    private float learningRate;
    private int imageSize;
    private int batchSize;
    private String mappingLabel;
    private int trainingTime;
    private Date createDate;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getModelLink() {
        return modelLink;
    }

    public void setModelLink(String modelLink) {
        this.modelLink = modelLink;
    }

    public String getEyeModelName() {
        return eyeModelName;
    }

    public void setEyeModelName(String eyeModelName) {
        this.eyeModelName = eyeModelName;
    }

    public List<EyeRecognitionSampleHistory> getEyeRecognitionSampleTrain() {
        return eyeRecognitionSampleTrain;
    }

    public void setEyeRecognitionSampleTrain(List<EyeRecognitionSampleHistory> eyeRecognitionSampleTrain) {
        this.eyeRecognitionSampleTrain = eyeRecognitionSampleTrain;
    }

    public float getAccuracy() {
        return accuracy;
    }

    public void setAccuracy(float accuracy) {
        this.accuracy = accuracy;
    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    public int getEpochs() {
        return epochs;
    }

    public void setEpochs(int epochs) {
        this.epochs = epochs;
    }

    public float getLearningRate() {
        return learningRate;
    }

    public void setLearningRate(float learningRate) {
        this.learningRate = learningRate;
    }

    public int getImageSize() {
        return imageSize;
    }

    public void setImageSize(int imageSize) {
        this.imageSize = imageSize;
    }

    public int getBatchSize() {
        return batchSize;
    }

    public void setBatchSize(int batchSize) {
        this.batchSize = batchSize;
    }

    public String getMappingLabel() {
        return mappingLabel;
    }

    public void setMappingLabel(String mappingLabel) {
        this.mappingLabel = mappingLabel;
    }

    public Date getCreateDate() {
        return createDate;
    }

    public void setCreateDate(Date createDate) {
        this.createDate = createDate;
    }

    public int getTrainingTime() {
        return trainingTime;
    }

    public void setTrainingTime(int trainingTime) {
        this.trainingTime = trainingTime;
    }
}