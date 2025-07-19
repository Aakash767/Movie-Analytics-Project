import csv


def tsv_to_csv(tsv_file_path, csv_file_path):
    with open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsv_in, \
            open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_out:
        tsv_reader = csv.reader(tsv_in, delimiter='\t')
        csv_writer = csv.writer(csv_out)
        for row in tsv_reader:
            csv_writer.writerow(row)


# Example usage:
tsv_file = 'D:\Movie Analytics\IMDB_data\Cleaned_Data\Hollywood_allDataMerged.tsv'
csv_file = 'D:\Movie Analytics\IMDB_data\Cleaned_Data\Hollywood_allDataMerged.csv'
tsv_to_csv(tsv_file, csv_file)