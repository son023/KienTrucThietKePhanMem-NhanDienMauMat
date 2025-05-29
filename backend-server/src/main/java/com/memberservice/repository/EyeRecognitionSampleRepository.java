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
    
    List<EyeRecognitionSample> findByMember_IdAndIsActiveTrue(UUID memberId);
    
    // Eager load Member with all relationships để tránh lazy loading issues
    @Query("SELECT ers FROM EyeRecognitionSample ers " +
           "JOIN FETCH ers.member m " +
           "LEFT JOIN FETCH m.fullName " +
           "LEFT JOIN FETCH m.role " +
           "WHERE m.id IN :memberIds AND ers.isActive = true")
    List<EyeRecognitionSample> findByMember_IdInAndIsActiveTrueWithMember(@Param("memberIds") List<UUID> memberIds);
    
    @Query("SELECT COUNT(ers) FROM EyeRecognitionSample ers WHERE ers.member.id = :memberId AND ers.isActive = true")
    Long countByMemberIdAndIsActiveTrue(@Param("memberId") UUID memberId);
    
    @Query("SELECT DISTINCT ers.member.id FROM EyeRecognitionSample ers WHERE ers.isActive = true GROUP BY ers.member.id HAVING COUNT(ers) >= :minSamples")
    List<UUID> findMemberIdsWithMinimumSamples(@Param("minSamples") int minSamples);
} 