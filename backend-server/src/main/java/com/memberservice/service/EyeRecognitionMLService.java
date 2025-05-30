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

@Service
public class EyeRecognitionMLService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${eye-recognition.service.url:http://localhost:8000}")
    private String eyeRecognitionServiceUrl;

    public EyeRecognitionModel trainModel(EyeRecognitionModel trainedModel) {
        try {
            String url = eyeRecognitionServiceUrl + "/api/eye-recognition-model/train";

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<EyeRecognitionModel> request = new HttpEntity<>(trainedModel, headers);
            ResponseEntity<EyeRecognitionModel> response = restTemplate.postForEntity(
                url, request, EyeRecognitionModel.class
            );

            EyeRecognitionModel eyeRecognitionModel = response.getBody();

            return eyeRecognitionModel;

        } catch (Exception e) {
            throw new RuntimeException("Lỗi khi gọi ML service: " + e.getMessage(), e);
        }
    }
}