import csv

def csv_to_dict(filename):
    result_dict = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 2:
                key, value = row
                result_dict[key] = value
    return result_dict

# Exemple d'utilisation
filename = '/Users/othmaneirhboula/WebScrap/Avito/Liens/NumTelBoutiques.csv'
dict_result = csv_to_dict(filename)
print(dict_result)
