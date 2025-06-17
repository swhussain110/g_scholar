import os
import json
import csv
import math
from datetime import datetime

folder_path = r"data"
details = []
current_year = datetime.now().year

def calculate_g_index(citations):
    citations = sorted(citations, reverse=True)
    g = 0
    total = 0
    for i, c in enumerate(citations, 1):
        total += c
        if total >= i * i:
            g = i
        else:
            break
    return g

def calculate_hg_index(h, g):
    return math.sqrt(h * g)

def calculate_a_index(citations, h):
    if h == 0:
        return 0
    return sum(sorted(citations, reverse=True)[:h]) / h

def calculate_r_index(citations, h):
    return math.sqrt(sum(sorted(citations, reverse=True)[:h]))

def calculate_f_index(citations):
    citations_sorted = sorted(citations, reverse=True)
    f = 0
    for i, c in enumerate(citations_sorted, 1):
        if c >= i:
            f = i
        else:
            break
    return f

def calculate_p_index(total_citations, total_publications):
    if total_publications == 0:
        return 0
    return (total_citations ** 2 / total_publications) ** (1/3)

def calculate_pi_index(num_citations, hindex):
    p_list = []
    cumulative_citations = []
    if not num_citations:
        return hindex
    for i in range(len(num_citations)):
        if i == 0:
            p_list.append(1)
        else:
            p_list.append(p_list[-1] + (i + 1))
    for i, citation in enumerate(num_citations):
        if i == 0:
            cumulative_citations.append(citation)
        else:
            cumulative_citations.append(cumulative_citations[-1] + citation)
    current_index = 0
    for i in range(len(cumulative_citations)):
        if p_list[i] <= cumulative_citations[i]:
            current_index = i
    pi_index = current_index + 1
    if pi_index < hindex:
        pi_index = hindex
    return pi_index

def calculate_k_index(total_citations, citations, h):
    if h == 0 or len(citations) == 0:
        return 0
    citations_sorted = sorted(citations, reverse=True)
    h_core = sum(citations_sorted[:h])
    h_tail = sum(citations_sorted[h:])
    if h_core == 0:
        return 0
    return (total_citations / len(citations)) * (h_tail / h_core)

def calculate_e_index(citations, h):
    citations_sorted = sorted(citations, reverse=True)
    e = sum(citations_sorted[:h]) - h * h
    return math.sqrt(e) if e > 0 else 0

def calculate_m_quotient(h, first_pub_year):
    if not first_pub_year or h == 0:
        return 0
    years = current_year - int(first_pub_year) + 1
    if years <= 0:
        return 0
    return h / years

def calculate_ar_index(citations, h, first_pub_year):
    if not first_pub_year or h == 0:
        return 0
    years = current_year - int(first_pub_year) + 1
    if years <= 0:
        return 0
    return math.sqrt(sum(sorted(citations, reverse=True)[:h]) / years)

def calculate_q2_index(h, m):
    return math.sqrt(h * m)

def calculate_normalized_h_index(h, total_publications):
    if total_publications == 0:
        return 0
    return h / total_publications

def calculate_proposed_index(h, g, e):
    if h and g and e:
        return (h + g + e) / 3
    return 0

def calculate_hm_index(publications):
    citations = []
    frac_authors = []
    for pub in publications:
        n_authors = len(pub.get('bib', {}).get('author', '').split(',')) if pub.get('bib', {}).get('author') else 1
        citations.append(pub.get('num_citations', 0))
        frac_authors.append(1 / n_authors)
    sorted_items = sorted(zip(citations, frac_authors), key=lambda x: x[0], reverse=True)
    sum_frac = 0
    hm = 0
    for i, (c, f) in enumerate(sorted_items):
        sum_frac += f
        if c >= sum_frac:
            hm = sum_frac
        else:
            break
    return round(hm, 2)

def calculate_hi_index(publications, h):
    if h == 0:
        return 0
    sorted_pubs = sorted(publications, key=lambda x: x.get('num_citations', 0), reverse=True)[:h]
    total_authors = 0
    for pub in sorted_pubs:
        n_authors = len(pub.get('bib', {}).get('author', '').split(',')) if pub.get('bib', {}).get('author') else 1
        total_authors += n_authors
    avg_authors = total_authors / h if h > 0 else 1
    return round(h / avg_authors, 3) if avg_authors > 0 else 0

def calculate_hi_norm_index(publications, h):
    if h == 0:
        return 0
    total_authors = 0
    for pub in publications:
        n_authors = len(pub.get('bib', {}).get('author', '').split(',')) if pub.get('bib', {}).get('author') else 1
        total_authors += n_authors
    avg_authors = total_authors / len(publications) if publications else 1
    return round(h / avg_authors, 3) if avg_authors > 0 else 0

def calculate_aw_index(publications):
    aw = 0
    for pub in publications:
        pub_year = pub.get('bib', {}).get('pub_year')
        try:
            pub_year = int(pub_year)
            age = current_year - pub_year + 1
            if age > 0:
                aw += pub.get('num_citations', 0) / age
        except Exception:
            continue
    return round(aw, 2)

