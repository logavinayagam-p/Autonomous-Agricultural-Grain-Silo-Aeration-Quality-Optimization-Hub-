package com.grainsilo.hub.repository;

import com.grainsilo.hub.entity.StorageCondition;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface StorageConditionRepository extends JpaRepository<StorageCondition, Long> {
    List<StorageCondition> findAllByOrderByRecordedDateDesc();
    List<StorageCondition> findBySiloId(Long siloId);
}