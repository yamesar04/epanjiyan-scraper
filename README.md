# Rajasthan e-Search Scraper

This repository contains work-in-progress Python scripts designed to automate interactions with the Rajasthan e-Search portal at [https://epanjiyan.rajasthan.gov.in/e-search-page.aspx](https://epanjiyan.rajasthan.gov.in/e-search-page.aspx). The primary goal is to simulate user interactions—such as selecting location types and regions—and extract the underlying form parameters necessary for navigation and data retrieval from the site.

## Overview

The repository currently includes two distinct approaches:

### Approach 1 (`approach-1.py`)
- **Session Parameter Extraction:**  
  Extracts initial session parameters (like `__VIEWSTATE` and `__EVENTVALIDATION`) from the page.
- **Form Interaction Simulation:**  
  Prepares and updates the payload to simulate form submissions that reflect user selections (e.g., choosing a location type or district).
- **CAPTCHA Handling (Planned):**  
  Contains a placeholder for CAPTCHA decoding functionality using Tesseract, which is yet to be implemented.

### Approach 2 – SignalR Based (`approach-2-signalr.py`)
- **SignalR Communication:**  
  Implements a SignalR handshake to negotiate a connection with the server, maintaining the connection via long polling.
- **Sequential Form Actions:**  
  Simulates a multi-step form interaction: starting with selecting a rural option, choosing a district (e.g., AJMER), and then fetching and selecting Tehsil options.
- **State Management:**  
  Parses dynamic form states and validates that the selections persist correctly in the updated DOM.

> **Note:** Both approaches are under active development and do not yet fully work. They serve as prototypes to explore different strategies for navigating the e-Search site's form interactions.

## Features

- **Dynamic Session Handling:**  
  Retrieve and update hidden form parameters required by the website.
  
- **Simulated User Interaction:**  
  Automate the process of selecting options (location type, district, tehsil, etc.) as if a user were interacting with the form.
  
- **Real-Time Communication (Approach 2):**  
  Use SignalR to maintain a live connection with the server, facilitating a real-time update of session states.

- **Planned CAPTCHA Decoding:**  
  Future work includes integrating Tesseract OCR to decode CAPTCHA challenges.

## Requirements

- **Python:** 3.7 or later
- **Libraries:**
  - `requests`
  - `beautifulsoup4`
  - `lxml` (optional, for faster HTML parsing)
  - `pytesseract` (planned for future CAPTCHA decoding)

Install dependencies via pip:

```bash
pip install requests beautifulsoup4 lxml pytesseract
