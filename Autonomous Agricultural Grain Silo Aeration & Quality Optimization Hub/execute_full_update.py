import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH

def set_para_text(p, text, align=None, bold=None):
    if align is not None:
        p.alignment = align
    if p.runs:
        p.runs[0].text = text
        if bold is not None:
            p.runs[0].font.bold = bold
        for r in p.runs[1:]:
            r.text = ''
    else:
        run = p.add_run(text)
        if bold is not None:
            run.font.bold = bold

def replace_block(doc, start_header, end_header, new_code_lines):
    # Find start and end indices
    start_idx = -1
    end_idx = -1
    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if start_header in txt and start_idx == -1:
            start_idx = i
        elif end_header in txt and start_idx != -1 and end_idx == -1:
            end_idx = i
            break
            
    if start_idx == -1 or end_idx == -1:
        print(f"Warning: Could not find block between '{start_header}' and '{end_header}'")
        return

    available_slots = end_idx - start_idx - 1
    for i in range(available_slots):
        target_idx = start_idx + 1 + i
        p = doc.paragraphs[target_idx]
        if i < len(new_code_lines):
            # If it's the last slot and we have more lines left, join remaining lines
            if i == available_slots - 1 and len(new_code_lines) > available_slots:
                joined = "\n".join(new_code_lines[i:])
                set_para_text(p, joined)
            else:
                set_para_text(p, new_code_lines[i])
        else:
            set_para_text(p, "")

