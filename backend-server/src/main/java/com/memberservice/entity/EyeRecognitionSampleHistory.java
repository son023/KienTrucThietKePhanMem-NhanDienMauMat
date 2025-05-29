package com.memberservice.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.GenericGenerator;
import java.util.UUID;

@Entity
@Table(name = "tblEyeRecognitionSampleHistory")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EyeRecognitionSampleHistory {

    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    @Column(name = "notes")
    private String notes;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "modelId")
    @JsonIgnore
    private EyeRecognitionModel model;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "sampleId")
    private EyeRecognitionSample eyeRecognitionSample;
} 