package com.statisticservice.builder;

import com.statisticservice.model.EyeRecognitionModel;
import com.statisticservice.model.RecognitionEvent;
import com.statisticservice.model.StatEyeRecognitionModel;
import java.util.Date;
import java.util.List;

public class ImplStatRecognitionModelBuilder implements StatRecognitionModelBuilder {
    private StatEyeRecognitionModel statModel;

    public ImplStatRecognitionModelBuilder() {
        this.statModel = new StatEyeRecognitionModel();
    }

    @Override
    public StatRecognitionModelBuilder modelStats(EyeRecognitionModel model) {
        statModel.setModel_stats(model);
        return this;
    }

    @Override
    public StatRecognitionModelBuilder dateRange(Date startDate, Date endDate) {
        statModel.setStartDate(startDate);
        statModel.setEndDate(endDate);
        return this;
    }

    @Override
    public StatRecognitionModelBuilder recognitionEvents(List<RecognitionEvent> recognitionEvent) {
        statModel.setRecognitionEvent(recognitionEvent);
        return this;
    }

    @Override
    public StatRecognitionModelBuilder accuracyRate(float rate) {
        statModel.setAccuracyRate(rate);
        return this;
    }

    @Override
    public StatRecognitionModelBuilder falsePositiveRate(float falseRate) {
        statModel.setFalsePositiveRate(falseRate);
        return this;
    }

    @Override
    public StatRecognitionModelBuilder recognitionCounts(int success, int fail) {
        statModel.setSuccess(success);
        statModel.setFail(fail);
        return this;
    }

    @Override
    public StatEyeRecognitionModel build() {
        return this.statModel;
    }
}