def update_entire_report(file_path):
    print(f"Processing: {file_path}")
    doc = docx.Document(file_path)

    # 1. Update Title Page Table 0
    t0 = doc.tables[0]
    cell_title = t0.rows[0].cells[1]
    for p in cell_title.paragraphs:
        if '<< TITLE OF THE PROJECT >>' in p.text or 'PROJECT' in p.text:
            set_para_text(p, 'AUTONOMOUS AGRICULTURAL GRAIN SILO AERATION & QUALITY OPTIMIZATION HUB', bold=True)
            break

    # 2. Update Table 5 (Project Batch & Details)
    t5 = doc.tables[5]
    t5.rows[0].cells[1].text = 'AUTONOMOUS AGRICULTURAL GRAIN SILO AERATION & QUALITY OPTIMIZATION HUB'
    t5.rows[0].cells[2].text = 'AUTONOMOUS AGRICULTURAL GRAIN SILO AERATION & QUALITY OPTIMIZATION HUB'
    t5.rows[8].cells[1].text = 'SDG 2: Zero Hunger & SDG 12: Responsible Consumption and Production'
    t5.rows[8].cells[2].text = 'SDG 2: Zero Hunger & SDG 12: Responsible Consumption and Production'
    t5.rows[9].cells[1].text = 'Goal 2 (Target 2.4 - Sustainable Food Production) & Goal 12 (Target 12.3 - Reduce Food Loss)'
    t5.rows[9].cells[2].text = 'Goal 2 (Target 2.4 - Sustainable Food Production) & Goal 12 (Target 12.3 - Reduce Food Loss)'
    t5.rows[10].cells[1].text = 'Technology Readiness Level 3 (TRL 3)'
    t5.rows[10].cells[2].text = 'Technology Readiness Level 3 (TRL 3)'
    t5.rows[11].cells[1].text = 'TRL 3: Analytical and experimental critical function proof of concept'
    t5.rows[11].cells[2].text = 'TRL 3: Analytical and experimental critical function proof of concept'

    # 3. Update Table 6 (POs & PSOs Mapping)
    t6 = doc.tables[6]
    mapped_indices = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
    for idx in range(len(t6.rows[2].cells)):
        t6.rows[2].cells[idx].text = '✓' if idx in mapped_indices else ''

    # 4. Update Table 7 (Laboratory details)
    t7 = doc.tables[7]
    t7.rows[1].cells[1].text = 'Java JDK 17, Spring Boot 3.2.5, MySQL Server 8.0, Visual Studio Code (VS Code), Apache Maven 3.9, Windows 11 PC'

    # 5. Update Table 8 (Component & Expenditure)
    t8 = doc.tables[8]
    expenditures = [
        ("1", "Visual Studio Code IDE", "1", "0.00 (Open Source)", "0.00"),
        ("2", "Oracle Java Development Kit (JDK 17)", "1", "0.00 (Open Source)", "0.00"),
        ("3", "Spring Boot 3 Framework & Libraries", "1", "0.00 (Open Source)", "0.00"),
        ("4", "MySQL Community Server 8.0 & Workbench", "1", "0.00 (Open Source)", "0.00"),
        ("5", "Apache Maven Build Tool", "1", "0.00 (Open Source)", "0.00"),
        ("6", "Bootstrap 5 UI Framework & Web Icons", "1", "0.00 (Open Source)", "0.00"),
        ("7", "Documentation, Printing & Binding Expenses", "4", "250.00", "1,000.00"),
        ("Total", "", "", "", "Rs. 1,000.00")
    ]
    for i, exp in enumerate(expenditures):
        row = t8.rows[i + 1]
        for col_idx, val in enumerate(exp):
            row.cells[col_idx].text = val

    # 6. Content Paragraphs Updates (Theory Sections)
    for p in doc.paragraphs:
        txt = p.text.strip()
        
        # 1.1 OBJECTIVE
        if txt.startswith("The Spring Boot-based PROJECT NAME aims to develop a sophisticated web application for effective personal financial management"):
            set_para_text(p, "The Spring Boot-based Autonomous Agricultural Grain Silo Aeration & Quality Optimization Hub aims to develop a robust, centralized web application for effective grain storage management and environmental condition monitoring. It prioritizes grain quality preservation and post-harvest loss prevention by tracking temperature and relative humidity inside bulk storage silos. Users can effortlessly manage silo facilities through seamless CRUD operations and record fan aeration activities to maintain optimal grain storage parameters.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("Built with HTML, CSS, and JavaScript templates, the application provides an intuitive"):
            set_para_text(p, "Built with Thymeleaf, HTML5, CSS3, and Bootstrap 5, the application provides an intuitive, visually engaging user interface. It emphasizes usability, accessibility, and operational clarity through real-time condition indicators (NORMAL and ATTENTION) and dynamic capacity utilization progress bars. Stringent data integrity and relational consistency are maintained with Spring Boot's Spring Data JPA framework and MySQL database, including automated schema generation and cascade safe deletions.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("Ultimately, this project empowers users with a powerful tool for maintaining financial discipline"):
            set_para_text(p, "Ultimately, this project empowers warehouse managers, farmers, and agricultural cooperatives with a practical software prototype for preventing grain spoilage, hot spot formation, and moisture accumulation, supporting informed operational decisions in grain aeration management.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

        # EXISTING SCENARIO
        elif txt.startswith("In the current digital landscape, numerous platforms and applications facilitate personal finance management"):
            set_para_text(p, "In current agricultural storage and grain warehousing facilities, environmental monitoring and aeration scheduling are predominantly conducted through manual logging, paper ledgers, or standalone spreadsheets. Facility supervisors manually record thermometer cable readings and relative humidity values at irregular intervals. Commercial grain elevator automation systems and industrial SCADA platforms offer sophisticated real-time telemetry and automated controls; however, they require expensive proprietary hardware, high sensor maintenance overhead, and complex software licensing costs that remain inaccessible to small and medium agricultural cooperatives.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("For individuals and smaller entities who wish to manage their finances with greater control"):
            set_para_text(p, "For local grain storage facilities and cooperative warehouses seeking reliable management without the cost and complexity of industrial automation, these proprietary systems are often impractical. The need arises for a clean, accessible web-based hub that simplifies silo record-keeping, condition tracking, and aeration history without requiring specialized hardware installations. This gap is addressed by Java-based solutions like the Autonomous Agricultural Grain Silo Aeration & Quality Optimization Hub, enabling operators to record micro-climate readings, review capacity metrics, and maintain aeration logs independently using open-source Spring Boot and MySQL technologies.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

        # PROBLEM STATEMENT
        elif txt.startswith("The Spring Boot-based PROJECT NAME revolutionizes personal financial management with a robust and user-friendly web application"):
            set_para_text(p, "The Spring Boot-based Autonomous Agricultural Grain Silo Aeration & Quality Optimization Hub addresses the critical challenges of agricultural post-harvest storage through a structured, user-friendly web application. Managing storage conditions across multiple silos is challenging when done manually, often resulting in undetected core heating, mold development, and capacity overfill errors. This system provides comprehensive CRUD operations for facility operators to manage grain silo parameters, record temperature and humidity readings, and maintain ventilation run records.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("The application generates automated financial summaries and insightful reports from entered expenses"):
            set_para_text(p, "The application provides immediate operational insights by benchmarking recorded temperature and humidity readings against established demonstration safety thresholds, categorizing silo conditions into NORMAL and ATTENTION statuses. Built with Thymeleaf and Bootstrap 5, its responsive dashboard ensures usability across all screen sizes with visual capacity indicators.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("Spring Boot's security features and a MySQL database maintain data integrity and privacy"):
            set_para_text(p, "Spring Data JPA and a robust MySQL database maintain relational integrity, enforcing business rules such as verifying that stored grain weight cannot exceed total storage capacity, while automatically handling safe cascade deletions when a silo is retired.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

        # PROPOSED SOLUTION - OVERVIEW
        elif txt.startswith("The Spring Boot-based PROJECT NAME transforms personal financial management with its robust features"):
            set_para_text(p, "The Spring Boot-based Autonomous Agricultural Grain Silo Aeration & Quality Optimization Hub transforms bulk grain storage oversight with structured management features and an accessible interface. Developed with Java 17 and Spring Boot 3, the application establishes a centralized platform where storage facility personnel can maintain comprehensive digital records for grain bins and environmental parameters.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("Users can efficiently manage expenses through intuitive CRUD operations"):
            set_para_text(p, "Users can efficiently manage facilities through intuitive CRUD operations across three dedicated modules: Grain Silo Management, Storage Condition Monitoring, and Aeration Activity Logging. An integrated threshold evaluation engine analyzes environmental readings, displaying color-coded status badges that alert operators to potential risks before grain degradation occurs.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("Built with Thymeleaf and Bootstrap, the application ensures responsiveness across devices"):
            set_para_text(p, "Built with Thymeleaf and Bootstrap 5, the application delivers a modern, responsive user experience complete with intuitive forms, data tables, and capacity utilization progress bars. Database operations are handled efficiently via Spring Data JPA and Hibernate, with automated schema creation in MySQL.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("The interface is designed for seamless navigation and user engagement, facilitating informed decision-making"):
            set_para_text(p, "The application serves as a complete academic prototype demonstrating automated decision support for grain quality preservation, empowering agricultural managers with accurate record-keeping, historical operational reviews, and proactive ventilation management.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

        # CONCLUSION
        elif txt.startswith("The PROJECT NAME built with Spring Boot represents a robust solution for individuals seeking efficient management of their finances"):
            set_para_text(p, "The Autonomous Agricultural Grain Silo Aeration & Quality Optimization Hub built with Spring Boot represents a robust solution for agricultural facility managers and grain warehouse supervisors seeking efficient oversight of bulk storage conditions. By leveraging Spring Boot's MVC architecture and MySQL, the application integrates essential features such as Grain Silo Inventory CRUD, environmental micro-climate tracking, and aeration fan activity logging. Enforcing strict business logic, such as preventing stored grain volume from exceeding bin capacity, ensures operational accuracy.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("For financial oversight, the application calculates and displays the total sum of expenses"):
            set_para_text(p, "For quality preservation, the application's condition monitoring engine compares recorded temperature and relative humidity values against demonstration safety thresholds, instantly providing operators with color-coded NORMAL and ATTENTION indicators. Safe cascade deletion ensures associated monitoring records and aeration logs are cleaned up safely when a silo is removed. The frontend, designed with Thymeleaf and Bootstrap 5, delivers a responsive, intuitive interface featuring real-time metric cards and utilization progress bars.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        elif txt.startswith("Overall, the PROJECT NAME exemplifies a practical application of Spring Boot's capabilities"):
            set_para_text(p, "Overall, the project exemplifies a practical application of Java Spring Boot in agricultural technology, providing a reliable, cost-effective prototype that bridges the gap between manual record-keeping and industrial grain management systems.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

        # REFERENCES
        elif "Spring Security Reference" in txt:
            set_para_text(p, "Hibernate Community. (2024). Hibernate ORM Core Documentation. Retrieved from https://hibernate.org/orm/documentation/6.4/")
        elif "expense" in txt.lower() and "personal finance" in txt.lower():
            set_para_text(p, "Food and Agriculture Organization (FAO). (2023). Grain Storage and Aeration Manual for Quality Preservation in Tropical and Subtropical Climates. Rome: United Nations.")

    # 7. Code Sections Updates
    # Update Section Headers
    for p in doc.paragraphs:
        txt = p.text.strip()
        if "CONTROLLER (ExpenseController.java)" in txt:
            set_para_text(p, "CONTROLLER (SiloController.java)", bold=True)
        elif "ENTITY (Expense.java)" in txt:
            set_para_text(p, "ENTITY (Silo.java)", bold=True)
        elif "PDF.HTML" in txt:
            set_para_text(p, "CONDITIONS.HTML", bold=True)

    # Controller Code Lines
    controller_code = [
        "package com.grainsilo.hub.controller;",
        "",
        "import com.grainsilo.hub.entity.Silo;",
        "import com.grainsilo.hub.service.SiloService;",
        "import jakarta.validation.Valid;",
        "import org.springframework.beans.factory.annotation.Autowired;",
        "import org.springframework.stereotype.Controller;",
        "import org.springframework.ui.Model;",
        "import org.springframework.validation.BindingResult;",
        "import org.springframework.web.bind.annotation.*;",
        "import org.springframework.web.servlet.mvc.support.RedirectAttributes;",
        "import java.util.List;",
        "",
        "@Controller",
        "@RequestMapping(\"/silos\")",
        "public class SiloController {",
        "",
        "    @Autowired",
        "    private SiloService siloService;",
        "",
        "    // List all silos",
        "    @GetMapping",
        "    public String listSilos(Model model) {",
        "        model.addAttribute(\"silos\", siloService.getAllSilos());",
        "        model.addAttribute(\"activePage\", \"silos\");",
        "        return \"silos\";",
        "    }",
        "",
        "    // Show add new silo form",
        "    @GetMapping(\"/new\")",
        "    public String showNewSiloForm(Model model) {",
        "        model.addAttribute(\"silo\", new Silo());",
        "        model.addAttribute(\"pageTitle\", \"Add New Grain Silo\");",
        "        return \"silo-form\";",
        "    }",
        "",
        "    // Save silo with capacity validation",
        "    @PostMapping(\"/save\")",
        "    public String saveSilo(@Valid @ModelAttribute(\"silo\") Silo silo,",
        "                           BindingResult result, Model model,",
        "                           RedirectAttributes redirectAttributes) {",
        "        if (silo.getStoredQuantity() != null && silo.getStorageCapacity() != null) {",
        "            if (silo.getStoredQuantity() > silo.getStorageCapacity()) {",
        "                result.rejectValue(\"storedQuantity\", \"error.silo\",",
        "                        \"Stored quantity cannot exceed total storage capacity.\");",
        "            }",
        "        }",
        "        if (result.hasErrors()) {",
        "            model.addAttribute(\"pageTitle\", \"Edit Grain Silo\");",
        "            return \"silo-form\";",
        "        }",
        "        siloService.saveSilo(silo);",
        "        redirectAttributes.addFlashAttribute(\"successMessage\", \"Silo saved successfully!\");",
        "        return \"redirect:/silos\";",
        "    }",
        "",
        "    // Delete silo safely",
        "    @GetMapping(\"/delete/{id}\")",
        "    public String deleteSilo(@PathVariable Long id, RedirectAttributes redirectAttributes) {",
        "        siloService.deleteSilo(id);",
        "        redirectAttributes.addFlashAttribute(\"successMessage\", \"Silo deleted successfully.\");",
        "        return \"redirect:/silos\";",
        "    }",
        "}"
    ]
    replace_block(doc, "CONTROLLER (SiloController.java)", "APPLICATION CONFIG (application.properties)", controller_code)

    # application.properties Lines
    app_props_code = [
        "# Server Port",
        "server.port=8080",
        "",
        "# Spring Application Name",
        "spring.application.name=grain-silo-hub",
        "",
        "# MySQL Database Configuration",
        "spring.datasource.url=jdbc:mysql://localhost:3306/grain_silo_db?createDatabaseIfNotExist=true&useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true",
        "spring.datasource.username=root",
        "spring.datasource.password=toor",
        "spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver",
        "",
        "# JPA & Hibernate Settings",
        "spring.jpa.hibernate.ddl-auto=update",
        "spring.jpa.show-sql=true",
        "spring.jpa.properties.hibernate.format_sql=true",
        "",
        "# Thymeleaf Template Settings",
        "spring.thymeleaf.cache=false",
        "spring.thymeleaf.prefix=classpath:/templates/",
        "spring.thymeleaf.suffix=.html"
    ]
    replace_block(doc, "APPLICATION CONFIG (application.properties)", "ENTITY (Silo.java)", app_props_code)

    # Entity Code Lines
    entity_code = [
        "package com.grainsilo.hub.entity;",
        "",
        "import jakarta.persistence.*;",
        "import jakarta.validation.constraints.DecimalMin;",
        "import jakarta.validation.constraints.NotBlank;",
        "import jakarta.validation.constraints.NotNull;",
        "import java.util.ArrayList;",
        "import java.util.List;",
        "",
        "@Entity",
        "@Table(name = \"silo\")",
        "public class Silo {",
        "",
        "    @Id",
        "    @GeneratedValue(strategy = GenerationType.IDENTITY)",
        "    private Long id;",
        "",
        "    @NotBlank(message = \"Silo Name is required\")",
        "    private String siloName;",
        "",
        "    @NotBlank(message = \"Location is required\")",
        "    private String location;",
        "",
        "    @NotBlank(message = \"Grain Type is required\")",
        "    private String grainType;",
        "",
        "    @NotNull(message = \"Storage Capacity is required\")",
        "    @DecimalMin(value = \"0.1\")",
        "    private Double storageCapacity;",
        "",
        "    @NotNull(message = \"Stored Quantity is required\")",
        "    @DecimalMin(value = \"0.0\")",
        "    private Double storedQuantity;",
        "",
        "    // Safe Cascade Deletions for related monitoring records",
        "    @OneToMany(mappedBy = \"silo\", cascade = CascadeType.ALL, orphanRemoval = true)",
        "    private List<StorageCondition> storageConditions = new ArrayList<>();",
        "",
        "    // Getters and Setters",
        "    public Long getId() { return id; }",
        "    public void setId(Long id) { this.id = id; }",
        "    public String getSiloName() { return siloName; }",
        "    public void setSiloName(String siloName) { this.siloName = siloName; }",
        "    public String getLocation() { return location; }",
        "    public void setLocation(String location) { this.location = location; }",
        "    public String getGrainType() { return grainType; }",
        "    public void setGrainType(String grainType) { this.grainType = grainType; }",
        "    public Double getStorageCapacity() { return storageCapacity; }",
        "    public void setStorageCapacity(Double storageCapacity) { this.storageCapacity = storageCapacity; }",
        "    public Double getStoredQuantity() { return storedQuantity; }",
        "    public void setStoredQuantity(Double storedQuantity) { this.storedQuantity = storedQuantity; }",
        "}"
    ]
    replace_block(doc, "ENTITY (Silo.java)", "INDEX.HTML", entity_code)

    # index.html Lines
    index_html_code = [
        "<!DOCTYPE html>",
        "<html lang=\"en\" xmlns:th=\"http://www.thymeleaf.org\">",
        "<head>",
        "    <meta charset=\"UTF-8\">",
        "    <title>Grain Silo Aeration Hub - Dashboard</title>",
        "    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\">",
        "</head>",
        "<body class=\"bg-light\">",
        "<nav class=\"navbar navbar-expand-lg navbar-dark bg-dark\">",
        "    <div class=\"container\">",
        "        <a class=\"navbar-brand fw-bold\" th:href=\"@{/}\">Grain Silo Hub</a>",
        "        <div class=\"navbar-nav ms-auto\">",
        "            <a class=\"nav-link active\" th:href=\"@{/}\">Dashboard</a>",
        "            <a class=\"nav-link\" th:href=\"@{/silos}\">Silos</a>",
        "            <a class=\"nav-link\" th:href=\"@{/conditions}\">Conditions</a>",
        "            <a class=\"nav-link\" th:href=\"@{/aerations}\">Aeration Logs</a>",
        "        </div>",
        "    </div>",
        "</nav>",
        "<div class=\"container mt-4\">",
        "    <h3 class=\"mb-3\">Overview Dashboard</h3>",
        "    <div class=\"row g-3 mb-4\">",
        "        <div class=\"col-md-4\">",
        "            <div class=\"card bg-primary text-white p-3 shadow-sm\">",
        "                <h6>Total Grain Silos</h6>",
        "                <h2 th:text=\"${totalSilos}\">0</h2>",
        "            </div>",
        "        </div>",
        "        <div class=\"col-md-4\">",
        "            <div class=\"card bg-success text-white p-3 shadow-sm\">",
        "                <h6>Storage Conditions</h6>",
        "                <h2 th:text=\"${totalConditions}\">0</h2>",
        "            </div>",
        "        </div>",
        "        <div class=\"col-md-4\">",
        "            <div class=\"card bg-warning text-dark p-3 shadow-sm\">",
        "                <h6>Aeration Activities</h6>",
        "                <h2 th:text=\"${totalAerations}\">0</h2>",
        "            </div>",
        "        </div>",
        "    </div>",
        "</div>",
        "</body>",
        "</html>"
    ]
    replace_block(doc, "INDEX.HTML", "CONDITIONS.HTML", index_html_code)

    # conditions.html Lines (replaces PDF.HTML)
    conditions_html_code = [
        "<!DOCTYPE html>",
        "<html lang=\"en\" xmlns:th=\"http://www.thymeleaf.org\">",
        "<head>",
        "    <meta charset=\"UTF-8\">",
        "    <title>Storage Conditions - Grain Silo Hub</title>",
        "    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\">",
        "</head>",
        "<body class=\"bg-light\">",
        "<div class=\"container mt-4\">",
        "    <div class=\"d-flex justify-content-between mb-3\">",
        "        <h3>Storage Micro-Climate Readings</h3>",
        "        <a th:href=\"@{/conditions/new}\" class=\"btn btn-success\">Record Reading</a>",
        "    </div>",
        "    <table class=\"table table-bordered table-hover bg-white\">",
        "        <thead class=\"table-light\">",
        "            <tr>",
        "                <th>Silo</th>",
        "                <th>Grain Type</th>",
        "                <th>Temperature (°C)</th>",
        "                <th>Humidity (%)</th>",
        "                <th>Status Indicator</th>",
        "            </tr>",
        "        </thead>",
        "        <tbody>",
        "            <tr th:each=\"c : ${conditions}\">",
        "                <td th:text=\"${c.silo.siloName}\">North Silo</td>",
        "                <td th:text=\"${c.silo.grainType}\">Wheat</td>",
        "                <td th:text=\"${c.temperature} + ' °C'\">21.5 °C</td>",
        "                <td th:text=\"${c.humidity} + ' %'\">54.0 %</td>",
        "                <td><span th:class=\"${c.statusBadgeClass}\" th:text=\"${c.conditionStatus}\">NORMAL</span></td>",
        "            </tr>",
        "        </tbody>",
        "    </table>",
        "</div>",
        "</body>",
        "</html>"
    ]
    replace_block(doc, "CONDITIONS.HTML", "OUTPUT", conditions_html_code)

    doc.save(file_path)
    print(f"Update successfully written to: {file_path}")

if __name__ == '__main__':
    update_entire_report(r'E:\Studies\Clg\2nd Year\Sem 3\Java\leap project report\1\Leap.docx')
    update_entire_report(r'E:\Studies\Clg\2nd Year\Sem 3\Java\leap project report\project report final.docx')
