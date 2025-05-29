package com.memberservice.builder;

import com.memberservice.entity.EyeRecognitionModel;
import com.memberservice.entity.RecognitionEvent;
import com.memberservice.entity.StatEyeRecognitionModel;

import java.util.Date;
import java.util.List;

public interface StatRecognitionModelBuilder {
    StatRecognitionModelBuilder modelStats(EyeRecognitionModel model);
    StatRecognitionModelBuilder dateRange(Date startDate, Date endDate);
    StatRecognitionModelBuilder recognitionEvents(List<RecognitionEvent> recognitionEvent);
    StatRecognitionModelBuilder accuracyRate(float rate);
    StatRecognitionModelBuilder falsePositiveRate(float falseRate);
    StatRecognitionModelBuilder recognitionCounts(int success, int fail);
    StatEyeRecognitionModel build();
} 