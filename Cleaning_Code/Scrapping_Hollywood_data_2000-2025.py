##### This is the first step of our project it involve Hollywood Movie data scrapinig from wikipedia
# In this we have gathered the list of Hollywood movies from year 2000-2025

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Set the output directory
output_dir = r'D:\Movie Analytics\Wikipedia_Bollywood_movie'
os.makedirs(output_dir, exist_ok=True)

# Loop through years from 2000 to 2025
for year in range(2000, 2026):
    print(f"\nProcessing year: {year}")

    # Wikipedia URL for that year
    url = f"https://en.wikipedia.org/wiki/List_of_American_films_of_{year}"
    page = requests.get(url)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page.text, 'html.parser')

    all_rows = []  # To hold all extracted rows
    all_columns_set = set()  # To collect all unique column names

    # Loop through 4 quarterly tables (index 1 to 4)
    for i in range(1, 5):
        try:
            table = soup.find_all('table', class_='wikitable')[i]
        except IndexError:
            continue  # Skip if fewer tables exist

        # Extract column headers from <thead>, fallback to first row if needed
        thead = table.find('thead')
        if thead:
            column = thead.find_all('th')
        else:
            column = table.find_all('tr')[0].find_all('th')  # fallback

        # Extract all <th> column names (don't skip the first one now)
        column_names = [title.text.strip() for title in column]

        # Reverse column names to match reversed row data order
        column_names.reverse()
        all_columns_set.update(column_names)
        # Extract rows from <tbody> (excluding subheader rows)
        rows = table.find_all('tr')[1:]  # skip header row
        for row in rows:
            if row.find('th'):
                continue  # skip subheaders like "July–September"

            row_data = row.find_all('td')
            individual_row_data = [data.text.strip() for data in row_data]
            individual_row_data.reverse()

            # Adjust row length to match columns
            if len(column_names) < len(individual_row_data):
                n = len(individual_row_data) - len(column_names)
                individual_row_data = individual_row_data[:-n]

            if len(column_names) > len(individual_row_data):
                n = len(column_names) - len(individual_row_data)
                individual_row_data = individual_row_data + ['op'] * n

            # Map each row to a dictionary
            row_dict = dict(zip(column_names, individual_row_data))
            all_rows.append(row_dict)

    # Create DataFrame with all rows and consistent column set
    all_columns_list = list(all_columns_set)
    df = pd.DataFrame(all_rows, columns=all_columns_list)
    # Save as a .tsv file
    file_path = os.path.join(output_dir, f'movie_table_{year}.tsv')
    df.to_csv(file_path, sep='\t', index=False)
    print(f"Saved: {file_path}")

