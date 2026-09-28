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