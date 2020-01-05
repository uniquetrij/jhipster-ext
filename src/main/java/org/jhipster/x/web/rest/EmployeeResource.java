package org.jhipster.x.web.rest;

import org.jhipster.domain.Employee;
import org.jhipster.x.service.EmployeeService;
import org.jhipster.web.rest.errors.BadRequestAlertException;

import io.github.jhipster.web.util.HeaderUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;

/**
 * REST controller for managing {@link org.jhipster.domain.Employee}.
 */
@RestController("EmployeeResource")
@RequestMapping("/api/rest")
public class EmployeeResource extends org.jhipster.web.rest.EmployeeResource {

    private final Logger log = LoggerFactory.getLogger(EmployeeResource.class);

    private static final String ENTITY_NAME = "employee";

    @Value("${jhipster.clientApp.name}")
    private String applicationName;

    private final EmployeeService employeeService;

    public EmployeeResource(EmployeeService employeeService) {
        super(employeeService);
        this.employeeService = employeeService;
    }

    /**
     * {@code GET  /employees} : get all the employees.
     *
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and the list of employees in body.
     */
    @GetMapping("/employees/test")
    public List<Employee> getAllEmployees() {
        log.debug("REST request to get all Employees");
        return employeeService.findAll();
    }
}
