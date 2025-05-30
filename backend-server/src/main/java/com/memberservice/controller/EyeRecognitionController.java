package com.memberservice.controller;

import com.memberservice.entity.EyeRecognitionModel;
import com.memberservice.entity.EyeRecognitionSample;
import com.memberservice.entity.EyeRecognitionSampleHistory;
import com.memberservice.entity.Member;
import com.memberservice.service.EyeRecognitionTrainingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/eye-recognition")
public class EyeRecognitionController {

    @Autowired
    private EyeRecognitionTrainingService trainingService;


    @PostMapping("/train-model")
    public ResponseEntity<EyeRecognitionModel> trainModel(@RequestBody Map<String, Object> requestBody) {
        try {
            System.out.println("DEBUG: Request body received: " + requestBody);

            List<String> memberIdStrs = (List<String>) requestBody.get("memberIds");
            if (memberIdStrs == null || memberIdStrs.isEmpty()) {
                throw new RuntimeException("memberIds thiếu trong request body");
            }
            
            List<UUID> memberIds = memberIdStrs.stream()
                    .map(UUID::fromString)
                    .collect(Collectors.toList());
            
            String modelName = (String) requestBody.get("modelName");
            if (modelName == null || modelName.trim().isEmpty()) {
                throw new RuntimeException("modelName không được để trống");
            }
            
            String modelType = (String) requestBody.getOrDefault("modelType", "resnet");
            Integer epochs = (Integer) requestBody.get("epochs");
            Integer batchSize = (Integer) requestBody.get("batchSize");
            Double learningRate = (Double) requestBody.get("learningRate");
            Integer imageSize = (Integer) requestBody.get("imageSize");

            EyeRecognitionModel trainedModel = trainingService.trainModel(
                memberIds, modelName, modelType, epochs, batchSize, learningRate, imageSize
            );
            
            return ResponseEntity.ok(trainedModel);
            
        } catch (Exception e) {
            System.err.println("ERROR in trainModel: " + e.getMessage());
            e.printStackTrace();
            throw new RuntimeException("Lỗi server: " + e.getMessage());
        }
    }

    @PostMapping("/save-trained-model")
    public ResponseEntity<EyeRecognitionModel> saveTrainedModel(@RequestBody EyeRecognitionModel model) {
        try {
            EyeRecognitionModel savedModel = trainingService.saveTrainedModel(model);
            return ResponseEntity.ok(savedModel);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
} 