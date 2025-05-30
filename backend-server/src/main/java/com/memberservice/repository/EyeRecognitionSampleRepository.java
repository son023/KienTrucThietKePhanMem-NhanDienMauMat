package com.memberservice.repository;

import com.memberservice.entity.EyeRecognitionSample;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface EyeRecognitionSampleRepository extends JpaRepository<EyeRecognitionSample, UUID> {
    @Query("SELECT ers FROM EyeRecognitionSample ers " +
           "JOIN FETCH ers.member m " +
           "LEFT JOIN FETCH m.fullName " +
           "LEFT JOIN FETCH m.role " +
           "WHERE m.id IN :memberIds AND ers.isActive = true")
    List<EyeRecognitionSample> findByMember_IdInAndIsActiveTrue(@Param("memberIds") List<UUID> memberIds);
} 