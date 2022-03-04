import os
import csv

path_to_directory = '/Users/tiger/cs1951a/final-project/billboard100'
directory = os.fsencode(path_to_directory)

dict = {}

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)

    with open('billboard100/'+filename, 'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            song = row[0]
            artist = row[1]
            weeks_on_chart = int(row[2])
            if (song, artist) in dict:
                dict[(song, artist)] = max(dict[(song, artist)], weeks_on_chart)
            else:
                dict[(song, artist)] = weeks_on_chart

with open('billboard100/aggregate', 'w') as f:
    header = ["song", "artist", "weeks_on_chart"]
    writer = csv.writer(f)
    writer.writerow(header)

    for key in dict:
        (song, artist) = key
        weeks_on_chart = dict[key]
        row = [song, artist, weeks_on_chart]
        writer.writerow(row)