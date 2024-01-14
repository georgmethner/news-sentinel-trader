import csv


def remove_at(i: int, s: str) -> str:
    return s[:i] + s[i + 1:]


with open('data/stock_company_info.csv', 'r') as infile, open('data/dataset.csv', 'w') as outfile:
    for row in infile:
        t_row = row
        ticker = ""
        for i in range(row.find(" - ") + 2):

            if not i == row.find(" - ") and not t_row[1] == " ":
                ticker += t_row[1]
            t_row = t_row[:1] + t_row[2:]

        outfile.write(ticker + ", " + t_row)
