#!/usr/bin/env python3
"""
scraper.py - displays ASCII welcome and app purpose for the Job_Search project.

Usage: python3 scraper.py
"""

ASCII = r'''
  ____  _           _                 
 / ___|| | ___  ___| |_ _   _ _ __ ___ 
 \\___ \| |/ _ \/ __| __| | | | '__/ _ \
  ___) | |  __/ (__| |_| |_| | | |  __/\n |____/|_|\___|\___|\__|\__,_|_|  \___|\n'''

def main():
    print(ASCII)
    print()
    print("Welcome to the Job_Search mini-site project!")
    print()
    print("This small app demonstrates a 4-page static website (me.html, xula.html, dillard.html, other_university.html)")
    print("that share a single CSS stylesheet. It uses images and styles to showcase basic HTML/CSS concepts.")
    print()
    print("What this script does (TODO 3 & 4):")
    print("- Displays a pleasant ASCII-art welcome message")
    print("- Explains the purpose of the app: to demonstrate a 4-page static site sharing one CSS file and images")
    print()
    print("Status of TODOs:")
    print("- TODO 1: Complete the W3Schools 'What is HTML/CSS' tutorial (student action)")
    print("- TODO 2: Completed — the 4 HTML pages and shared style.css are included in the repo")
    print("- TODO 3: This script prints the ASCII welcome message (done)")
    print("- TODO 4: This script prints an explanation of the app's purpose (done)")
    print()
    print("Run this script with: python3 scraper.py")

if __name__ == '__main__':
    main()
