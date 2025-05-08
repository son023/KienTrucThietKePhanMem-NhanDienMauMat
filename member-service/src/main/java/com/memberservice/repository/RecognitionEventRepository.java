package com.memberservice.repository;

import com.memberservice.entity.RecognitionEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface RecognitionEventRepository extends JpaRepository<RecognitionEvent, Integer> {
    List<RecognitionEvent> findByMemberId(Integer memberId);
    List<RecognitionEvent> findByCameraName(String cameraName);
    List<RecognitionEvent> findByIsSuccessful(Boolean isSuccessful);

    // Thêm phương thức mới
    List<RecognitionEvent> findByRecognitionModelIdAndTimeVerifyBetween(
            Integer recognitionModelId, LocalDateTime startDate, LocalDateTime endDate);

    // Phương thức cho tất cả sự kiện trong khoảng thời gian
    List<RecognitionEvent> findByTimeVerifyBetween(LocalDateTime startDate, LocalDateTime endDate);
}