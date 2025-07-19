##### This is the second step where we convert the data so that we can compare it with other big tables

import pandas as pd
import re

# Loop over each year from 2000 to 2025
for year in range(2000, 2026):
    # Step 1: Load only the 'Title' column
    file_path = fr'D:\Movie Analytics\Wikipedia_Bollywood_movie\movie_table_{year}.tsv'
    df = pd.read_csv(file_path, sep='\t', usecols=['Title'], encoding='utf-8')

    # Step 2: Define the cleaning function
    def clean_title(text):
        if pd.isna(text):
            return ''
        text = text.lower()                             # Convert to lowercase
        text = re.sub(r'\[.*?\]', '', text)             # Remove anything inside [...]
        text = text.replace(' ', '')                    # Remove all spaces
        text = re.sub(r'(.)\1+', r'\1', text)           # Remove repeated characters
        text = re.sub(r'[^a-z0-9]', '', text)           # Remove all special characters
        return text

    # Step 3: Apply the cleaning function
    df['Title'] = df['Title'].astype(str).apply(clean_title)

    # Step 4: Save the cleaned data to a new file
    output_path = fr'D:\Movie Analytics\Wikipedia_Bollywood_movie\Wikipedia_Bollywood_movie_cleaned\movie_table_{year}_filtered.tsv'
    df.to_csv(output_path, sep='\t', index=False)

    # Step 5: Print status
    print(f"Titles cleaned and saved to: {output_path}")


