##### This is the first step of our project it involve Bollywood movie data scrapinig from wikipedia
# In this we have gathered the list of hindi bollywood movies from year 2000-2025
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Create the output directory if it doesn't exist
output_dir = r'D:\Movie Analytics\Wikipedia_Bollywood_movie'
os.makedirs(output_dir, exist_ok=True)

# Scraps the data of year 2000-2006
for year in range(2000, 2006):
    print(f"Processing year: {year}")

    # Generate the Wikipedia URL
    url = f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_{year}"

    try:
        # Request and parse the page
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # Find the 2nd wikitable (assuming it holds the movie data)
        tables = soup.find_all('table', class_='wikitable')
        if len(tables) < 2:
            print(f"Less than 2 tables found for year {year}. Skipping.")
            continue
        table = tables[1]

        # Extract headers
        column = table.find_all('th')
        column_names = [title.text.strip() for title in column]

        # Initialize DataFrame
        df = pd.DataFrame(columns=column_names)

        # Extract row data
        column_data = table.find_all('tr')
        for row in column_data[1:]:
            row_data = row.find_all('td')
            individual_row_data = [data.text.strip() for data in row_data]

            # Clean the row: pad or truncate to match column count
            individual_row_data = individual_row_data[:len(df.columns)]
            while len(individual_row_data) < len(df.columns):
                individual_row_data.append('')

            df.loc[len(df)] = individual_row_data

        # Build file path dynamically
        file_path = os.path.join(output_dir, f'movie_table_{year}.tsv')

        # Save to TSV
        df.to_csv(file_path, sep='\t', index=False)
        print(f"Saved: {file_path}")

    except Exception as e:
        print(f"Error processing year {year}: {e}")

# Runs the for loop from year 2006–2025
for year in range(2006, 2026):
    print(f"Processing year: {year}")

    url = f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_{year}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Initialize a list to collect all rows
    all_rows = []
    all_columns_set = set()

    # Loop through multiple wikitable tables (usually 4)
    for i in range(1, 5):
        try:
            table = soup.find_all('table', class_='wikitable')[i]
        except IndexError:
            continue  # Skip if table not found

        # Get column names and reverse order
        column = table.find_all('th')
        column_names = [title.text.strip() for title in column[1:]]
        column_names.reverse()
        all_columns_set.update(column_names)

        # Extract data rows
        column_data = table.find_all('tr')
        for row in column_data[1:]:
            row_data = row.find_all('td')
            individual_row_data = [data.text.strip() for data in row_data]
            individual_row_data.reverse()

            # Fix row length mismatch
            if len(column_names) < len(individual_row_data):
                n = len(individual_row_data) - len(column_names)
                individual_row_data = individual_row_data[:-n]
            elif len(column_names) > len(individual_row_data):
                n = len(column_names) - len(individual_row_data)
                individual_row_data += ['op'] * n

            # Store as dictionary to merge later
            row_dict = dict(zip(column_names, individual_row_data))
            all_rows.append(row_dict)

    # Create final DataFrame using all collected columns
    all_columns_list = list(all_columns_set)
    df = pd.DataFrame(all_rows, columns=all_columns_list)

    # Save as TSV
    file_path = os.path.join(output_dir, f'movie_table_{year}.tsv')
    df.to_csv(file_path, sep='\t', index=False)
    print(f"Saved: {file_path}")

