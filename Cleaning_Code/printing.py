
#####Printing the Columns, 20 rows and total no of rows
#####Prints headers, first 20 rows and total number of rows


def search_in_tsv(file_path, keyword):
    keyword = keyword.lower()  # optional: case-insensitive
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if keyword in line.lower():  # case-insensitive match
                print(line.strip())

if __name__ == "__main__":
    tsv_file = r"D:\IMDB_data\Updates1\title_basics_filtered.tsv"#input("Enter path to the .tsv file: ").strip()
    search_word = input("Enter the word to search for: ").strip()
    search_in_tsv(tsv_file, search_word)




