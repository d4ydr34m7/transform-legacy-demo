package com.verafin.legacy;

import com.verafin.commons.jdo.LegacyJdoManager;

public class CustomerService {
    private final LegacyJdoManager jdo;

    public CustomerService(LegacyJdoManager jdo) {
        this.jdo = jdo;
    }

    public String formatDisplay(Customer c) {
        jdo.begin();
        try {
            String out = c.getId() + ":" + c.getName();
            jdo.commit();
            return out;
        } catch (RuntimeException e) {
            jdo.rollback();
            throw e;
        }
    }
}
