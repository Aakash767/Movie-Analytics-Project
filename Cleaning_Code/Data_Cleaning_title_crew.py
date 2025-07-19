##### This is the step three where we clean the data
import pandas as pd

# === Step 1: Load name_basics.tsv ===
print("Loading name_basics.tsv...")
name_df = pd.read_csv(
    'C:/User/asus\OneDrive\Desktop\Movie Analytics\IMDB_data/name_basics.tsv',
    sep='\t',
    usecols=['nconst', 'primaryName'],
    dtype={'nconst': str, 'primaryName': str}
)

# === Step 2: Load title_crew.tsv ===
print("Loading title_crew.tsv...")
crew_df = pd.read_csv(
    'D:\Movie Analytics\IMDB_data/title_crew.tsv',
    sep='\t',
    dtype=str  # Ensure all data is read as strings
)

# === Step 3: Create mapping from nconst to primaryName ===
print("Creating name map...")
name_map = dict(zip(name_df['nconst'], name_df['primaryName']))
del name_df  # Free up memory


# === Step 4: Safe conversion function ===
def convert_nconsts(nconst_str):
    if not isinstance(nconst_str, str) or pd.isna(nconst_str):
        return ''

    result = []
    for nc in nconst_str.split(','):
        nc_clean = str(nc).strip()
        primary_name = name_map.get(nc_clean, nc_clean)
        result.append(str(primary_name))  # Ensure it's a string
    return ','.join(result)


# === Step 5: Apply conversion to both directors and writers ===
print("Replacing nconsts with primary names...")
crew_df['directors'] = crew_df['directors'].apply(convert_nconsts)
crew_df['writers'] = crew_df['writers'].apply(convert_nconsts)

# === Step 6: Save the new file ===
output_file = 'D:\Movie Analytics\IMDB_data\Cleaned_data/title_crew_with_names.tsv'
print(f"Saving output to {output_file}...")
crew_df.to_csv(output_file, sep='\t', index=False)

print("Done! Your output is ready.")
