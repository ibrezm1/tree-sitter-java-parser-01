package com.jpa;

import javax.persistence.PostPersist;
import javax.persistence.PostUpdate;

public class CustomerListener {

    @PostPersist
    public void onPostPersist(Object o) {
        System.out.println("##### CustomerListener - object persisted: " + o);
    }

    @PostUpdate
    public void onPostUpdate(Object o) {
        System.out.println("##### CustomerListener - object updated: " + o);
    }
}
