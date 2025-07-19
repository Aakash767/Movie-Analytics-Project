file_path = r"D:/IMDB_data/Updates1/Hollywood_basics_matched.tsv"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read and print column names (header)
        header_line = f.readline()
        if not header_line:
            print("File is empty.")
            exit()

        header = header_line.strip().split('\t')
        print("📌 Columns:")
        print(header)

        print("\n📋 First 200 rows:\n")
        row_count = 0

        for i, line in enumerate(f, start=1):
            if i <= 200:
                print(line.strip())
            row_count += 1

        print(f"\n📈 Total number of rows (excluding header): {row_count}")

except FileNotFoundError:
    print("❌ File not found. Please check the path.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
