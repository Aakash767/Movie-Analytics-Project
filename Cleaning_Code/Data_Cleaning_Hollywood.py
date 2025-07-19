##### This is the second step where we convert the data so that we can compare it with other big table

import pandas as pd
import re
for year in range(2000,2026):
    # Step 1: Load only the 'Title' column
    file_path = fr'D:\Movie Analytics\Wikipedia_Hollywood_movie\movie_table_{year}.tsv'
    df = pd.read_csv(file_path, sep='\t', usecols=['Title'], encoding='utf-8')

    # Step 2: Define the cleaning function
    def clean_title(text):
        if pd.isna(text):
            return ''
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'\[.*?\]', '', text)  # Remove anything inside [...]
        text = text.replace(' ', '')  # Remove all spaces
        text = re.sub(r'(.)\1+', r'\1', text)  # Remove repeated characters
        text = re.sub(r'[^a-z0-9]', '', text)  # Remove all special characters
        return text

    # Step 3: Apply the function
    df['Title'] = df['Title'].astype(str).apply(clean_title)

    # Step 5: Save the cleaned output
    output_path = fr'D:\Movie Analytics\Wikipedia_Hollywood_movie\Wikipedia_Hollywood_movie_cleaned\movie_table_{year}_filtered.tsv'
    df.to_csv(output_path, sep='\t', index=False)
    print("Titles cleaned (lowercased, no spaces, no repeats, no brackets) and saved to:", output_path)