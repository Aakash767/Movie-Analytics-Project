##### this is the forth step where we are going to make a final file we are going to need in powerBI
import sys
import csv

# File paths
filtered_file = "D:\Movie Analytics\IMDB_data\Cleaned_Data\Hollywood_matched_data.tsv"
full_file = "D:\Movie Analytics\IMDB_data/title_basics.tsv"
rating_file = "D:\Movie Analytics\IMDB_data\Cleaned_Data/title_ratings.tsv"
crew_file = "D:\Movie Analytics\IMDB_data\Cleaned_Data/title_crew_with_names.tsv"
output_file = "D:\Movie Analytics\IMDB_data\Cleaned_Data\Hollywood_allDataMerged.tsv"

# Columns to remove from title_basics.tsv
columns_to_remove = {"primaryTitle", "endYear"}

# Step 1: Read tconst values from the filtered file
with open(filtered_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    filtered_tconsts = set(row["tconst"].strip() for row in reader)

print(f"🔍 Found {len(filtered_tconsts)} tconsts in {filtered_file}")

# Step 2: Load rating data (tconst → averageRating)
with open(rating_file, "r", encoding="utf-8") as frating:
    rating_reader = csv.DictReader(frating, delimiter="\t")
    rating_map = {row["tconst"].strip(): row["averageRating"] for row in rating_reader}

print(f"📊 Loaded ratings for {len(rating_map)} titles from {rating_file}")

# Step 3: Load crew data (tconst → directors, writers)
with open(crew_file, "r", encoding="utf-8") as fcrew:
    crew_reader = csv.DictReader(fcrew, delimiter="\t")
    crew_map = {
        row["tconst"].strip(): {
            "directors": row.get("directors", "\\N"),
            "writers": row.get("writers", "\\N")
        }
        for row in crew_reader
    }

print(f"🎬 Loaded crew info for {len(crew_map)} titles from {crew_file}")

# Step 4: Process and filter title_basics.tsv
with open(full_file, "r", encoding="utf-8") as fin, \
        open(output_file, "w", encoding="utf-8", newline="") as fout:
    reader = csv.DictReader(fin, delimiter="\t")

    # Determine final column set (excluding unwanted ones)
    final_fieldnames = [field for field in reader.fieldnames if field not in columns_to_remove]

    # Add new merged & static fields to final output
    final_fieldnames.extend(["averageRating", "directors", "writers", "country"])

    writer = csv.DictWriter(fout, fieldnames=final_fieldnames, delimiter="\t")
    writer.writeheader()

    match_count = 0
    for row in reader:
        tconst = row["tconst"].strip()
        if tconst in filtered_tconsts:
            # Start with base row (excluding unwanted columns)
            filtered_row = {key: value for key, value in row.items() if key in final_fieldnames}

            # Add averageRating
            filtered_row["averageRating"] = rating_map.get(tconst, "\\N")

            # Add directors and writers
            crew = crew_map.get(tconst, {})
            filtered_row["directors"] = crew.get("directors", "\\N")
            filtered_row["writers"] = crew.get("writers", "\\N")

            # Add fixed country value
            filtered_row["country"] = "US"

            writer.writerow(filtered_row)
            match_count += 1

print(f"✅ Done! Wrote {match_count} rows to {output_file} with averageRating, directors, writers, and country='IN'")
