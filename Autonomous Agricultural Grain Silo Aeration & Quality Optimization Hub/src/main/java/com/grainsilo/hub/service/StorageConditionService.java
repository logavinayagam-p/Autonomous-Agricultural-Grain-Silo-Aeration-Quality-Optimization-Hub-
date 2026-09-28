package com.grainsilo.hub.service;

import com.grainsilo.hub.entity.StorageCondition;
import com.grainsilo.hub.repository.StorageConditionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class StorageConditionService {

    private final StorageConditionRepository conditionRepository;

    @Autowired
    public StorageConditionService(StorageConditionRepository conditionRepository) {
        this.conditionRepository = conditionRepository;
    }

    public List<StorageCondition> getAllConditions() {
        return conditionRepository.findAllByOrderByRecordedDateDesc();
    }

    public Optional<StorageCondition> getConditionById(Long id) {
        return conditionRepository.findById(id);
    }

    public StorageCondition saveCondition(StorageCondition condition) {
        return conditionRepository.save(condition);
    }

    public void deleteCondition(Long id) {
        conditionRepository.deleteById(id);
    }

    public long countConditions() {
        return conditionRepository.count();
    }

    public List<StorageCondition> getConditionsBySilo(Long siloId) {
        return conditionRepository.findBySiloId(siloId);
    }
}