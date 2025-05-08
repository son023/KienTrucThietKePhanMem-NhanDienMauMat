package com.memberservice.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "tblRecognitionEvent")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RecognitionEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "imageLink", nullable = false)
    private String imageLink;

    @Column(name = "recognitionModelId", nullable = false)
    private Integer recognitionModelId;

    @Column(name = "eyeDetectionModelId", nullable = false)
    private Integer eyeDetectionModelId;

    @Column(name = "cameraName", nullable = false)
    private String cameraName;

    @Column(name = "timeVerify")
    private LocalDateTime timeVerify;

    @Column(name = "isSuccessful")
    private Boolean isSuccessful;

    @Column(name = "accuracy")
    private Float accuracy;

    @ManyToOne
    @JoinColumn(name = "tblMemberId")
    private Member member;
}