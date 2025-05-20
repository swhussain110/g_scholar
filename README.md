# 📚 Google Scholar Author Scraper & Metrics Calculator

This project automates the process of collecting author data from Google Scholar and computes advanced bibliometric indices such as the H-index, H-core, and Pi-index. It is designed for researchers, analysts, and institutions interested in analyzing scholarly impact.

---

## 🚀 Features

- **Automated Author Data Collection:**  
  Scrapes author profiles and publication data from Google Scholar using the [`scholarly`](https://github.com/scholarly-python-package/scholarly) library.

- **Advanced Metrics Calculation:**  
  Computes H-index, H-core, Pi-index, total citations, and more for each author.

- **Batch Processing:**  
  Reads a list of authors from a CSV file and processes them in bulk.

- **Structured Output:**  
  Saves detailed author data as JSON and summary metrics as a CSV file for easy analysis.

---

## 📂 Project Structure

```
.
├── output.py           # Processes JSON data and computes metrics
├── scrape.py           # Scrapes author data from Google Scholar
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── data/               # Folder for JSON files and intermediate data
│   └── searched_authors.json
└── output_pi.csv       # Final output with computed metrics
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/swhussain110/g_scholar.git
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
  Contains the following columns for each author:
  - `author_name`
  - `author_id`
  - `author_affiliation`
  - `first_publication`
  - `first_pb_year`
  - `citations`
  - `hindex`
  - `i10index`
  - `hcore`
  - `total_pubs`
  - `pi`

---

## 📝 Requirements

- Python 3.7+
- scholarly==1.7.11
- pandas==2.2.2

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
