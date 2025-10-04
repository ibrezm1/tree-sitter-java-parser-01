/*
 * This code is part of pirobase PIM.
 * This code is developed by the pirobase imperia gmbh.
 * Do not make any changes.
 * ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 * Copyright (C) pirobase imperia gmbh
 * All Rights Reserved.
 * ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 */
package com.ejb.client;

import java.io.IOException;
import java.io.PrintWriter;
import javax.ejb.EJB;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.ejb.CustomerService;
import com.jpa.Customer;

@WebServlet(name = "AccountController", urlPatterns = {"/AccountController"})
public class AccountController extends HttpServlet {
    
    @EJB
    private CustomerService customerService;
    
    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        try (PrintWriter out = response.getWriter()) {
            String firstName = request.getParameter("firstName");
            String lastName = request.getParameter("lastName");
            
            Customer customer = customerService.createCustomer(firstName, lastName);
            out.println("Customer[" + customer.getFirstName() + "] : " + customer.getId());
        }
    }
    
}