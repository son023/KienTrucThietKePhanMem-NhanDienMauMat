package com.memberservice.repository;

import com.memberservice.entity.Member;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface MemberRepository extends JpaRepository<Member, UUID> {
    Optional<Member> findByUsername(String username);

    @Query("SELECT DISTINCT m FROM Member m " +
            "WHERE m.id IN (" +
            "    SELECT ers.member.id FROM EyeRecognitionSample ers " +
            "    GROUP BY ers.member.id " +
            "    HAVING COUNT(ers) >= :minSamples" +
            ")")
    List<Member> findMembersWithMinimumSamples(@Param("minSamples") int minSamples);
}