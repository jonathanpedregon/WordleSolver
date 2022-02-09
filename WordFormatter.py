import csv

rows = []

with open('FiveLetterWords_raw.txt', 'r') as fd:
    reader = csv.reader(fd)
    for row in reader:
        rows.append(row)

file = open('FiveLetterWords.txt', 'a')
for row in rows:
    for word in row[0].split():
        file.write("{0}\n".format(word))

file.close()
