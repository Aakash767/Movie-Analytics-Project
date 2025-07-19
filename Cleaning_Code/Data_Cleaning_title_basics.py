##### This is the second step where we convert the data so that we can compare it with other big table

import pandas as pd
import re

# Step 1: Load required columns only
file_path = r'D:\Movie Analytics\IMDB_data\title_basics.tsv'
cols_to_use = ['tconst', 'titleType', 'originalTitle', 'startYear', 'endYear', 'runtimeMinutes']
df = pd.read_csv(file_path, sep='\t', usecols=cols_to_use, encoding='utf-8')

# Step 2: Define cleaning function for 'originalTitle'
def clean_title(text):
    if pd.isna(text):
        return ''
    text = text.lower()                      # lowercase
    text = re.sub(r'\[.*?\]', '', text)      # remove [...] and content
    text = text.replace(' ', '')             # remove spaces
    text = re.sub(r'(.)\1+', r'\1', text)    # remove repeated characters
    text = re.sub(r'[^a-z0-9]', '', text)  # Remove all special characters
    return text

# Step 3: Apply cleaning to originalTitle
df['originalTitle'] = df['originalTitle'].astype(str).apply(clean_title)

# Step 4: Preview first few rows
print(df.head())

# Step 5: Save to new file (optional)
output_path = r'D:\Movie Analytics\IMDB_data\Cleaned_data\title_basics_filtered.tsv'
df.to_csv(output_path, sep='\t', index=False)

print("Filtered columns with cleaned originalTitle saved to:", output_path)
