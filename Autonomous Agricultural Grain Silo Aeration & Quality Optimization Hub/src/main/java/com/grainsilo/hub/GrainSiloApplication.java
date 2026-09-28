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