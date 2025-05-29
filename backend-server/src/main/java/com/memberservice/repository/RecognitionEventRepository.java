package com.memberservice.repository;

import com.memberservice.entity.RecognitionEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Repository
public interface RecognitionEventRepository extends JpaRepository<RecognitionEvent, UUID> {

    List<RecognitionEvent> findByRecognitionModelIdAndTimeVerifyBetween(
            UUID recognitionModelId, LocalDateTime startDate, LocalDateTime endDate);

    List<RecognitionEvent> findByTimeVerifyBetween(LocalDateTime startDate, LocalDateTime endDate);
}