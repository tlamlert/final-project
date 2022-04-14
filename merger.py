import os
import csv
import datetime


def aggregate(year):
    path_to_directory = 'billboard100/daily-charts'
    directory = os.fsencode(path_to_directory)
    weeks = {}
    timestamp = {}

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if not filename.startswith(year):
            continue
        print(filename)

        with open('billboard100/daily-charts/' + filename, 'r') as f:
            next(f)
            reader = csv.reader(f)
            for row in reader:
                song = row[0]
                artist = row[1]
                weeks_on_chart = int(row[2])
                key = (song, artist)

                if key in weeks:
                    weeks[key] = max(weeks[key], weeks_on_chart)
                else:
                    weeks[key] = weeks_on_chart

                if key in timestamp:
                    if datetime.date.fromisoformat(timestamp[key]) > datetime.date.fromisoformat(filename):
                        timestamp[key] = filename
                else:
                    timestamp[key] = filename

    with open('billboard100/aggregate-by-year/' + year, 'w') as f:
        header = ["song", "artist", "weeks_on_chart", "1st_appear"]
        writer = csv.writer(f)
        writer.writerow(header)

        # keys = list(dict.keys())
        # random.shuffle(keys)
        # for key in dict:
        #     (song, artist) = key
        #     weeks_on_chart = dict[key]
        #     row = [song, artist, weeks_on_chart]
        #     writer.writerow(row)

        sorted_dict = sorted(weeks.items(), key=lambda item: -item[1])
        for item in sorted_dict:
            (key, weeks_on_chart) = item
            (song, artist) = key
            date = timestamp[(song, artist)]
            row = [song, artist, weeks_on_chart, date]
            writer.writerow(row)


# start_decade = 1970
# end_decade = 203
#
# for decade in range(start_decade, end_decade):
#     aggregate(str(decade))

start_year = 1970
end_year = 2023

for year in range(start_year, end_year):
    aggregate(str(year))