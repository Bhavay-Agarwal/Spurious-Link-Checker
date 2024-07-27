# Spurious Link Checker

Spurious Link Checker is a web application that allows users to check the safety of links using three levels of scans:
1. **Quick Scan:** Lexical Analysis
2. **Moderate Scan:** Web Content Analysis
3. **Deep Scan:** DNS Lookup

The application uses AI models to classify links as safe or not safe.

## Technologies Used

- **Frontend:**
  - HTML
  - CSS
  - Vanilla JS

- **Backend:**
  - Rest API
  - Python `urllib` for Lexical Analysis
  - `BeautifulSoup` for Web Content Analysis
  - `whois` for DNS Lookup
  - `Helmet.js` for securing HTTP headers

## Features

- **Quick Scan:** 
  - Performs a lexical analysis on the URL to identify potentially harmful patterns.
  
- **Moderate Scan:**
  - Analyzes the web content of the URL to detect malicious content.
  
- **Deep Scan:**
  - Conducts a DNS lookup to verify the authenticity of the domain.

## Acknowledgements

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [whois](https://pypi.org/project/whois/)
- [Helmet.js](https://helmetjs.github.io/)

## Contact

- **Author:** Bhavay Agarwal
- **Email:** bhavayagarwal0103@gmail.com
- **GitHub:** [Bhavay-Agarwal](https://github.com/Bhavay-Agarwal)
