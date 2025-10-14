package Job_Search;

public class Scraper {
    public static void main(String[] args) {
        printWelcome();
    }

    private static void printWelcome() {
        String[] art = {
            "  _____       _     _____                      _                 ",
            " |_   _|     | |   /  ___|                    | |                ",
            "   | |  _ __ | |_  \\ `--.  ___  ___ _ ____   _| | ___  _ __ ___  ",
            "   | | | '_ \\| __|  `--. \\/ _ \\/ __| '__\\ \\ / / |/ _ \\| '__/ _ \\ ",
            "  _| |_| | | | |_  /\\__/ /  __/ (__| |   \\ V /| | (_) | | |  __/ ",
            " |_____|_| |_|\\__| \\____/ \\___|\\___|_|    \\_/ |_|\\___/|_|  \\___| ",
            "                                                                  ",
            "                  JOB SEARCH SCRAPER - v1.0                       "
        };

        System.out.println();
        for (String line : art) System.out.println(line);
        System.out.println();
        System.out.println("Welcome to the Job Search Scraper");
        System.out.println("------------------------------------------------------------");
        System.out.println("Purpose: This application scrapes job listings from configured");
        System.out.println("sources, normalizes and deduplicates results, and stores them");
        System.out.println("for searching, analysis, and downstream automation.");
        System.out.println();
        System.out.println("Usage: configure sources and run this scraper to build a");
        System.out.println("searchable dataset of job postings for your workflows.");
        System.out.println("------------------------------------------------------------");
        System.out.println();
    }
}