package com.verafin.legacy;

import com.verafin.commons.jdo.LegacyJdoManager;
import com.verafin.commons.jdo.LegacyQueries;

public class CustomerDao {
    private final LegacyJdoManager jdo;

    public CustomerDao(LegacyJdoManager jdo) {
        this.jdo = jdo;
    }

    public String buildFindByIdQuery(String id) {
        // demo purpose: we’re not executing against DB yet
        return LegacyQueries.byCustomerId(id);
    }
}
