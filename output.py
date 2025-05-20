import os
import json
import csv
from datetime import datetime

# Define the path to the folder containing the JSON files
folder_path = r"data"

details = []

# Get the current year
current_year = datetime.now().year

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    h_core = 0
    num_citations = []
    data = {}
    p_list = []
    cumulative_citations = []

    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the file and load the JSON data
        with open(os.path.join(folder_path, filename)) as f:
            try:
                file_data = json.load(f)

                # Extract basic author details
                data['author_name'] = file_data.get('name', 'N/A')
                data['author_id'] = file_data.get('scholar_id', 'N/A')
                data['author_affiliation'] = file_data.get('affiliation', 'N/A')

                # Get the first publication year and title
                first_publication = None
                first_pub_year = None

                # Check publications for valid years
                for publication in file_data.get('publications', []):
                    pub_year = publication.get('bib', {}).get('pub_year')
                    try:
                        # Convert pub_year to an integer and validate it
                        pub_year = int(pub_year)
                        if 1900 <= pub_year <= current_year:  # Ensure the year is valid
                            if first_pub_year is None or pub_year < first_pub_year:
                                first_pub_year = pub_year
                                first_publication = publication.get('bib', {}).get('title', 'N/A')
                    except (ValueError, TypeError):
                        # Skip publications with invalid or missing pub_year
                        continue

                # Fallback to cites_per_year if no valid publication year is found
                if first_pub_year is None:
                    cites_per_year = file_data.get('cites_per_year', {})
                    if cites_per_year:
                        first_pub_year = min(int(year) for year in cites_per_year.keys())
                        first_publication = "Derived from cites_per_year"

                data['first_publication'] = first_publication if first_publication else 'N/A'
                data['first_pb_year'] = first_pub_year if first_pub_year else 'N/A'

                # Print the first publication and year
                print(f"First Publication: {data['first_publication']}")
                print(f"First Publication Year: {data['first_pb_year']}")

                data['citations'] = int(file_data.get('citedby', 0))
                data['hindex'] = int(file_data.get('hindex', 0))
                data['i10index'] = int(file_data.get('i10index', 0))

                # Calculate H-core
                h_index = file_data.get("hindex", 0)
                if h_index > 0:
                    for pub in file_data.get('publications', [])[:h_index]:
                        h_core += pub.get('num_citations', 0)
                data['hcore'] = h_core
                data['total_pubs'] = len(file_data.get('publications', []))

                # Get num_citations for publications with pub_year <= 2019
                for publication in file_data.get('publications', []):
                    pub_year = publication.get('bib', {}).get('pub_year')
                    try:
                        if pub_year and int(pub_year) <= 2019:
                            num_citations.append(publication.get('num_citations', 0))
                            print("Pub Year:", pub_year)
                    except ValueError:
                        print(f"Invalid pub_year: {pub_year}")

                # Check if num_citations is empty
                if not num_citations:
                    print(f"No publications with pub_year <= 2019 found for {data['author_name']}.")
                    data['pi'] = 0  # Set Pi index to 0 if no valid publications
                else:
                    # Pi calculation
                    for i in range(len(num_citations)):
                        if i == 0:
                            p_list.append(1)  # Start with 1
                        else:
                            p_list.append(p_list[-1] + (i + 1))

                    # Cumulative sum for num_citations
                    for i, citation in enumerate(num_citations):
                        if i == 0:
                            cumulative_citations.append(citation)
                        else:
                            cumulative_citations.append(cumulative_citations[-1] + citation)

                    # Calculate Pi index
                    current_index = 0
                    for i in range(len(cumulative_citations)):
                        if p_list[i] <= cumulative_citations[i]:
                            current_index = i
                            print(f"Less at index {i}: p_list[i] = {p_list[i]}, cumulative_citations[i] = {cumulative_citations[i]}")

                    # Ensure Pi-index is at least equal to H-index
                    pi_index = current_index + 1
                    if pi_index < data['hindex']:
                        print(f"Adjusting Pi-index from {pi_index} to match H-index {data['hindex']}")
                        pi_index = data['hindex']

                    data['pi'] = pi_index

                print("Num citations:", num_citations)
                print("P list:", p_list)
                print("Cumulative citations:", cumulative_citations)
                print("Pi index:", data['pi'])

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error in file {filename}: {e}")
            finally:
                details.append(data)

# Save the results to a CSV file
fields = ["author_name", "author_id", "author_affiliation", "first_publication", "first_pb_year", "citations", "hindex", "i10index", "hcore", "total_pubs", "Ψ-Index"]

with open("output_pi.csv", "w", newline="", encoding='utf-8') as csvfile:
    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    # Write the header row
    writer.writeheader()

    # Write each row of data
    for row in details:
        writer.writerow(row)