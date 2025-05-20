import pandas as pd
from scholarly import scholarly
import json
import time

df = pd.read_csv('data.csv', encoding="iso-8859-1")
not_found = []
searched_authors = []  # List to store all searched authors with their data

for index, author_name in enumerate(df['Author']):
    try:
        print("Index: ", index + 1)
        print(author_name)
        time.sleep(5.0)
        search_query = scholarly.search_author(author_name)

        # Loop through all results for the author name
        for author_result in search_query:
            try:
                author = scholarly.fill(author_result)
                author_id = author.get("scholar_id", None)

                if author_id:
                    # Save each author's data in a JSON file named after their author_id
                    filename = f"{author_id}.json"
                    json_string = json.dumps(author, indent=4)
                    with open("data/" + filename, "w") as f:
                        f.write(json_string)
                    print(f"JSON file {filename} created.")

                    # Add the author name and data to the searched_authors list
                    searched_authors.append({
                        "name": author_name,
                        "data": author
                    })

            except Exception as e:
                print(f"Error processing author result for {author_name}: {e}")

    except Exception as e:
        print(f"Exception occurred for {author_name}: {e}")
        not_found.append(author_name)

# Save the searched authors list to a JSON file
with open("data/searched_authors.json", "w") as f:
    json.dump(searched_authors, f, indent=4)

print("Authors not found:", not_found)