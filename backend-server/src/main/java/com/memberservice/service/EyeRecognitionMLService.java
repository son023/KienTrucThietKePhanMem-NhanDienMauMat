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
                                        String modelType,
                                        Integer epochs,
                                        Integer batchSize,
                                        Double learningRate,
                                        Integer imageSize) {
        try {
            String url = eyeRecognitionServiceUrl + "/api/eye-recognition-model/train";

            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("samples", samples);
            requestBody.put("modelName", modelName);
            requestBody.put("modelType", modelType != null ? modelType : "resnet");
            requestBody.put("epochs", epochs);
            requestBody.put("batchSize", batchSize);
            requestBody.put("learningRate", learningRate);
            requestBody.put("imageSize", imageSize);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            ResponseEntity<EyeRecognitionModel> response = restTemplate.postForEntity(
                url, entity, EyeRecognitionModel.class
            );

            EyeRecognitionModel result = response.getBody();

            return result;

        } catch (Exception e) {
            throw new RuntimeException("Lỗi khi gọi ML service: " + e.getMessage(), e);
        }
    }
}