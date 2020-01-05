package org.jhipster.service;

import org.jhipster.domain.Employee;

import java.util.List;
import java.util.Optional;

/**
 * Service Interface for managing {@link Employee}.
 */
public interface EmployeeService {

    /**
     * Save a employee.
     *
     * @param employee the entity to save.
     * @return the persisted entity.
     */
    Employee save(Employee employee);

    /**
     * Get all the employees.
     *
     * @return the list of entities.
     */
    List<Employee> findAll();


    /**
     * Get the "id" employee.
     *
     * @param id the id of the entity.
     * @return the entity.
     */
    Optional<Employee> findOne(Long id);

    /**
     * Delete the "id" employee.
     *
     * @param id the id of the entity.
     */
    void delete(Long id);
}
