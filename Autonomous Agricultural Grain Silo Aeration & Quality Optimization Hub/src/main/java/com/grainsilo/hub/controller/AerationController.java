package com.grainsilo.hub.controller;

import com.grainsilo.hub.entity.Aeration;
import com.grainsilo.hub.service.AerationService;
import com.grainsilo.hub.service.SiloService;
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
@RequestMapping("/aerations")
public class AerationController {

    private final AerationService aerationService;
    private final SiloService siloService;

    @Autowired
    public AerationController(AerationService aerationService, SiloService siloService) {
        this.aerationService = aerationService;
        this.siloService = siloService;
    }

    // Display all aeration activities
    @GetMapping
    public String listAerations(Model model) {
        model.addAttribute("aerations", aerationService.getAllAerations());
        model.addAttribute("activePage", "aerations");
        return "aerations";
    }

    // Show form to add a new aeration activity
    @GetMapping("/new")
    public String showNewAerationForm(Model model, RedirectAttributes redirectAttributes) {
        if (siloService.countSilos() == 0) {
            redirectAttributes.addFlashAttribute("errorMessage", 
                    "Please create at least one Grain Silo before recording aeration activities.");
            return "redirect:/silos/new";
        }

        Aeration aeration = new Aeration();
        aeration.setAerationDate(LocalDate.now());
        aeration.setFanStatus("ON");

        model.addAttribute("aeration", aeration);
        model.addAttribute("silos", siloService.getAllSilos());
        model.addAttribute("pageTitle", "Record New Aeration Activity");
        model.addAttribute("activePage", "aerations");
        return "aeration-form";
    }

    // Show form to edit existing aeration record
    @GetMapping("/edit/{id}")
    public String showEditAerationForm(@PathVariable("id") Long id, Model model, RedirectAttributes redirectAttributes) {
        Optional<Aeration> aerationOptional = aerationService.getAerationById(id);
        if (aerationOptional.isPresent()) {
            model.addAttribute("aeration", aerationOptional.get());
            model.addAttribute("silos", siloService.getAllSilos());
            model.addAttribute("pageTitle", "Edit Aeration Record #" + id);
            model.addAttribute("activePage", "aerations");
            return "aeration-form";
        } else {
            redirectAttributes.addFlashAttribute("errorMessage", "Aeration record with ID " + id + " not found.");
            return "redirect:/aerations";
        }
    }

    // Save or update aeration record
    @PostMapping("/save")
    public String saveAeration(@Valid @ModelAttribute("aeration") Aeration aeration,
                               BindingResult bindingResult,
                               Model model,
                               RedirectAttributes redirectAttributes) {

        if (bindingResult.hasErrors()) {
            model.addAttribute("silos", siloService.getAllSilos());
            model.addAttribute("pageTitle", aeration.getId() == null ? "Record New Aeration Activity" : "Edit Aeration Record #" + aeration.getId());
            model.addAttribute("activePage", "aerations");
            return "aeration-form";
        }

        aerationService.saveAeration(aeration);
        redirectAttributes.addFlashAttribute("successMessage", 
                "Aeration record #" + aeration.getId() + " was saved successfully!");

        return "redirect:/aerations";
    }

    // Delete aeration record
    @GetMapping("/delete/{id}")
    public String deleteAeration(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        try {
            aerationService.deleteAeration(id);
            redirectAttributes.addFlashAttribute("successMessage", 
                    "Aeration record #" + id + " was deleted successfully.");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", 
                    "Error deleting aeration record: " + e.getMessage());
        }
        return "redirect:/aerations";
    }
}