for filename in os.listdir(folder_path):
    h_core = 0
    num_citations = []
    data = {}

    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
            try:
                file_data = json.load(f)

                data['author_name'] = file_data.get('name', 'N/A')
                data['author_id'] = file_data.get('scholar_id', 'N/A')
                data['author_affiliation'] = file_data.get('affiliation', 'N/A')

                first_publication = None
                first_pub_year = None

                for publication in file_data.get('publications', []):
                    pub_year = publication.get('bib', {}).get('pub_year')
                    try:
                        pub_year = int(pub_year)
                        if 1900 <= pub_year <= current_year:
                            if first_pub_year is None or pub_year < first_pub_year:
                                first_pub_year = pub_year
                                first_publication = publication.get('bib', {}).get('title', 'N/A')
                    except (ValueError, TypeError):
                        continue

                if first_pub_year is None:
                    cites_per_year = file_data.get('cites_per_year', {})
                    if cites_per_year:
                        first_pub_year = min(int(year) for year in cites_per_year.keys())
                        first_publication = "Derived from cites_per_year"

                data['first_publication'] = first_publication if first_publication else 'N/A'
                data['first_pb_year'] = first_pub_year if first_pub_year else 'N/A'

                publications = file_data.get('publications', [])
                citations_list = [pub.get('num_citations', 0) for pub in publications]
                total_publications = len(publications)
                total_citations = sum(citations_list)

                # Total years since first publication
                if first_pub_year:
                    total_years = current_year - int(first_pub_year) + 1
                else:
                    total_years = 0

                cites_per_year = total_citations / total_years if total_years > 0 else 0
                cites_per_paper = total_citations / total_publications if total_publications > 0 else 0

                total_authors = 0
                for pub in publications:
                    n_authors = len(pub.get('bib', {}).get('author', '').split(',')) if pub.get('bib', {}).get('author') else 1
                    total_authors += n_authors
                authors_per_paper = total_authors / total_publications if total_publications > 0 else 0

                cites_per_author = 0
                for pub in publications:
                    n_authors = len(pub.get('bib', {}).get('author', '').split(',')) if pub.get('bib', {}).get('author') else 1
                    cites_per_author += pub.get('num_citations', 0) / n_authors

                papers_per_author = 0
                for pub in publications:
                    n_authors = len(pub.get('bib', {}).get('author', '').split(',')) if pub.get('bib', {}).get('author') else 1
                    papers_per_author += 1 / n_authors

                # H-index and related metrics
                hindex = int(file_data.get('hindex', 0))
                gindex = calculate_g_index(citations_list)
                hgindex = calculate_hg_index(hindex, gindex)
                aindex = calculate_a_index(citations_list, hindex)
                rindex = calculate_r_index(citations_list, hindex)
                findex = calculate_f_index(citations_list)
                pindex = calculate_p_index(total_citations, total_publications)
                # Pi-index (Ψ-Index)
                num_citations_pi = []
                for publication in publications:
                    pub_year = publication.get('bib', {}).get('pub_year')
                    try:
                        if pub_year and int(pub_year) <= 2019:
                            num_citations_pi.append(publication.get('num_citations', 0))
                    except ValueError:
                        continue
                psi_index = calculate_pi_index(num_citations_pi, hindex)
                kindex = calculate_k_index(total_citations, citations_list, hindex)
                eindex = calculate_e_index(citations_list, hindex)
                m_quotient = calculate_m_quotient(hindex, first_pub_year)
                ar_index = calculate_ar_index(citations_list, hindex, first_pub_year)
                q2_index = calculate_q2_index(hindex, m_quotient)
                normalized_h_index = calculate_normalized_h_index(hindex, total_publications)
                proposed_index = calculate_proposed_index(hindex, gindex, eindex)
                hm_index = calculate_hm_index(publications)
                hi_index = calculate_hi_index(publications, hindex)
                hi_norm = calculate_hi_norm_index(publications, hindex)
                aw_index = calculate_aw_index(publications)
                hc_index = sum(sorted(citations_list, reverse=True)[:hindex])
                hg_iindex = hgindex

                data['hcore'] = hc_index

                # Save all metrics
                data['citations'] = total_citations
                data['hindex'] = hindex
                data['gindex'] = gindex
                data['hgindex'] = round(hgindex, 2)
                data['aindex'] = round(aindex, 2)
                data['rindex'] = round(rindex, 2)
                data['findex'] = findex
                data['pindex'] = round(pindex, 2)
                data['Ψ-Index'] = psi_index
                data['kindex'] = round(kindex, 2)
                data['eindex'] = round(eindex, 2)
                data['M-quotient'] = round(m_quotient, 3)
                data['AR-index'] = round(ar_index, 3)
                data['Q2-Index'] = round(q2_index, 3)
                data['Normalized h-index'] = round(normalized_h_index, 3)
                data['Proposed index'] = round(proposed_index, 3)
                data['hm-index'] = hm_index
                data['hi-index'] = hi_index
                data['hi-norm'] = hi_norm
                data['AW-index'] = aw_index
                data['hc-index'] = hc_index
                data['hg-iIndex'] = round(hg_iindex, 2)
                data['total_publications'] = total_publications
                data['total_citations'] = total_citations
                data['total_years'] = total_years
                data['Cites-Year'] = round(cites_per_year, 2)
                data['Cites-Paper'] = round(cites_per_paper, 2)
                data['Authors-Paper'] = round(authors_per_paper, 2)
                data['cites_per_author'] = round(cites_per_author, 2)
                data['papers_per_author'] = round(papers_per_author, 2)
                data['total_pubs'] = total_publications

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error in file {filename}: {e}")
            finally:
                details.append(data)

fields = [
    "author_name", "author_id", "author_affiliation", "first_publication", "first_pb_year",
    "citations", "hindex", "gindex", "hgindex", "aindex", "rindex", "findex", "hcore", "hc-index",
    "pindex", "Ψ-Index", "kindex", "eindex", "M-quotient", "AR-index", "Q2-Index", "Normalized h-index", "Proposed index",
    "hm-index", "hi-index", "hi-norm", "AW-index", "hg-iIndex",
    "total_publications", "total_citations", "total_years", "Cites-Year", "Cites-Paper",
    "Authors-Paper", "cites_per_author", "papers_per_author", "total_pubs"
]

with open("output_pi.csv", "w", newline="", encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for row in details:
        writer.writerow(row)