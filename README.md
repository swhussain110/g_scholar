# 📚 Google Scholar Author Metrics Extractor

This project automates the extraction of author data from Google Scholar and computes **25 advanced bibliometric indices** for each author. It is designed for researchers, analysts, and institutions interested in comprehensive scholarly impact analysis.

---

## 🚀 Features

- **Automated Author Data Collection:**  
  Scrapes author profiles and publication data from Google Scholar using the [`scholarly`](https://github.com/scholarly-python-package/scholarly) library.

- **Comprehensive Metrics Calculation:**  
  Calculates 25 indices, including:
  - h-index, g-index, hc-index, hi-index, hi-norm, AW-index, e-index, hm-index, f-index, p-index, Ψ-Index , k-index, M-quotient, AR-index, Q2-Index, Normalized h-index, Proposed index, a-index, r-index, hg-Index, Cites-Year, Authors-Paper, Cites-Paper, Publication count, Citation count.

- **Batch Processing:**  
  Reads a list of authors from a CSV file and processes them in bulk.

- **Structured Output:**  
  Saves detailed author data as JSON and summary metrics as a CSV file for easy analysis.

---

## 📂 Project Structure

```
.
├── output.py           # Processes JSON data and computes all metrics
├── scrape.py           # Scrapes author data from Google Scholar
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── data/               # Folder for JSON files and intermediate data
│   └── [author_id].json
└── output_pi.csv       # Final output with computed metrics
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/g_scholar.git
   cd g_scholar
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## 📑 Usage

1. **Prepare your input:**
   - Create a `data.csv` file with an `Author` column listing the names of authors you want to analyze.

2. **Scrape author data:**
   ```sh
   python scrape.py
   ```
   - This will create individual JSON files for each author in the `data/` directory.

3. **Compute metrics and generate output:**
   ```sh
   python output.py
   ```
   - The results will be saved in `output_pi.csv`.

---

# 📊 Output

- **output_pi.csv:**

1. hindex  
2. gindex  
3. hgindex  
4. hc-index  
5. hi-index  
6. hi-norm  
7. AW-index  
8. eindex  
9. hm-index  
10. findex  
11. pindex  
12. Ψ-Index  
13. kindex  
14. M-quotient  
15. AR-index  
16. Q2-Index  
17. Normalized h-index  
18. Proposed index  
19. aindex  
20. rindex  
21. hg-iIndex  
22. Cites-Year  
23. Authors-Paper  
24. Cites-Paper  
25. total_publications  
26. total_citations  
27. total_years  
28. cites_per_author  
29. papers_per_author  
30.
 

---

## 📝 Requirements

- Python 3.7+
- scholarly
- pandas

Install all dependencies with:
```sh
pip install -r requirements.txt
```

---

## 🙏 Acknowledgements

- [scholarly](https://github.com/scholarly-python-package/scholarly) for Google Scholar scraping.
- [pandas](https://pandas.pydata.org/) for data manipulation.

---

## 📬 License

This project is for educational and research purposes only. Please respect Google Scholar's terms of service.