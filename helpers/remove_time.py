import csv

with open('../data/cnbc_headlines.csv', 'r', encoding="utf8") as infile, open('../data/cnbc_headlines_edit.csv', 'w') as outfile:
    reader = csv.reader(infile)

    for row in reader:

        date = row[1]
        date = date[18:]
        if len(date) == 0:
            continue

        if date[0] == " ":
            date = date.replace(" ", "0")
        print(date)
        row[1] = date

        row[2] = row[2].replace("'", '')
        row[2] = row[2].replace('"', "'")

        outfile.write('"' + row[0] + '",' + row[1] + ', "' + row[2] + '"\n')
