package com.grainsilo.hub.service;

import com.grainsilo.hub.entity.Silo;
import com.grainsilo.hub.repository.SiloRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class SiloService {

    private final SiloRepository siloRepository;

    @Autowired
    public SiloService(SiloRepository siloRepository) {
        this.siloRepository = siloRepository;
    }

    public List<Silo> getAllSilos() {
        return siloRepository.findAllByOrderByIdDesc();
    }

    public Optional<Silo> getSiloById(Long id) {
        return siloRepository.findById(id);
    }

    public Silo saveSilo(Silo silo) {
        if (silo.getStoredQuantity() != null && silo.getStorageCapacity() != null) {
            if (silo.getStoredQuantity() > silo.getStorageCapacity()) {
                throw new IllegalArgumentException("Stored quantity (" + silo.getStoredQuantity() 
                        + " tons) cannot exceed total storage capacity (" + silo.getStorageCapacity() + " tons).");
            }
        }
        return siloRepository.save(silo);
    }

    public void deleteSilo(Long id) {
        siloRepository.deleteById(id);
    }

    public long countSilos() {
        return siloRepository.count();
    }

    public List<Silo> getRecentSilos(int limit) {
        return siloRepository.findAllByOrderByIdDesc().stream().limit(limit).toList();
    }
}