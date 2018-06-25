import csv

# 0               1           2       3       4       5           6           7       8           9               10
# POS_ASSOLUTA	PETTORALE	COGNOME	NOME	TEAM	NAZIONALITA	CATEGORIA	POS_CAT	POS_SESSO	TEMPO_UFFICIALE	DISTACCO

# Gender;Rank;Name;Birthyear;City;Club;Time;Offset;Bib;Category
import json
from datetime import date, time
from pprint import pprint
from time import sleep

import requests

columns = ('Gender', 'Name', 'Category', 'Club', 'Time')

catMap = {
    'JU-M': {'Gender': 'M', 'Pos': 0},
    'JU-F': {'Gender': 'F', 'Pos': 0},
    'EL-M': {'Gender': 'M', 'Pos': 1},
    'EL-F': {'Gender': 'F', 'Pos': 1},
    'MM 20-29': {'Gender': 'M', 'Pos': 2},
    'MF 20-29': {'Gender': 'F', 'Pos': 2},
    'MM 30-39': {'Gender': 'M', 'Pos': 3},
    'MF 30-39': {'Gender': 'F', 'Pos': 3},
    'MM 40-49': {'Gender': 'M', 'Pos': 4},
    'MF 40-49': {'Gender': 'F', 'Pos': 4},
    'MM 50-59': {'Gender': 'M', 'Pos': 5},
    'MF 50-59': {'Gender': 'F', 'Pos': 5},
    'MM 60-99': {'Gender': 'M', 'Pos': 6},
    'MF 60-99': {'Gender': 'F', 'Pos': 6},
    'INSP-M': {'Gender': 'M', 'Pos': 7},
    'INSP-F': {'Gender': 'F', 'Pos': 7},
    'sprint-F': {'Gender': 'F', 'Pos': 8},
    'sprint-M': {'Gender': 'M', 'Pos': 8},
}

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


outdata = []
first=True
line=0
with open("Oceanman2018-half - Generale.tsv") as csvfile:
    reader = csv.reader(csvfile, delimiter="\t")
    for row in reader:
        if first:
            first=False
            continue

        out = {}

        line += 1
        if line > 350:
            continue

        out['Gender'] = catMap[row[6]]['Gender']
        out['Pos'] = catMap[row[6]]['Pos']
        out['Bib'] = row[1]
        out['Name'] = f"{row[2]} {row[3]}, {row[4]}, {row[5]}"
        out['Time'] = row[9]
        out['Rank'] = int(row[0]),
        out['Cat'] = row[6]

        try:
            r = requests.get(f'https://apiah-staging.endu.net/events/41115/result/{int(row[1])+1000}/detail')
            record = r.json()
            parts = record['year'].split('-')
            born = date(int(parts[0]), int(parts[1]), int(parts[2]))
            out['Age'] = calculate_age(born)
            print(f"Age for {record['year']} is {out['Age']}")
        except:
            print(f"Failed to calculate age from " + record['year'])
            out['Age'] = 0

        pprint(out)
        outdata.append(out)

        sleep(1)

        #https: // apiah - staging.endu.net / events / 41115 / result / 277 / detail


with open('../frontend/processed.json', 'w') as outfile:
    json.dump(outdata, outfile)


