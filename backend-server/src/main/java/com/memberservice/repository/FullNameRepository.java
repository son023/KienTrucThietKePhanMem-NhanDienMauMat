package com.memberservice.repository;

import com.memberservice.entity.FullName;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface FullNameRepository extends JpaRepository<FullName, UUID> {
}