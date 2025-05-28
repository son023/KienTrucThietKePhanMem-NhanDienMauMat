package com.memberservice.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.GenericGenerator;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "tblRecognitionEvent")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RecognitionEvent {

    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    @Column(name = "imageLink", nullable = false)
    private String imageLink;

    @Column(name = "recognitionModelId", nullable = false)
    private UUID recognitionModelId;

    @Column(name = "eyeDetectionModelId", nullable = false)
    private UUID eyeDetectionModelId;

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