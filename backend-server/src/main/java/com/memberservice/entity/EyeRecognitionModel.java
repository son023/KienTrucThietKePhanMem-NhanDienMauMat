package com.memberservice.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.GenericGenerator;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "tblEyeRecognitionModel")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EyeRecognitionModel {

    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    @Column(name = "modelLink")
    private String modelLink;

    @Column(name = "eyeModelName")
    private String eyeModelName;

    @Column(name = "accuracy")
    private Double accuracy;

    @Column(name = "f1Score")
    private Double f1Score;

    @Column(name = "precision")
    private Double precision;

    @Column(name = "isActive", nullable = false)
    private Boolean isActive = true;

    @Column(name = "epochs")
    private Integer epochs;

    @Column(name = "learningRate")
    private Double learningRate;

    @Column(name = "imageSize")
    private Integer imageSize;

    @Column(name = "batchSize")
    private Integer batchSize;

    @Column(name = "mappingLabel")
    private String mappingLabel;

    @Column(name = "trainingTime")
    private Integer trainingTime;

    @Column(name = "createDate")
    private LocalDateTime createDate;

    @Column(name = "modeltype")
    private String modelType;

    @OneToMany(mappedBy = "model", fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JsonProperty("eyeRecognitionSampleHistory")
    private List<EyeRecognitionSampleHistory> histories;
} 