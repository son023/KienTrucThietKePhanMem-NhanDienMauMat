package com.memberservice.service;

import com.memberservice.entity.EyeRecognitionModel;
import com.memberservice.entity.EyeRecognitionSample;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class EyeRecognitionMLService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${eye-recognition.service.url:http://localhost:8000}")
    private String eyeRecognitionServiceUrl;

    public EyeRecognitionModel trainModel(List<EyeRecognitionSample> samples,
                                        String modelName,
                                        Integer epochs,
                                        Integer batchSize,
                                        Double learningRate,
                                        Integer imageSize) {
        try {
            String url = eyeRecognitionServiceUrl + "/api/eye-recognition-model/train";

            // Tạo request body đơn giản
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("samples", samples);  // Gửi thẳng samples
            requestBody.put("modelName", modelName);
            requestBody.put("epochs", epochs);
            requestBody.put("batchSize", batchSize);
            requestBody.put("learningRate", learningRate);
            requestBody.put("imageSize", imageSize);

            System.out.println("DEBUG ML Service Request:");
            System.out.println("  URL: " + url);
            System.out.println("  Samples count: " + samples.size());
            System.out.println("  Request body keys: " + requestBody.keySet());

            // Set headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            // Gọi ML service
            ResponseEntity<EyeRecognitionModel> response = restTemplate.postForEntity(
                url, entity, EyeRecognitionModel.class
            );

            EyeRecognitionModel result = response.getBody();
            
            // Debug response
            System.out.println("DEBUG ML Service Response:");
            if (result != null) {
                System.out.println("  Model ID: " + result.getId());
                System.out.println("  Model Name: " + result.getEyeModelName());
                System.out.println("  Accuracy: " + result.getAccuracy());
                System.out.println("  Histories count: " + (result.getHistories() != null ? result.getHistories().size() : "null"));
                
                if (result.getHistories() != null && !result.getHistories().isEmpty()) {
                    System.out.println("  First history notes: " + result.getHistories().get(0).getNotes());
                }
            } else {
                System.out.println("  Response body is null!");
            }

            return result;

        } catch (Exception e) {
            throw new RuntimeException("Lỗi khi gọi ML service: " + e.getMessage(), e);
        }
    }
}