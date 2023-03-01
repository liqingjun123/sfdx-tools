'''
@author Liquad Li
@date 2023-02
@description To get the author of all files in a directory and output the results to a CSV file
'''
import os
import re
import csv

def get_author_from_file(filename):
    with open(filename, "r") as f:
        contents = f.read(200)
        match = re.search(r"\* @author\s+([\w\s]+)", contents)
        if match:
            author = match.group(1).strip()
            return author
    return None

def get_authors_in_directory(dirname):
    results = []
    for filename in os.listdir(dirname):
        if filename.endswith(".cls"):  # Change this to match the file extension you're looking for
            print(filename)
            filepath = os.path.join(dirname, filename)
            author = get_author_from_file(filepath)
            results.append((filename, author))
    return results

def write_results_to_csv(results, output_filename):
    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File", "Author"])
        for filename, author in results:
            writer.writerow([filename, author])

dirname = r"C:\vsts\LATAM_DX\force-app\main\default\classes"  # Change this to the directory you want to search
results = get_authors_in_directory(dirname)
write_results_to_csv(results, "output.csv")
