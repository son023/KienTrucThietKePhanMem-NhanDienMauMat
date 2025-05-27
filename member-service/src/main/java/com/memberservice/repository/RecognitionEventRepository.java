package com.memberservice.repository;

import com.memberservice.entity.RecognitionEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface RecognitionEventRepository extends JpaRepository<RecognitionEvent, Integer> {

    List<RecognitionEvent> findByRecognitionModelIdAndTimeVerifyBetween(
            Integer recognitionModelId, LocalDateTime startDate, LocalDateTime endDate);

    List<RecognitionEvent> findByTimeVerifyBetween(LocalDateTime startDate, LocalDateTime endDate);
}