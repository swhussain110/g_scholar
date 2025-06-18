# 📚 Google Scholar Author Metrics Extractor

This project automates the extraction of author data from Google Scholar and computes **25 advanced bibliometric indices** for each author. It is designed for researchers, analysts, and institutions interested in comprehensive scholarly impact analysis.

---

## 🚀 Features

- **Automated Author Data Collection:**  
  Scrapes author profiles and publication data from Google Scholar using the [`scholarly`](https://github.com/scholarly-python-package/scholarly) library.

- **Comprehensive Metrics Calculation:**  
  Calculates 25 indices, including:
  - h-index, g-index, hg-index (h × g), hc-index, hi-index, hi-norm, AW-index, e-index, hm-index, f-index, p-index, Ψ-Index (Pi-index), k-index, M-quotient, AR-index, Q2-Index, Normalized h-index, Proposed index, a-index, r-index, hg-iIndex, Cites-Year, Authors-Paper, Cites-Paper, total publications, total citations, and more.

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

- **output_pi.csv:** Contains the following columns for each author (among others):

  | Metric Name          | Description |
  |----------------------|-------------|
  | Publication count    | Total number of publications |
  | Citation count       | Total number of citations |
  | h-index              | h-index |
  | hc-index             | h-core index (sum of citations in h-core) |
  | hi-index             | Individual h-index (normalized by authors in h-core) |
  | hi-norm              | Normalized h-index (by authors per paper) |
  | AW-index             | Age-weighted citation rate |
  | e-index              | e-index (excess citations in h-core) |
  | g-index              | g-index |
  | hm-index             | Multi-author h-index |
  | Cites-Year           | Citations per year since first publication |
  | Authors-Paper        | Average authors per paper |
  | Cites-Paper          | Average citations per paper |
  | hg-iIndex            | hg-index (product of h and g) |
  | A-index              | Average citations in h-core |
  | R-index              | sqrt(sum of h-core citations) |
  | f-index              | f-index |
  | p-index              | p-index |
  | Ψ-Index         | Pi-index (Psi-index) |
  | k-index              | k-index |
  | M-quotient           | h-index / academic age |
  | AR-index             | sqrt(h-core citations / academic age) |
  | Q2-Index             | sqrt(h-index * m-quotient) |
  | Normalized h-index   | h-index / total publications |
  | Proposed index       | (h + g + e) / 3 |
 

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