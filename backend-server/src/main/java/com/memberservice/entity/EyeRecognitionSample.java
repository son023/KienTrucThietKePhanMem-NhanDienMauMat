package com.memberservice.entity;

import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.GenericGenerator;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "tblEyeRecognitionSample")
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class EyeRecognitionSample {

    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    @Column(name = "id", updatable = false, nullable = false)
    @JsonProperty("id")
    private UUID id;

    @Column(name = "eyeImageLink", nullable = false)
    @JsonProperty("eyeImageLink")
    private String eyeImageLink;

    @Column(name = "label")
    @JsonProperty("label")
    private String label;

    @Column(name = "isActive", nullable = false)
    @JsonProperty("isActive")
    private Boolean isActive = true;

    @Column(name = "captureDate")
    @JsonProperty("captureDate")
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime captureDate;

    // Chỉ serialize member object với các field cần thiết
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "memberId")
    @JsonIgnoreProperties({
            "hibernateLazyInitializer",
            "handler",
            "password",              // Bỏ qua password
            "eyeRecognitionSamples", // Tránh circular reference
            "createdAt",
            "updatedAt"
    })
    @JsonProperty("member")
    private Member member;
}