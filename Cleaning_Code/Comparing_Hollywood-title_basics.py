##### This is third step where we compare both the Hollywood title in wikipedia and IMDB data

import pandas as pd
import re

# Cleaning function for titles
def clean_title(text):
    if pd.isna(text):
        return ''
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = text.replace(' ', '')
    text = re.sub(r'(.)\1+', r'\1', text)
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

# Load IMDb data once
title_basics_path = r'D:\Movie Analytics\IMDB_data\Cleaned_data\title_basics_filtered.tsv'
title_df = pd.read_csv(
    title_basics_path,
    sep='\t',
    encoding='utf-8',
    dtype=str,
    na_values=['\\N', r'\N']
)

# Clean originalTitle column
title_df['cleanedOriginalTitle'] = title_df['originalTitle'].astype(str).apply(clean_title)

# Master list to collect yearly data
all_data = []

# Loop through years 2000–2025
for year in range(2000, 2026):
    print(f"\nProcessing year: {year}")
    movie_path = fr'D:\Movie Analytics\Wikipedia_Hollywood_movie\Wikipedia_Hollywood_movie_cleaned\movie_table_{year}_filtered.tsv'

    try:
        movie_df = pd.read_csv(movie_path, sep='\t', encoding='utf-8')
    except FileNotFoundError:
        print(f"File not found: {movie_path} — skipping.")
        continue

    movie_titles_set = set(movie_df['Title'])

    # Filter IMDb entries for current year and title match
    filtered_df = title_df[
        (title_df['cleanedOriginalTitle'].isin(movie_titles_set)) &
        (title_df['titleType'] == 'movie') &
        (title_df['startYear'] == str(year))
    ].copy()

    print(f"Matches found for {year}: {len(filtered_df)}")

    if filtered_df.empty:
        continue

    # Handle runtimeMinutes
    filtered_df['runtimeMinutes'] = pd.to_numeric(filtered_df['runtimeMinutes'], errors='coerce')
    filtered_df['runtimeMinutes_filled'] = filtered_df['runtimeMinutes'].fillna(-1).infer_objects(copy=False)

    # Sort and drop duplicates
    filtered_df = (
        filtered_df.sort_values('runtimeMinutes_filled', ascending=False)
                   .drop_duplicates(subset=['cleanedOriginalTitle'], keep='first')
    )

    # Add the originalYear column
    filtered_df['originalYear'] = year

    # Drop helper columns
    filtered_df = filtered_df.drop(columns=['runtimeMinutes_filled', 'cleanedOriginalTitle'])

    # Add to list
    all_data.append(filtered_df)

# Combine all data
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    output_path = r'D:\Movie Analytics\IMDB_data\Cleaned_data\Hollywood_matched_data.tsv'
    final_df.to_csv(output_path, sep='\t', index=False)
    print(f"\nFinal combined file saved: {output_path}")
else:
    print("\nNo data matched across all years. No file created.")
