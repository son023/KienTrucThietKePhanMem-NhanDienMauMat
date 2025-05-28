package com.memberservice.controller;

import com.memberservice.entity.EyeRecognitionModel;
import com.memberservice.entity.EyeRecognitionSample;
import com.memberservice.entity.EyeRecognitionSampleHistory;
import com.memberservice.entity.Member;
import com.memberservice.repository.EyeRecognitionModelRepository;
import com.memberservice.repository.EyeRecognitionSampleRepository;
import com.memberservice.repository.EyeRecognitionSampleHistoryRepository;
import com.memberservice.repository.MemberRepository;
import com.memberservice.service.EyeRecognitionTrainingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/eye-recognition")
public class EyeRecognitionController {

    @Autowired
    private EyeRecognitionModelRepository modelRepository;

    @Autowired
    private EyeRecognitionSampleRepository sampleRepository;

    @Autowired
    private EyeRecognitionSampleHistoryRepository historyRepository;

    @Autowired
    private MemberRepository memberRepository;

    @Autowired
    private EyeRecognitionTrainingService trainingService;

    // TEST endpoint để debug
    @PostMapping("/test-request")
    public ResponseEntity<?> testRequest(@RequestBody Map<String, Object> requestBody) {
        System.out.println("TEST: Request body type and content: " + requestBody.getClass() + " = " + requestBody);
        
        for (Map.Entry<String, Object> entry : requestBody.entrySet()) {
            System.out.println("  " + entry.getKey() + " (" + entry.getValue().getClass() + ") = " + entry.getValue());
        }
        
        return ResponseEntity.ok("Request received successfully");
    }

    // Train model ONLY - không save vào DB
    @PostMapping("/train-model")
    public ResponseEntity<?> trainModel(@RequestBody Map<String, Object> requestBody) {
        try {
            System.out.println("DEBUG: Request body received: " + requestBody);
            
            // Parse request parameters
            @SuppressWarnings("unchecked")
            List<String> memberIdStrs = (List<String>) requestBody.get("memberIds");
            if (memberIdStrs == null || memberIdStrs.isEmpty()) {
                return ResponseEntity.badRequest().body("memberIds không được để trống");
            }
            
            List<UUID> memberIds = memberIdStrs.stream()
                    .map(UUID::fromString)
                    .collect(Collectors.toList());
            
            String modelName = (String) requestBody.get("modelName");
            if (modelName == null || modelName.trim().isEmpty()) {
                return ResponseEntity.badRequest().body("modelName không được để trống");
            }
            
            Integer epochs = (Integer) requestBody.get("epochs");
            Integer batchSize = (Integer) requestBody.get("batchSize");
            Double learningRate = (Double) requestBody.get("learningRate");
            Integer imageSize = (Integer) requestBody.get("imageSize");
            
            System.out.println("DEBUG: Parsed parameters - memberIds: " + memberIds.size() + 
                             ", modelName: " + modelName + ", epochs: " + epochs);
            
            // CHỈ TRAIN, KHÔNG SAVE
            EyeRecognitionModel trainedModel = trainingService.trainModelOnly(
                memberIds, modelName, epochs, batchSize, learningRate, imageSize
            );
            
            return ResponseEntity.ok(trainedModel);
            
        } catch (Exception e) {
            System.err.println("ERROR in trainModel: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.badRequest().body("Lỗi server: " + e.getMessage());
        }
    }

    // Lấy members có ít nhất minSamples mẫu mắt
    @GetMapping("/members-with-samples")
    public ResponseEntity<List<Member>> getMembersWithMinSamples(@RequestParam int minSamples) {
        List<Member> members = trainingService.getMembersWithMinSamples(2);
        return ResponseEntity.ok(members);
    }

    // REMOVED: Endpoint này thừa, member-service tự lấy samples

    // Lưu model đã train kèm history (sau khi user confirm)
    @PostMapping("/save-trained-model")
    public ResponseEntity<EyeRecognitionModel> saveTrainedModel(@RequestBody EyeRecognitionModel model) {
        try {
            EyeRecognitionModel savedModel = trainingService.saveTrainedModel(model);
            return ResponseEntity.ok(savedModel);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // Lấy tất cả models
    @GetMapping("/models")
    public ResponseEntity<List<EyeRecognitionModel>> getAllModels(@RequestParam(defaultValue = "true") boolean activeOnly) {
        List<EyeRecognitionModel> models;
        if (activeOnly) {
            models = modelRepository.findByIsActiveTrueOrderByCreateDateDesc();
        } else {
            models = modelRepository.findAllByOrderByCreateDateDesc();
        }
        return ResponseEntity.ok(models);
    }

    // Lấy model theo ID
    @GetMapping("/models/{modelId}")
    public ResponseEntity<EyeRecognitionModel> getModelById(@PathVariable UUID modelId) {
        return modelRepository.findById(modelId)
                .map(model -> ResponseEntity.ok(model))
                .orElse(ResponseEntity.notFound().build());
    }

    // Lấy model theo ID kèm histories và samples
    @GetMapping("/models/{modelId}/with-histories")
    public ResponseEntity<EyeRecognitionModel> getModelWithHistories(@PathVariable UUID modelId) {
        return modelRepository.findByIdWithHistories(modelId)
                .map(model -> ResponseEntity.ok(model))
                .orElse(ResponseEntity.notFound().build());
    }

    // Lấy history của model
    @GetMapping("/models/{modelId}/history")
    public ResponseEntity<List<EyeRecognitionSampleHistory>> getModelHistory(@PathVariable UUID modelId) {
        List<EyeRecognitionSampleHistory> history = historyRepository.findByModelId(modelId);
        return ResponseEntity.ok(history);
    }
} 