package com.statisticservice.service;

import com.statisticservice.builder.ImplStatRecognitionModelBuilder;
import com.statisticservice.model.EyeRecognitionModel;
import com.statisticservice.model.RecognitionEvent;
import com.statisticservice.model.StatEyeRecognitionModel;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Slf4j
@Service
public class StatisticsService {

    @Autowired
    private RecognitionModelService modelService;

    @Autowired
    private UserService userService;


    public StatEyeRecognitionModel getModelStatistics(int modelId, Date startDate, Date endDate) {
        EyeRecognitionModel model = modelService.getModelById(modelId);
        if (model == null) {
            throw new RuntimeException("Không tìm thấy mô hình với ID: " + modelId);
        }
        log.error("fer");

        List<RecognitionEvent> events = userService.getEventsByModelId(modelId, startDate, endDate);

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

    public List<StatEyeRecognitionModel> getAllModelStatistics(Date startDate, Date endDate, String sortBy) {
        List<EyeRecognitionModel> allModels = modelService.getAllActiveModels();
        List<Integer> modelIds = allModels.stream()
                .map(EyeRecognitionModel::getId)
                .toList();

        List<StatEyeRecognitionModel> results = new ArrayList<>();

        for (Integer modelId : modelIds) {
            try {
                StatEyeRecognitionModel stats = getModelStatistics(modelId, startDate, endDate);
                results.add(stats);
            } catch (Exception e) {
                System.err.println("Error getting statistics for model ID " + modelId + ": " + e.getMessage());
            }
        }

        sortModelStats(results, sortBy);

        return results;
    }


    private void sortModelStats(List<StatEyeRecognitionModel> modelStats, String sortBy) {
        switch (sortBy.toLowerCase()) {
            case "success":
                modelStats.sort((a, b) -> Integer.compare(b.getSuccess(), a.getSuccess())); // Sắp xếp giảm dần
                break;
            case "accuracy":
            case "accuracyrate":
                modelStats.sort((a, b) -> Float.compare(b.getAccuracyRate(), a.getAccuracyRate())); // Sắp xếp giảm dần
                break;
            default:
                modelStats.sort((a, b) -> Integer.compare(b.getSuccess(), a.getSuccess())); // Mặc định sắp xếp theo success
                break;
        }
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