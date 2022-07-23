# csv-to-txt.py
import os

'''
Converts comma-separated .csv files into space-separated .txt files
'''
def to_text(csv_file):
    txt_file = csv_file.replace(".csv", ".txt")
    with open(csv_file, 'r') as to_read:
        with open(txt_file, 'w') as to_write:
            for csv_line in to_read:
                txt_line = csv_line.replace(",", " ")
                to_write.write(txt_line)

# Get all .csv files in the current directory
sample_data_path = os.path.dirname(__file__)
sample_data_files =  os.listdir(sample_data_path)
print("Converting .csv files in " + sample_data_path)
for file in sample_data_files:
    if file.endswith(".csv"):
        print("\t" + file + " --> " +file.replace(".csv", ".txt"))
        to_text(file)