package com.grainsilo.hub.repository;

import com.grainsilo.hub.entity.Aeration;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface AerationRepository extends JpaRepository<Aeration, Long> {
    List<Aeration> findAllByOrderByAerationDateDesc();
    List<Aeration> findBySiloId(Long siloId);
}