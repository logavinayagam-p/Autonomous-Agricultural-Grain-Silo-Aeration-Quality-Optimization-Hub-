package com.grainsilo.hub.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "silo")
public class Silo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Silo Name is required")
    @Column(nullable = false, length = 100)
    private String siloName;

    @NotBlank(message = "Location is required")
    @Column(nullable = false, length = 100)
    private String location;

    @NotBlank(message = "Grain Type is required (e.g., Wheat, Corn, Barley, Paddy)")
    @Column(nullable = false, length = 50)
    private String grainType;

    @NotNull(message = "Storage Capacity is required")
    @DecimalMin(value = "0.1", message = "Capacity must be greater than 0")
    @Column(nullable = false)
    private Double storageCapacity;

    @NotNull(message = "Stored Quantity is required")
    @DecimalMin(value = "0.0", message = "Stored quantity cannot be negative")
    @Column(nullable = false)
    private Double storedQuantity;

    @OneToMany(mappedBy = "silo", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<StorageCondition> storageConditions = new ArrayList<>();

    @OneToMany(mappedBy = "silo", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Aeration> aerations = new ArrayList<>();

    public Silo() {
    }

    public Silo(String siloName, String location, String grainType, Double storageCapacity, Double storedQuantity) {
        this.siloName = siloName;
        this.location = location;
        this.grainType = grainType;
        this.storageCapacity = storageCapacity;
        this.storedQuantity = storedQuantity;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getSiloName() { return siloName; }
    public void setSiloName(String siloName) { this.siloName = siloName; }
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    public String getGrainType() { return grainType; }
    public void setGrainType(String grainType) { this.grainType = grainType; }
    public Double getStorageCapacity() { return storageCapacity; }
    public void setStorageCapacity(Double storageCapacity) { this.storageCapacity = storageCapacity; }
    public Double getStoredQuantity() { return storedQuantity; }
    public void setStoredQuantity(Double storedQuantity) { this.storedQuantity = storedQuantity; }
    public List<StorageCondition> getStorageConditions() { return storageConditions; }
    public void setStorageConditions(List<StorageCondition> storageConditions) { this.storageConditions = storageConditions; }
    public List<Aeration> getAerations() { return aerations; }
    public void setAerations(List<Aeration> aerations) { this.aerations = aerations; }

    public double getUtilizationPercentage() {
        if (storageCapacity == null || storageCapacity == 0.0 || storedQuantity == null) {
            return 0.0;
        }
        double percentage = (storedQuantity / storageCapacity) * 100;
        return Math.round(percentage * 10.0) / 10.0;
    }
}