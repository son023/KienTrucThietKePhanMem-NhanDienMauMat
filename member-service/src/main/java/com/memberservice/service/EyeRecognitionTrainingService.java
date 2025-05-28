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
    
    // CHỈ TRAIN model, KHÔNG save vào database
    public EyeRecognitionModel trainModelOnly(List<UUID> memberIds,
                                             String modelName,
                                             Integer epochs,
                                             Integer batchSize,
                                             Double learningRate,
                                             Integer imageSize) {
        try {
            // 1. Lấy samples từ database với eager loading
            List<EyeRecognitionSample> samples = sampleRepository.findByMember_IdInAndIsActiveTrueWithMember(memberIds);
            
            if (samples.isEmpty()) {
                throw new RuntimeException("Không tìm thấy mẫu mắt cho các member IDs đã chọn");
            }
            
            // 2. Gọi ML service để train
            EyeRecognitionModel trainedModel = mlService.trainModel(
                samples, modelName, epochs, batchSize, learningRate, imageSize
            );
            
            if (trainedModel == null) {
                throw new RuntimeException("ML service trả về null");
            }
            
            // CHỈ trả về model đã train, KHÔNG save vào DB
            return trainedModel;
            
        } catch (Exception e) {
            throw new RuntimeException("Lỗi trong quá trình training: " + e.getMessage(), e);
        }
    }

    // SAVE model vào database sau khi user confirm
    @Transactional
    public EyeRecognitionModel saveTrainedModel(EyeRecognitionModel trainedModel) {
        try {
            System.out.println("=== SAVE TRAINED MODEL START ===");
            System.out.println("Model ID: " + trainedModel.getId());
            System.out.println("Model Name: " + trainedModel.getEyeModelName());
            
            // Set metadata
            trainedModel.setCreateDate(LocalDateTime.now());
            trainedModel.setIsActive(true);
            
            // Lưu histories tạm trước khi clear
            List<EyeRecognitionSampleHistory> historiesToSave = trainedModel.getHistories();
            System.out.println("Histories từ ML service: " + (historiesToSave != null ? historiesToSave.size() : "null"));

            
            // Lưu model trước (không bao gồm histories)
            trainedModel.setHistories(null);
            EyeRecognitionModel savedModel = modelRepository.save(trainedModel);
            System.out.println("Model saved với ID: " + savedModel.getId());
            
            // Lưu histories riêng nếu có
            if (historiesToSave != null && !historiesToSave.isEmpty()) {
                System.out.println("Bắt đầu lưu " + historiesToSave.size() + " histories...");
                int savedCount = 0;
                
                for (EyeRecognitionSampleHistory history : historiesToSave) {
                    try {
                        // Chỉ lưu nếu có sample
                        if (history.getEyeRecognitionSample() != null && history.getEyeRecognitionSample().getId() != null) {
                            // Tạo history mới và set relationships
                            EyeRecognitionSampleHistory newHistory = new EyeRecognitionSampleHistory();
                            newHistory.setModel(savedModel);  // Set model relationship
                            newHistory.setEyeRecognitionSample(history.getEyeRecognitionSample());  // Set sample relationship
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
    
    // Helper method để lấy members có đủ samples
    public List<Member> getMembersWithMinSamples(int minSamples) {
        List<UUID> memberIds = sampleRepository.findMemberIdsWithMinimumSamples(minSamples);
        return memberRepository.findAllById(memberIds);
    }
} 