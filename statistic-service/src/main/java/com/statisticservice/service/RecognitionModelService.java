package com.statisticservice.service;

import com.statisticservice.model.EyeRecognitionModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;

@Service
public class RecognitionModelService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${services.recognition.url}")
    private String recognitionServiceUrl;


    public EyeRecognitionModel getModelById(int modelId) {
        String url = recognitionServiceUrl + "/api/eye-recognition-model/" + modelId;
        ResponseEntity<EyeRecognitionModel> response = restTemplate.getForEntity(url, EyeRecognitionModel.class);
        return response.getBody();
    }

    public List<EyeRecognitionModel> getAllActiveModels() {
        String url = recognitionServiceUrl + "/api/eye-recognition-model?active_only=true";
        ResponseEntity<EyeRecognitionModel[]> response = restTemplate.getForEntity(url, EyeRecognitionModel[].class);
        return Arrays.asList(response.getBody());
    }
}