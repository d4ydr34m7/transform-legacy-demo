package com.verafin.legacy;

import com.verafin.commons.jdo.LegacyJdoManager;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

class CustomerDaoTest {
    @Test
    void buildsLegacyQuery() {
        CustomerDao dao = new CustomerDao(new LegacyJdoManager());
        String q = dao.buildFindByIdQuery("123");
        assertTrue(q.contains("Customer"));
        assertTrue(q.contains("id =="));
    }
}
