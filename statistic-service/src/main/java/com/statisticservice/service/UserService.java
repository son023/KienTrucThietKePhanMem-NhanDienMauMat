package com.statisticservice.service;

import com.statisticservice.model.RecognitionEvent;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.List;

@Service
public class UserService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${services.user.url}")
    private String userServiceUrl;

    public List<RecognitionEvent> getEventsByModelId(int modelId, Date startDate, Date endDate) {
        // Chuyển đổi Date sang LocalDate theo định dạng ISO
        LocalDate start = startDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
        LocalDate end = endDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();

        // Sử dụng ISO format YYYY-MM-DD cho LocalDate
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE;

        String url = UriComponentsBuilder.fromHttpUrl(userServiceUrl + "/api/recognition-events")
                .queryParam("model_id", modelId)
                .queryParam("start_date", start.format(formatter))
                .queryParam("end_date", end.format(formatter))
                .build().toUriString();

        ResponseEntity<List<RecognitionEvent>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<List<RecognitionEvent>>() {}
        );

        return response.getBody();
    }

}