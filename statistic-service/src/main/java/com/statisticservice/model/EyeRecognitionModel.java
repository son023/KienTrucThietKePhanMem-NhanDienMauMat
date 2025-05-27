package com.statisticservice.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;
import java.util.List;
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EyeRecognitionModel {
    private int id;
    private String modelLink;
    private String eyeModelName;
    private List<EyeRecognitionSampleHistory> eyeRecognitionSampleTrain;
    private float accuracy;
    private float f1_score;
    private float precision;
    private boolean isActive;
    private int epochs;
    private float learningRate;
    private int imageSize;
    private int batchSize;
    private String mappingLabel;
    private int trainingTime;
    private Date createDate;

}