package com.memberservice.controller;

import com.memberservice.entity.RecognitionEvent;
import com.memberservice.service.RecognitionEventService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/recognition-events")

    public class RecognitionEventController {

    private final RecognitionEventService recognitionEventService;

    @Autowired
    public RecognitionEventController(RecognitionEventService recognitionEventService) {
        this.recognitionEventService = recognitionEventService;
    }

    @GetMapping
    public ResponseEntity<List<RecognitionEvent>> getAllEventsByModelId(
            @RequestParam(required = false) Integer model_id,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate start_date,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate end_date) {

        LocalDateTime startDateTime = start_date != null ? start_date.atStartOfDay() : null;
        LocalDateTime endDateTime = end_date != null ? end_date.atTime(23, 59, 59) : null;

        if (model_id != null && startDateTime != null && endDateTime != null) {
            return ResponseEntity.ok(
                    recognitionEventService.getEventsByModelIdAndTimeRange(model_id, startDateTime, endDateTime)
            );
        } else if (startDateTime != null && endDateTime != null) {
            return ResponseEntity.ok(
                    recognitionEventService.getEventsByTimeRange(startDateTime, endDateTime)
            );
        } else {
            return ResponseEntity.ok(recognitionEventService.getAllEvents());
        }
    }
}