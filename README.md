# 📚 Google Scholar Author Metrics Extractor

This project automates the extraction of author data from Google Scholar and computes **25 advanced bibliometric indices** for each author. It is designed for researchers, analysts, and institutions interested in comprehensive scholarly impact analysis.

---

## 🚀 Features

- **Automated Author Data Collection:**  
  Scrapes author profiles and publication data from Google Scholar using the [`scholarly`](https://github.com/scholarly-python-package/scholarly) library.

- **Comprehensive Metrics Calculation:**  
  Calculates 25 indices, including:
  - h-index, g-index, hc-index, hi-index, hi-norm, AW-index, e-index, hm-index, f-index, p-index, Ψ-Index, k-index, M-quotient, AR-index, Q2-Index, Normalized h-index, Proposed index, A-index, R-index, hg-Index, Cites-Year, Authors-Paper, Cites-Paper, Publication count, Citation count.

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

## 📊 Output

- **output_pi.csv:**

  1. h-index  
  2. g-index  
  3. hc-index  
  4. hi-index  
  5. hi-norm  
  6. AW-index  
  7. e-index  
  8. hm-index  
  9. f-index  
  10. p-index  
  11. Ψ-Index  
  12. k-index  
  13. M-quotient  
  14. AR-index  
  15. Q2-Index  
  16. Normalized h-index  
  17. Proposed Index  
  18. a-index  
  19. R-index  
  20. hg-Index  
  21. Cites-Year  
  22. Authors-Paper  
  23. Cites-Paper  
  24. Publication count  
  25. Citation count  

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