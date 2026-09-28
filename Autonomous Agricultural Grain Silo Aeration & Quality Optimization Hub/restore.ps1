# PowerShell Restoration Script for Autonomous Grain Silo Hub

$pomContent = @'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.5</version>
        <relativePath/>
    </parent>
    
    <groupId>com.grainsilo</groupId>
    <artifactId>grain-silo-hub</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>grain-silo-hub</name>
    <description>Autonomous Agricultural Grain Silo Aeration and Quality Optimization Hub</description>
    
    <properties>
        <java.version>17</java.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\pom.xml", $pomContent, (New-Object System.Text.UTF8Encoding($false)))

$appJava = @'
package com.grainsilo.hub;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class GrainSiloApplication {

    public static void main(String[] args) {
        SpringApplication.run(GrainSiloApplication.class, args);
        System.out.println("==================================================================");
        System.out.println("Grain Silo Hub Application started successfully at http://localhost:8080");
        System.out.println("==================================================================");
    }
}
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\GrainSiloApplication.java", $appJava, (New-Object System.Text.UTF8Encoding($false)))

$siloJava = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\entity\Silo.java", $siloJava, (New-Object System.Text.UTF8Encoding($false)))

$condJava = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\entity\StorageCondition.java", $condJava, (New-Object System.Text.UTF8Encoding($false)))

$aerationJava = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\entity\Aeration.java", $aerationJava, (New-Object System.Text.UTF8Encoding($false)))

$siloRepo = @'
package com.grainsilo.hub.repository;

import com.grainsilo.hub.entity.Silo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface SiloRepository extends JpaRepository<Silo, Long> {
    List<Silo> findAllByOrderByIdDesc();
}
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\repository\SiloRepository.java", $siloRepo, (New-Object System.Text.UTF8Encoding($false)))

$condRepo = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\repository\StorageConditionRepository.java", $condRepo, (New-Object System.Text.UTF8Encoding($false)))

$aerationRepo = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\repository\AerationRepository.java", $aerationRepo, (New-Object System.Text.UTF8Encoding($false)))

$siloServ = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\service\SiloService.java", $siloServ, (New-Object System.Text.UTF8Encoding($false)))

$condServ = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\service\StorageConditionService.java", $condServ, (New-Object System.Text.UTF8Encoding($false)))

$aerationServ = @'
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
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\service\AerationService.java", $aerationServ, (New-Object System.Text.UTF8Encoding($false)))

$dashCtrl = @'
package com.grainsilo.hub.controller;

import com.grainsilo.hub.service.AerationService;
import com.grainsilo.hub.service.SiloService;
import com.grainsilo.hub.service.StorageConditionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class DashboardController {

    private final SiloService siloService;
    private final StorageConditionService conditionService;
    private final AerationService aerationService;

    @Autowired
    public DashboardController(SiloService siloService, 
                               StorageConditionService conditionService, 
                               AerationService aerationService) {
        this.siloService = siloService;
        this.conditionService = conditionService;
        this.aerationService = aerationService;
    }

    @GetMapping({"/", "/dashboard"})
    public String viewDashboard(Model model) {
        model.addAttribute("totalSilos", siloService.countSilos());
        model.addAttribute("totalConditions", conditionService.countConditions());
        model.addAttribute("totalAerations", aerationService.countAerations());
        model.addAttribute("recentSilos", siloService.getRecentSilos(5));
        model.addAttribute("activePage", "dashboard");
        return "index";
    }
}
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\controller\DashboardController.java", $dashCtrl, (New-Object System.Text.UTF8Encoding($false)))

$siloCtrl = @'
package com.grainsilo.hub.controller;

import com.grainsilo.hub.entity.Silo;
import com.grainsilo.hub.service.SiloService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import java.util.Optional;

@Controller
@RequestMapping("/silos")
public class SiloController {

    private final SiloService siloService;

    @Autowired
    public SiloController(SiloService siloService) {
        this.siloService = siloService;
    }

    @GetMapping
    public String listSilos(Model model) {
        model.addAttribute("silos", siloService.getAllSilos());
        model.addAttribute("activePage", "silos");
        return "silos";
    }

    @GetMapping("/new")
    public String showNewSiloForm(Model model) {
        model.addAttribute("silo", new Silo());
        model.addAttribute("pageTitle", "Add New Grain Silo");
        model.addAttribute("activePage", "silos");
        return "silo-form";
    }

    @GetMapping("/edit/{id}")
    public String showEditSiloForm(@PathVariable("id") Long id, Model model, RedirectAttributes redirectAttributes) {
        Optional<Silo> siloOptional = siloService.getSiloById(id);
        if (siloOptional.isPresent()) {
            model.addAttribute("silo", siloOptional.get());
            model.addAttribute("pageTitle", "Edit Grain Silo #" + id);
            model.addAttribute("activePage", "silos");
            return "silo-form";
        } else {
            redirectAttributes.addFlashAttribute("errorMessage", "Silo with ID " + id + " not found.");
            return "redirect:/silos";
        }
    }

