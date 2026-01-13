package com.verafin.legacy;

import com.verafin.commons.jdo.LegacyJdoManager;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CustomerServiceTest {
    @Test
    void formatsDisplay() {
        CustomerService svc = new CustomerService(new LegacyJdoManager());
        assertEquals("1:Shreya", svc.formatDisplay(new Customer("1", "Shreya")));
    }
}
