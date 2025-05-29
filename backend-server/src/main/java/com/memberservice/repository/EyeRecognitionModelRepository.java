package com.memberservice.repository;

import com.memberservice.entity.EyeRecognitionModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface EyeRecognitionModelRepository extends JpaRepository<EyeRecognitionModel, UUID> {
    
    List<EyeRecognitionModel> findByIsActiveTrueOrderByCreateDateDesc();
    
    List<EyeRecognitionModel> findAllByOrderByCreateDateDesc();
    
    @Query("SELECT m FROM EyeRecognitionModel m LEFT JOIN FETCH m.histories h LEFT JOIN FETCH h.eyeRecognitionSample WHERE m.id = :modelId")
    Optional<EyeRecognitionModel> findByIdWithHistories(@Param("modelId") UUID modelId);
} 