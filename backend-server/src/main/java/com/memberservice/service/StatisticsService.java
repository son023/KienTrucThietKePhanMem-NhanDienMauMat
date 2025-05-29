package com.memberservice.service;

import com.memberservice.entity.EyeRecognitionModel;
import com.memberservice.entity.RecognitionEvent;
import com.memberservice.repository.EyeRecognitionModelRepository;
import com.memberservice.repository.RecognitionEventRepository;
import com.memberservice.builder.ImplStatRecognitionModelBuilder;
import com.memberservice.entity.StatEyeRecognitionModel;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.*;

@Slf4j
@Service
public class StatisticsService {

    @Autowired
    private EyeRecognitionModelRepository modelRepository;

    @Autowired
    private RecognitionEventRepository eventRepository;

    public StatEyeRecognitionModel getModelStatistics(UUID modelId, Date startDate, Date endDate) {
        Optional<EyeRecognitionModel> modelOpt = modelRepository.findById(modelId);
        if (modelOpt.isEmpty()) {
            throw new RuntimeException("Không tìm thấy mô hình với ID: " + modelId);
        }

        EyeRecognitionModel model = modelOpt.get();

        LocalDateTime startDateTime = startDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime();
        LocalDateTime endDateTime = endDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime();

        List<RecognitionEvent> events = eventRepository.findByRecognitionModelIdAndTimeVerifyBetween(
                modelId, startDateTime, endDateTime);

        int totalRecognitions = events.size();
        int successCount = (int) events.stream().filter(RecognitionEvent::getIsSuccessful).count();
        int failCount = totalRecognitions - successCount;

        float accuracyRate = totalRecognitions > 0 ? (float) successCount / totalRecognitions : 0;
        float falsePositiveRate = calculateFalsePositiveRate(events);

        StatEyeRecognitionModel statEyeRecognitionModel = new ImplStatRecognitionModelBuilder()
                .modelStats(model)
                .dateRange(startDate, endDate)
                .recognitionEvents(events)
                .recognitionCounts(successCount, failCount)
                .accuracyRate(accuracyRate)
                .falsePositiveRate(falsePositiveRate)
                .build();

        return statEyeRecognitionModel;
    }

    public List<StatEyeRecognitionModel> getAllModelStatistics(Date startDate, Date endDate) {
        List<EyeRecognitionModel> allModels = modelRepository.findByIsActiveTrueOrderByCreateDateDesc();
        List<UUID> modelIds = allModels.stream()
                .map(EyeRecognitionModel::getId)
                .toList();

        List<StatEyeRecognitionModel> results = new ArrayList<>();

        for (UUID modelId : modelIds) {
            try {
                StatEyeRecognitionModel stats = getModelStatistics(modelId, startDate, endDate);
                results.add(stats);
            } catch (Exception e) {
                System.err.println("Error getting statistics for model ID " + modelId + ": " + e.getMessage());
            }
        }

        results.sort((a, b) -> Integer.compare(b.getSuccess(), a.getSuccess()));

        return results;
    }

    private float calculateFalsePositiveRate(List<RecognitionEvent> events) {
        if (events == null || events.isEmpty()) {
            return 0;
        }

        long falsePositiveCount = events.stream()
                .filter(event -> !event.getIsSuccessful() && event.getAccuracy() > 0.5)
                .count();

        return events.size() > 0 ? (float) falsePositiveCount / events.size() : 0;
    }
} 