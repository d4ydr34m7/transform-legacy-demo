package com.verafin.commons.jdo;

public class LegacyQueries {
    public static String byCustomerId(String id) {
        // pretend this string later gets fed into JDO/Kodo query engine
        return "SELECT FROM com.verafin.legacy.Customer WHERE id == '" + id + "'";
    }
}
