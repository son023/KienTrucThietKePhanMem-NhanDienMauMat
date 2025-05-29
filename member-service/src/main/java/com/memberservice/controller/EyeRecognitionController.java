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
    private EyeRecognitionTrainingService trainingService;


    @PostMapping("/train-model")
    public ResponseEntity<?> trainModel(@RequestBody Map<String, Object> requestBody) {
        try {
            System.out.println("DEBUG: Request body received: " + requestBody);

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

    @GetMapping("/members-with-samples")
    public ResponseEntity<List<Member>> getMembersWithMinSamples(@RequestParam int minSamples) {
        List<Member> members = trainingService.getMembersWithMinSamples(2);
        return ResponseEntity.ok(members);
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