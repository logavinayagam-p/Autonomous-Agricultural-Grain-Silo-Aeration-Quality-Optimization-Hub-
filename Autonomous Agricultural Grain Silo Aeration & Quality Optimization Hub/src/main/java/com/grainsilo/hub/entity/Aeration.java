package com.grainsilo.hub.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.springframework.format.annotation.DateTimeFormat;
import java.time.LocalDate;

@Entity
@Table(name = "aeration")
public class Aeration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull(message = "Please select a Silo")
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "silo_id", nullable = false)
    private Silo silo;

    @NotNull(message = "Aeration date is required")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    @Column(nullable = false)
    private LocalDate aerationDate;

    @NotBlank(message = "Fan Status is required (ON / OFF)")
    @Column(nullable = false, length = 10)
    private String fanStatus;

    @NotNull(message = "Duration is required (in hours)")
    @DecimalMin(value = "0.1", message = "Duration must be at least 0.1 hours")
    @Column(nullable = false)
    private Double duration;

    @Column(length = 255)
    private String remarks;

    public Aeration() {
    }

    public Aeration(Silo silo, LocalDate aerationDate, String fanStatus, Double duration, String remarks) {
        this.silo = silo;
        this.aerationDate = aerationDate;
        this.fanStatus = fanStatus;
        this.duration = duration;
        this.remarks = remarks;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Silo getSilo() { return silo; }
    public void setSilo(Silo silo) { this.silo = silo; }
    public LocalDate getAerationDate() { return aerationDate; }
    public void setAerationDate(LocalDate aerationDate) { this.aerationDate = aerationDate; }
    public String getFanStatus() { return fanStatus; }
    public void setFanStatus(String fanStatus) { this.fanStatus = fanStatus; }
    public Double getDuration() { return duration; }
    public void setDuration(Double duration) { this.duration = duration; }
    public String getRemarks() { return remarks; }
    public void setRemarks(String remarks) { this.remarks = remarks; }
}