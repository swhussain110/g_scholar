import os
import json
import csv
from datetime import datetime
import math

# Define the path to the folder containing the JSON files
folder_path = r"data/sample"

details = []

# Get the current year
current_year = datetime.now().year

def get_first_publication(publications, cites_per_year):
    first_publication = None
    first_pub_year = None
    for publication in publications:
        pub_year = publication.get('bib', {}).get('pub_year')
        try:
            pub_year_int = int(pub_year)
            if 1900 <= pub_year_int <= current_year:
                if first_pub_year is None or pub_year_int < first_pub_year:
                    first_pub_year = pub_year_int
                    first_publication = publication.get('bib', {}).get('title', 'N/A')
        except (ValueError, TypeError):
            continue
    if first_pub_year is None and cites_per_year:
        try:
            first_pub_year = min(int(year) for year in cites_per_year.keys())
            first_publication = "Derived from cites_per_year"
        except Exception:
            first_pub_year = 'N/A'
            first_publication = 'N/A'
    return first_publication if first_publication else 'N/A', first_pub_year if first_pub_year else 'N/A'

def calculate_hcore(publications, h_index):
    h_core = 0
    if h_index > 0:
        for pub in publications[:h_index]:
            h_core += pub.get('num_citations', 0)
    return h_core

def get_num_citations(publications, year_limit=2019):
    num_citations = []
    for publication in publications:
        pub_year = publication.get('bib', {}).get('pub_year')
        try:
            pub_year_int = int(pub_year)
            if pub_year_int <= year_limit:
                num_citations.append(publication.get('num_citations', 0))
        except (ValueError, TypeError):
            continue
    return num_citations

def calculate_pi_index(num_citations, h_index):
    p_list = []
    cumulative_citations = []
    if not num_citations:
        return 0, p_list, cumulative_citations
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
    if pi_index < h_index:
        pi_index = h_index
    return pi_index, p_list, cumulative_citations

def count_all_publications(publications):
    """Returns the total number of publications, regardless of year."""
    return len(publications)

def calculate_e_index(hcore, hindex):
    """Calculate the e-index given hcore and hindex."""
    value = hcore - hindex ** 2
    return round(math.sqrt(value), 2) if value > 0 else 0.0

def calculate_cite_year(total_citations, first_pub_year, current_year):
    try:
        years = int(current_year) - int(first_pub_year)
        if years > 0:
            return round(total_citations / years, 2)
        else:
            return total_citations  # If only one year, return total citations
    except Exception:
        return 0.0

def calculate_authors_paper(publications):
    total_authors = 0
    total_pubs = len(publications)
    for pub in publications:
        authors = pub.get('bib', {}).get('author', '')
        if isinstance(authors, str):
            # Google Scholar uses ' and ' as separator
            author_list = [a.strip() for a in authors.split(' and ') if a.strip()]
            total_authors += len(author_list)
        elif isinstance(authors, list):
            total_authors += len(authors)
    if total_pubs > 0:
        return round(total_authors / total_pubs, 2)
    else:
        return 0.0

def calculate_cites_paper(total_citations, total_pubs):
    if total_pubs > 0:
        return round(total_citations / total_pubs, 2)
    else:
        return 0.0

def calculate_g_index(publications):
    # Get citation counts for all publications
    citations = [pub.get('num_citations', 0) for pub in publications]
    citations.sort(reverse=True)
    cumulative = 0
    g_index = 0
    for i, c in enumerate(citations, 1):
        cumulative += c
        if cumulative >= i * i:
            g_index = i
        else:
            break
    return g_index

def calculate_hg_index(hindex, gindex):
    return hindex * gindex

def calculate_a_index(hcore, hindex):
    if hindex > 0:
        return round(hcore / hindex, 2)
    else:
        return 0.0

def calculate_r_index(hcore):
    return round(math.sqrt(hcore), 2) if hcore > 0 else 0.0

def calculate_f_index(publications):
    citations = sorted([pub.get('num_citations', 0) for pub in publications], reverse=True)
    f_index = 0
    for i, c in enumerate(citations, 1):
        if c >= 2 * i:
            f_index = i
        else:
            break
    return f_index

def calculate_p_index(total_citations, total_pubs):
    try:
        if total_pubs > 0:
            value = (total_citations ** 2) / total_pubs
            return round(value ** (1/3), 2)
        else:
            return 0.0
    except Exception:
        return 0.0

def calculate_k_index(total_citations, total_pubs, hcore):
    try:
        if total_pubs > 0 and hcore > 0:
            return round((total_citations / total_pubs) * ((total_citations - hcore) / hcore), 2)
        else:
            return 0.0
    except Exception:
        return 0.0

