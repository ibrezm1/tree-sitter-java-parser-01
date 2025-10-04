package com.jpa;

import java.io.Serializable;

import javax.persistence.*;

@Entity
@EntityListeners(CustomerListener.class)
@Table(name = "CUSTOMER", schema = "ejb")
public class Customer implements Serializable {

    private Long id;
    
    private String firstName;
    private String LastName;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "ID")
    public Long getId() {
        return id;
    }
    
    @Basic
    @Column(name = "FIRSTNAME")
    public String getFirstName() {
        return firstName;
    }
    
    @Basic
    @Column(name = "LASTNAME")
    public String getLastName() {
        return LastName;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }
    
    public void setLastName(String LastName) {
        this.LastName = LastName;
    }
    
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Customer)) {
            return false;
        }
        Customer other = (Customer) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.jpa.Customer[ id=" + id + " ]";
    }
    
}
