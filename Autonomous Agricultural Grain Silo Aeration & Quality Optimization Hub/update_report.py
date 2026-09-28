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

def process_document(docx_path, output_path):
    doc = docx.Document(docx_path)
    
    # --- 1. Table 0 (Title page table) ---
    t0 = doc.tables[0]
    # Row 0, Cell 1 has the title
    cell_title = t0.rows[0].cells[1]
    for p in cell_title.paragraphs:
        if '<< TITLE OF THE PROJECT >>' in p.text or 'PROJECT' in p.text:
            set_para_text(p, 'AUTONOMOUS AGRICULTURAL GRAIN SILO AERATION & QUALITY OPTIMIZATION HUB', bold=True)
            break
            
    # --- 2. Table 5 (Project Batch & Details) ---
    t5 = doc.tables[5]
    # Row 0: PROJECT TITLE | PROJECT NAME
    t5.rows[0].cells[1].text = 'AUTONOMOUS AGRICULTURAL GRAIN SILO AERATION & QUALITY OPTIMIZATION HUB'
    t5.rows[0].cells[2].text = 'AUTONOMOUS AGRICULTURAL GRAIN SILO AERATION & QUALITY OPTIMIZATION HUB'
    
    # Row 8: SDG GOALS MAPPED
    t5.rows[8].cells[1].text = 'SDG 2: Zero Hunger & SDG 12: Responsible Consumption and Production'
    t5.rows[8].cells[2].text = 'SDG 2: Zero Hunger & SDG 12: Responsible Consumption and Production'
    
    # Row 9: MENTION THE SDG GOALS NUMBER
    t5.rows[9].cells[1].text = 'Goal 2 (Target 2.4 - Sustainable Food Production) & Goal 12 (Target 12.3 - Reduce Food Loss)'
    t5.rows[9].cells[2].text = 'Goal 2 (Target 2.4 - Sustainable Food Production) & Goal 12 (Target 12.3 - Reduce Food Loss)'
    
    # Row 10: NAME OF THE TRL LEVEL
    t5.rows[10].cells[1].text = 'Technology Readiness Level 3 (TRL 3)'
    t5.rows[10].cells[2].text = 'Technology Readiness Level 3 (TRL 3)'
    
    # Row 11: MENTION THE TRL LEVEL
    t5.rows[11].cells[1].text = 'TRL 3: Analytical and experimental critical function proof of concept'
    t5.rows[11].cells[2].text = 'TRL 3: Analytical and experimental critical function proof of concept'

    # --- 3. Table 6 (POs & PSOs Mapping) ---
    t6 = doc.tables[6]
    # Row 2 contains checkboxes: PO1 to PO11, PSO1 to PSO3
    # Mapped: PO1, PO2, PO3, PO4, PO5, PO6, PO7, PO9, PO10, PO11, PSO1, PSO2, PSO3
    mapped_indices = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
    for idx in range(len(t6.rows[2].cells)):
        if idx in mapped_indices:
            t6.rows[2].cells[idx].text = '✓'
        else:
            t6.rows[2].cells[idx].text = ''

    # --- 4. Table 7 (Laboratory details) ---
    t7 = doc.tables[7]
    t7.rows[1].cells[1].text = 'Java JDK 17, Spring Boot 3.2.5, MySQL Server 8.0, Visual Studio Code (VS Code), Apache Maven 3.9, Windows 11 PC'

    # --- 5. Table 8 (Component & Expenditure) ---
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

    # --- 6. Paragraphs Updates ---
    # Find key sections dynamically by header text
    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        
        # 1.1 OBJECTIVE paragraphs
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

        # Headings for code
        elif "CONTROLLER (ExpenseController.java)" in txt:
            set_para_text(p, "CONTROLLER (SiloController.java)", bold=True)
        elif "ENTITY (Expense.java)" in txt:
            set_para_text(p, "ENTITY (Silo.java)", bold=True)
        elif "PDF.HTML" in txt:
            set_para_text(p, "CONDITIONS.HTML", bold=True)

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

    doc.save(output_path)
    print(f"Successfully processed and saved to {output_path}")

if __name__ == '__main__':
    process_document(r'E:\Studies\Clg\2nd Year\Sem 3\Java\leap project report\1\Leap.docx',
                     r'E:\Studies\Clg\2nd Year\Sem 3\Java\leap project report\1\Leap.docx')
    process_document(r'E:\Studies\Clg\2nd Year\Sem 3\Java\leap project report\project report final.docx',
                     r'E:\Studies\Clg\2nd Year\Sem 3\Java\leap project report\project report final.docx')