def calculate_m_quotient(hindex, first_pub_year, current_year):
    try:
        age = int(current_year) - int(first_pub_year)
        if age > 0:
            return hindex / age
        else:
            return 0.0
    except Exception:
        return 0.0
    

def calculate_ar_index(hcore, first_pub_year, current_year):
    try:
        age = int(current_year) - int(first_pub_year)
        if age > 0 and hcore > 0:
            return round(math.sqrt(hcore / age), 2)
        else:
            return 0.0
    except Exception:
        return 0.0

def calculate_m_index(publications, hindex):
    if hindex > 0 and len(publications) >= hindex:
        # Get the citation counts of the h-core (top h) papers
        hcore_citations = sorted(
            [pub.get('num_citations', 0) for pub in publications],
            reverse=True
        )[:hindex]
        hcore_citations.sort()
        n = len(hcore_citations)
        if n % 2 == 1:
            return hcore_citations[n // 2]
        else:
            return round((hcore_citations[n // 2 - 1] + hcore_citations[n // 2]) / 2, 2)
    else:
        return 0.0

def calculate_q2_index(hindex, m_index):
    try:
        value = hindex * m_index
        return round(math.sqrt(value), 2) if value > 0 else 0.0
    except Exception:
        return 0.0
def calculate_normalized_h_index(hindex, total_pubs):
    if total_pubs > 0:
        return round(hindex / total_pubs, 3)
    else:
        return 0.0

def calculate_proposed_index(hindex, gindex, first_pub_year, current_year):
    try:
        age = int(current_year) - int(first_pub_year)
        if age > 0:
            return round((hindex * gindex) / age, 2)
        else:
            return 0.0
    except Exception:
        return 0.0


def calculate_hc_index(publications, current_year, gamma=4, delta=1):
    scores = []
    for pub in publications:
        pub_year = pub.get('bib', {}).get('pub_year')
        citations = pub.get('num_citations', 0)
        try:
            pub_year = int(pub_year)
            age = current_year - pub_year + 1
            score = gamma * (age ** -delta) * citations
            scores.append(score)
        except (ValueError, TypeError):
            continue
    scores.sort(reverse=True)
    hc_index = 0
    for i, score in enumerate(scores, 1):
        if score >= i:
            hc_index = i
        else:
            break
    return hc_index

def calculate_hi_index(hindex, avg_authors_per_paper):
    if avg_authors_per_paper > 0:
        return round(hindex / avg_authors_per_paper, 2)
    else:
        return 0.0

def calculate_hi_norm(publications):
    # Calculate normalized citations for each paper
    norm_citations = []
    for pub in publications:
        citations = pub.get('num_citations', 0)
        authors = pub.get('bib', {}).get('author', '')
        if isinstance(authors, str):
            author_list = [a.strip() for a in authors.split(' and ') if a.strip()]
            n_authors = len(author_list)
        elif isinstance(authors, list):
            n_authors = len(authors)
        else:
            n_authors = 1
        if n_authors > 0:
            norm_citations.append(citations / n_authors)
        else:
            norm_citations.append(0)
    # Sort normalized citations in descending order
    norm_citations.sort(reverse=True)
    # Find the largest h such that sum of top h normalized citations >= h
    hl_norm = 0
    for h in range(1, len(norm_citations) + 1):
        if sum(norm_citations[:h]) >= h:
            hl_norm = h
        else:
            break
    return hl_norm

import math

def calculate_aw_index(publications, hindex):
    if hindex == 0:
        return 0.0
    # Get top h papers by citations
    hcore_pubs = sorted(publications, key=lambda x: x.get('num_citations', 0), reverse=True)[:hindex]
    sum_cit_div_auth = 0.0
    for pub in hcore_pubs:
        citations = pub.get('num_citations', 0)
        authors = pub.get('bib', {}).get('author', '')
        if isinstance(authors, str):
            author_list = [a.strip() for a in authors.split(' and ') if a.strip()]
            n_authors = len(author_list)
        elif isinstance(authors, list):
            n_authors = len(authors)
        else:
            n_authors = 1
        if n_authors > 0:
            sum_cit_div_auth += citations / n_authors
    return round(math.sqrt(sum_cit_div_auth), 2) if sum_cit_div_auth > 0 else 0.0

def calculate_hm_index(publications):
    # Sort publications by citations descending
    sorted_pubs = sorted(publications, key=lambda x: x.get('num_citations', 0), reverse=True)
    fractional_sum = 0.0
    hm_index = 0
    for i, pub in enumerate(sorted_pubs):
        authors = pub.get('bib', {}).get('author', '')
        if isinstance(authors, str):
            author_list = [a.strip() for a in authors.split(' and ') if a.strip()]
            n_authors = len(author_list)
        elif isinstance(authors, list):
            n_authors = len(authors)
        else:
            n_authors = 1
        if n_authors > 0:
            fractional_sum += 1 / n_authors
        if fractional_sum >= i + 1:
            hm_index = i + 1
        else:
            break
    return hm_index

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    data = {}
    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename)) as f:
            try:
                file_data = json.load(f)
                publications = file_data.get('publications', [])
                cites_per_year = file_data.get('cites_per_year', {})

                data['author_name'] = file_data.get('name', 'N/A')
                data['author_id'] = file_data.get('scholar_id', 'N/A')
                data['author_affiliation'] = file_data.get('affiliation', 'N/A')

                # First publication and year
                first_publication, first_pub_year = get_first_publication(publications, cites_per_year)
                data['first_publication'] = first_publication
                data['first_pb_year'] = first_pub_year

                data['citations'] = int(file_data.get('citedby', 0))
                data['hindex'] = int(file_data.get('hindex', 0))
                data['i10index'] = int(file_data.get('i10index', 0))

                # H-core
                data['hcore'] = calculate_hcore(publications, data['hindex'])
                data['total_pubs'] = len(publications)

                # Pi-index and related lists
                num_citations = get_num_citations(publications, year_limit=2019)
                pi_index, p_list, cumulative_citations = calculate_pi_index(num_citations, data['hindex'])
                data['pi'] = pi_index

                # Publication count for all years
                data['pubs_all_time'] = count_all_publications(publications)


                # E-index
                data['eindex'] = calculate_e_index(data['hcore'], data['hindex'])

                # cite_year
                data['cite_year'] = calculate_cite_year(
                    data['citations'],
                    data['first_pb_year'] if data['first_pb_year'] != 'N/A' else current_year,
                    current_year
                )

                #authors_paper

                data['authors_paper'] = calculate_authors_paper(publications)

                # cites_paper
                data['cites_paper'] = calculate_cites_paper(data['citations'], data['total_pubs'])
                
                #g_index
                data['gindex'] = calculate_g_index(publications)


                # hg_index
                data['hg_index'] = calculate_hg_index(data['hindex'], data['gindex'])

                # a_index
                data['a_index'] = calculate_a_index(data['hcore'], data['hindex'])

                # r_index
                data['r_index'] = calculate_r_index(data['hcore'])

                # f_index
                data['f_index'] = calculate_f_index(publications)

                # p_index
                data['p_index'] = calculate_p_index(data['citations'], data['total_pubs'])

                # k_index
                data['k_index'] = calculate_k_index(data['citations'], data['total_pubs'], data['hcore'])

                # m_quotient
                data['m_quotient'] = calculate_m_quotient(
                    data['hindex'],
                    data['first_pb_year'] if data['first_pb_year'] != 'N/A' else current_year,
                    current_year
                )

                data['ar_index'] = calculate_ar_index(
                    data['hcore'],
                    data['first_pb_year'] if data['first_pb_year'] != 'N/A' else current_year,
                    current_year
                )

                m_index = calculate_m_index(publications, data['hindex'])

                # q2_index
                data['q2_index'] = calculate_q2_index(data['hindex'], m_index)

                # Normalized h-index
                data['normalized_h_index'] = calculate_normalized_h_index(data['hindex'], data['total_pubs'])

                data['proposed_index'] = calculate_proposed_index(
                    data['hindex'],
                    data['gindex'],
                    data['first_pb_year'] if data['first_pb_year'] != 'N/A' else current_year,
                    current_year
                )

                # HC-index
                data['hc_index'] = calculate_hc_index(publications, current_year)

                # Hi-index
                data['hi_index'] = calculate_hi_index(data['hindex'], data['authors_paper'])

                data['hl_norm'] = calculate_hi_norm(publications)

                data['aw_index'] = calculate_aw_index(publications, data['hindex'])


                data['hm_index'] = calculate_hm_index(publications)




            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error in file {filename}: {e}")
            finally:
                details.append(data)

# Save the results to a CSV file
fields = [
    "author_name", "author_id", "author_affiliation", "first_publication", "first_pb_year",
    "citations", "hindex", "gindex", "hg_index", "i10index", "hcore", "eindex", "a_index", "aw_index", "r_index",
    "f_index", "p_index", "k_index", "m_quotient", "ar_index", "m_index", "q2_index", "normalized_h_index",
    "proposed_index", "hi_index", "hi_norm", "hl_norm", "hc_index", "hm_index", "total_pubs", "pi", "pubs_all_time",
    "cite_year", "authors_paper", "cites_paper"
]

with open("output_pi.csv", "w", newline="", encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for row in details:
        writer.writerow(row)