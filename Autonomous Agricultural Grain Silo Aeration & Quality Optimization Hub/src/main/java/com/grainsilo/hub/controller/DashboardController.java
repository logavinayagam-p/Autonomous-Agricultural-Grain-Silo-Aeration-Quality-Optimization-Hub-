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