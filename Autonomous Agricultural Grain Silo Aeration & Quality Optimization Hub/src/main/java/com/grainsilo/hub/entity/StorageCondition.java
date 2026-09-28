package com.grainsilo.hub.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import org.springframework.format.annotation.DateTimeFormat;
import java.time.LocalDate;

@Entity
@Table(name = "storage_condition")
public class StorageCondition {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull(message = "Please select a Silo")
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "silo_id", nullable = false)
    private Silo silo;

    @NotNull(message = "Temperature is required")
    @Column(nullable = false)
    private Double temperature;

    @NotNull(message = "Humidity is required")
    @Column(nullable = false)
    private Double humidity;

    @NotNull(message = "Recorded date is required")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    @Column(nullable = false)
    private LocalDate recordedDate;

    public StorageCondition() {
    }

    public StorageCondition(Silo silo, Double temperature, Double humidity, LocalDate recordedDate) {
        this.silo = silo;
        this.temperature = temperature;
        this.humidity = humidity;
        this.recordedDate = recordedDate;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Silo getSilo() { return silo; }
    public void setSilo(Silo silo) { this.silo = silo; }
    public Double getTemperature() { return temperature; }
    public void setTemperature(Double temperature) { this.temperature = temperature; }
    public Double getHumidity() { return humidity; }
    public void setHumidity(Double humidity) { this.humidity = humidity; }
    public LocalDate getRecordedDate() { return recordedDate; }
    public void setRecordedDate(LocalDate recordedDate) { this.recordedDate = recordedDate; }

    public String getConditionStatus() {
        if (temperature == null || humidity == null) {
            return "UNKNOWN";
        }
        if (temperature > 25.0 || humidity > 65.0) {
            return "ATTENTION";
        }
        return "NORMAL";
    }

    public String getStatusBadgeClass() {
        String status = getConditionStatus();
        if ("ATTENTION".equals(status)) {
            return "badge bg-danger";
        } else if ("NORMAL".equals(status)) {
            return "badge bg-success";
        }
        return "badge bg-secondary";
    }
}