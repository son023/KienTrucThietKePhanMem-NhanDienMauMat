package com.memberservice.service;

import com.memberservice.entity.RecognitionEvent;
import com.memberservice.repository.RecognitionEventRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.*;

@Service
public class RecognitionEventService {

    private final RecognitionEventRepository recognitionEventRepository;

    @Autowired
    public RecognitionEventService(RecognitionEventRepository recognitionEventRepository) {
        this.recognitionEventRepository = recognitionEventRepository;
    }

    public List<RecognitionEvent> getAllEvents() {
        return recognitionEventRepository.findAll();
    }

    public List<RecognitionEvent> getEventsByModelIdAndTimeRange(
            Integer modelId, LocalDateTime startDate, LocalDateTime endDate) {
        return recognitionEventRepository.findByRecognitionModelIdAndTimeVerifyBetween(
                modelId, startDate, endDate);
    }

    public List<RecognitionEvent> getEventsByTimeRange(LocalDateTime startDate, LocalDateTime endDate) {
        return recognitionEventRepository.findByTimeVerifyBetween(startDate, endDate);
    }
}