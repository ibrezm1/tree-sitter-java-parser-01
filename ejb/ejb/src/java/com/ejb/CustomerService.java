package com.ejb;

import javax.ejb.Remote;
import javax.ejb.Stateless;
import javax.interceptor.Interceptors;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

import com.interceptor.TaskInterceptor;
import com.jpa.Customer;

@Remote
@Stateless
public class CustomerService {
    
    @PersistenceContext
    private EntityManager em;
    
    @Interceptors({TaskInterceptor.class})
    public Customer createCustomer(String firstName, String lastName) {
        Customer customer = new Customer();
        customer.setFirstName(firstName);
        customer.setLastName(lastName);

        em.persist(customer);

        System.err.println("##### CustomerService: " + firstName + " - " + lastName);

        return customer;
    }
    
}