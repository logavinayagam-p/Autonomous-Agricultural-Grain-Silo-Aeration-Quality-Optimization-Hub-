package com.grainsilo.hub.service;

import com.grainsilo.hub.entity.Aeration;
import com.grainsilo.hub.repository.AerationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class AerationService {

    private final AerationRepository aerationRepository;

    @Autowired
    public AerationService(AerationRepository aerationRepository) {
        this.aerationRepository = aerationRepository;
    }

    public List<Aeration> getAllAerations() {
        return aerationRepository.findAllByOrderByAerationDateDesc();
    }

    public Optional<Aeration> getAerationById(Long id) {
        return aerationRepository.findById(id);
    }

    public Aeration saveAeration(Aeration aeration) {
        return aerationRepository.save(aeration);
    }

    public void deleteAeration(Long id) {
        aerationRepository.deleteById(id);
    }

    public long countAerations() {
        return aerationRepository.count();
    }

    public List<Aeration> getAerationsBySilo(Long siloId) {
        return aerationRepository.findBySiloId(siloId);
    }
}