package com.memberservice.service;

import com.memberservice.entity.EyeRecognitionModel;
import com.memberservice.entity.EyeRecognitionSample;
import com.memberservice.entity.EyeRecognitionSampleHistory;
import com.memberservice.entity.Member;
import com.memberservice.repository.EyeRecognitionModelRepository;
import com.memberservice.repository.EyeRecognitionSampleRepository;
import com.memberservice.repository.EyeRecognitionSampleHistoryRepository;
import com.memberservice.repository.MemberRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class EyeRecognitionTrainingService {
    
    @Autowired
    private EyeRecognitionMLService mlService;
    
    @Autowired
    private EyeRecognitionModelRepository modelRepository;
    
    @Autowired
    private EyeRecognitionSampleRepository sampleRepository;
    
    @Autowired
    private EyeRecognitionSampleHistoryRepository historyRepository;
    
    @Autowired
    private MemberRepository memberRepository;

    public EyeRecognitionModel trainModelOnly(List<UUID> memberIds,
                                             String modelName,
                                             Integer epochs,
                                             Integer batchSize,
                                             Double learningRate,
                                             Integer imageSize) {
        try {
            List<EyeRecognitionSample> samples = sampleRepository.findByMember_IdInAndIsActiveTrueWithMember(memberIds);
            
            if (samples.isEmpty()) {
                throw new RuntimeException("Không tìm thấy mẫu mắt cho các member IDs đã chọn");
            }

            EyeRecognitionModel trainedModel = mlService.trainModel(
                samples, modelName, epochs, batchSize, learningRate, imageSize
            );
            
            if (trainedModel == null) {
                throw new RuntimeException("ML service trả về null");
            }

            return trainedModel;
            
        } catch (Exception e) {
            throw new RuntimeException("Lỗi trong quá trình training: " + e.getMessage(), e);
        }
    }

    @Transactional
    public EyeRecognitionModel saveTrainedModel(EyeRecognitionModel trainedModel) {
        try {
            trainedModel.setIsActive(true);

            List<EyeRecognitionSampleHistory> historiesToSave = trainedModel.getHistories();

            trainedModel.setHistories(null);
            EyeRecognitionModel savedModel = modelRepository.save(trainedModel);

            if (historiesToSave != null && !historiesToSave.isEmpty()) {
                System.out.println("Bắt đầu lưu " + historiesToSave.size() + " histories...");
                int savedCount = 0;
                
                for (EyeRecognitionSampleHistory history : historiesToSave) {
                    try {
                        if (history.getEyeRecognitionSample() != null && history.getEyeRecognitionSample().getId() != null) {
                            EyeRecognitionSampleHistory newHistory = new EyeRecognitionSampleHistory();
                            newHistory.setModel(savedModel);
                            newHistory.setEyeRecognitionSample(history.getEyeRecognitionSample());
                            newHistory.setNotes(history.getNotes() != null ? history.getNotes() : "");

                            historyRepository.save(newHistory);
                            savedCount++;
                        } else {
                            System.out.println("SKIP history vì sample null hoặc sample.id null");
                        }
                        
                    } catch (Exception e) {
                        System.out.println("Lỗi lưu history: " + e.getMessage());
                        e.printStackTrace();
                    }
                }
                
                System.out.println("Đã lưu " + savedCount + "/" + historiesToSave.size() + " histories");
            } else {
                System.out.println("Không có histories để lưu!");
            }
            
            System.out.println("=== SAVE TRAINED MODEL COMPLETED ===");
            return savedModel;
            
        } catch (Exception e) {
            System.out.println("=== SAVE TRAINED MODEL ERROR ===");
            e.printStackTrace();
            throw new RuntimeException("Lỗi khi lưu model: " + e.getMessage(), e);
        }
    }
    public List<Member> getMembersWithMinSamples(int minSamples) {
        List<UUID> memberIds = sampleRepository.findMemberIdsWithMinimumSamples(minSamples);
        return memberRepository.findAllById(memberIds);
    }
} 