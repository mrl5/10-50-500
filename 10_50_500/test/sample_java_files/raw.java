package com.tuxnet.utils;
import java.util.*;
public class Test {
    public static void main(String[] args) {
        Bash bash = new Bash();
        Integer test = 0;
        if (true) {
            for (String line : bash.verboseCmd("ls -la")) {
                System.out.println(line);
            }
        } else
            System.out.println("false");
        bash.quiet("uname -a");
        try {
            bash.quiet("ping www.github.com");
        } catch (NullPointerException e) {
            System.err.println("test");
            System.err.println("{we {{ are doomed {{{{");
            System.err.println("test");
            System.err.println("}}}}}}}}}}there is }}}}}}}}}}}}}stil hope }}}}}}}}}}}}}}");
            System.err.println("test");
            System.err.println('{' + '{' + '{' + '{');
            System.err.println("test");
            System.err.println('}' + '}' + '}' + '}' + '}' + '}' + '}' + '}' + '}' + '}' + '}' + '}' + '}');
            System.err.println("test");
        }
        switch (test) {
            case 0:
                String test2 = "something something";
                String s = test2.toString();
                break;
            default:
                String test3 = "right";
                break;
            case 1:
                boolean worked = test.toString()
                        .endsWith("1");
                break;
        }
    }
    private void yeah() {
        Integer test = 0;
        final int exit = 0;
        final int tickersDBPath = 1;
        final int tickersDBUsername = 2;
        final int tickersDBPassword = 3;
        final int cleanTickersDatabase = 4;
        final Map<Integer, String> options = new TreeMap<Integer, String>() {{
            put(tickersDBPath, String.valueOf(tickersDBPath) + ": path to database");
            put(tickersDBUsername, String.valueOf(tickersDBUsername) + ": change username");
            put(tickersDBPassword, String.valueOf(tickersDBPassword) + ": change password");
            put(cleanTickersDatabase, String.valueOf(cleanTickersDatabase) + ": clean JInvestor local database");
            put(exit, String.valueOf(exit) + ": go back to \"Database settings\" menu");
        }};
        final String submenuTitle = "\n### JInvestor local database settings";
        switch (test) {
            case 0:
                String test2 = "something something";
                String s = test2.toString();
                break;
            case 1:
                boolean worked = test.toString()
                        .endsWith("1");
                break;
            default:
                String test3 = "right";
        }
        String sqlStatement = "SELECT tickers.id_ticker, tickers.symbol, tickers.name, currencies.symbol AS currency, " +
                "cat_main.name AS category, cat_subcat.name AS subcategory, " +
                "tickers.stooq_symbol, tickers.yahoo_symbol FROM tickers " +
                "INNER JOIN currencies ON  tickers.currency=currencies.id_currency " +
                "INNER JOIN cat_main ON tickers.category=cat_main.id_category " +
                "INNER JOIN cat_subcat ON tickers.subcategory=cat_subcat.id_subcat " +
                "ORDER BY tickers.id_ticker ASC";
    }
}