    @PostMapping("/save")
    public String saveSilo(@Valid @ModelAttribute("silo") Silo silo, 
                           BindingResult bindingResult, 
                           Model model, 
                           RedirectAttributes redirectAttributes) {
        if (silo.getStoredQuantity() != null && silo.getStorageCapacity() != null) {
            if (silo.getStoredQuantity() > silo.getStorageCapacity()) {
                bindingResult.rejectValue("storedQuantity", "error.silo", 
                        "Stored quantity cannot exceed total storage capacity (" + silo.getStorageCapacity() + " tons).");
            }
        }

        if (bindingResult.hasErrors()) {
            model.addAttribute("pageTitle", silo.getId() == null ? "Add New Grain Silo" : "Edit Grain Silo #" + silo.getId());
            model.addAttribute("activePage", "silos");
            return "silo-form";
        }

        try {
            siloService.saveSilo(silo);
            redirectAttributes.addFlashAttribute("successMessage", 
                    "Silo '" + silo.getSiloName() + "' was successfully saved!");
        } catch (IllegalArgumentException e) {
            model.addAttribute("errorMessage", e.getMessage());
            model.addAttribute("pageTitle", silo.getId() == null ? "Add New Grain Silo" : "Edit Grain Silo #" + silo.getId());
            model.addAttribute("activePage", "silos");
            return "silo-form";
        }

        return "redirect:/silos";
    }

    @GetMapping("/delete/{id}")
    public String deleteSilo(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        try {
            siloService.deleteSilo(id);
            redirectAttributes.addFlashAttribute("successMessage", 
                    "Silo #" + id + " and all associated records were deleted successfully.");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", 
                    "Error deleting silo: " + e.getMessage());
        }
        return "redirect:/silos";
    }
}
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\controller\SiloController.java", $siloCtrl, (New-Object System.Text.UTF8Encoding($false)))

$condCtrl = @'
package com.grainsilo.hub.controller;

import com.grainsilo.hub.entity.StorageCondition;
import com.grainsilo.hub.service.SiloService;
import com.grainsilo.hub.service.StorageConditionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import java.time.LocalDate;
import java.util.Optional;

@Controller
@RequestMapping("/conditions")
public class StorageConditionController {

    private final StorageConditionService conditionService;
    private final SiloService siloService;

    @Autowired
    public StorageConditionController(StorageConditionService conditionService, SiloService siloService) {
        this.conditionService = conditionService;
        this.siloService = siloService;
    }

    @GetMapping
    public String listConditions(Model model) {
        model.addAttribute("conditions", conditionService.getAllConditions());
        model.addAttribute("activePage", "conditions");
        return "conditions";
    }

    @GetMapping("/new")
    public String showNewConditionForm(Model model, RedirectAttributes redirectAttributes) {
        if (siloService.countSilos() == 0) {
            redirectAttributes.addFlashAttribute("errorMessage", 
                    "Please create at least one Grain Silo before recording storage conditions.");
            return "redirect:/silos/new";
        }

        StorageCondition condition = new StorageCondition();
        condition.setRecordedDate(LocalDate.now());

        model.addAttribute("condition", condition);
        model.addAttribute("silos", siloService.getAllSilos());
        model.addAttribute("pageTitle", "Record New Storage Condition");
        model.addAttribute("activePage", "conditions");
        return "condition-form";
    }

    @GetMapping("/edit/{id}")
    public String showEditConditionForm(@PathVariable("id") Long id, Model model, RedirectAttributes redirectAttributes) {
        Optional<StorageCondition> conditionOptional = conditionService.getConditionById(id);
        if (conditionOptional.isPresent()) {
            model.addAttribute("condition", conditionOptional.get());
            model.addAttribute("silos", siloService.getAllSilos());
            model.addAttribute("pageTitle", "Edit Storage Condition #" + id);
            model.addAttribute("activePage", "conditions");
            return "condition-form";
        } else {
            redirectAttributes.addFlashAttribute("errorMessage", "Reading with ID " + id + " not found.");
            return "redirect:/conditions";
        }
    }

    @PostMapping("/save")
    public String saveCondition(@Valid @ModelAttribute("condition") StorageCondition condition,
                                BindingResult bindingResult,
                                Model model,
                                RedirectAttributes redirectAttributes) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("silos", siloService.getAllSilos());
            model.addAttribute("pageTitle", condition.getId() == null ? "Record New Storage Condition" : "Edit Storage Condition #" + condition.getId());
            model.addAttribute("activePage", "conditions");
            return "condition-form";
        }

        conditionService.saveCondition(condition);
        redirectAttributes.addFlashAttribute("successMessage", 
                "Storage condition record #" + condition.getId() + " was saved successfully!");

        return "redirect:/conditions";
    }

    @GetMapping("/delete/{id}")
    public String deleteCondition(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        try {
            conditionService.deleteCondition(id);
            redirectAttributes.addFlashAttribute("successMessage", 
                    "Condition reading #" + id + " was deleted successfully.");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", 
                    "Error deleting condition reading: " + e.getMessage());
        }
        return "redirect:/conditions";
    }
}
'@
[System.IO.File]::WriteAllText("$PSScriptRoot\src\main\java\com\grainsilo\hub\controller\StorageConditionController.java", $condCtrl, (New-Object System.Text.UTF8Encoding($false)))

Write-Host "All source files restored successfully."
