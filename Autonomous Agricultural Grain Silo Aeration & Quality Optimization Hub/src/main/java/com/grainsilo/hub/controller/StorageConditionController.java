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