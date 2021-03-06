import requests
import csv
import re
from tqdm import tqdm
from urllib.parse import quote

CLIENT_ID = "b4ce31d839c848e69665411db2425fed"
CLIENT_SECRET = "c35022a7e155415bb35dd6331d44d55d"

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = 'https://api.spotify.com/v1/'


def get_token():
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # Convert response to JSON
    auth_response_data = auth_response.json()

    # Save the access token
    access_token = auth_response_data['access_token']
    return access_token


def clean(artists):
    delimitors = ' & |&|, |,| Featuring | X | / |/| Duet With | With '
    return re.split(delimitors, artists)


def get_features(song, artist_name, access_token):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    song = quote(song)
    artist = quote(artist_name)
    artist_1st = quote(clean(artist_name)[0])

    def get_song(song_name, artist_name):
        # GET song ID
        url = BASE_URL + f"search?q=track:{song_name}%20artist:{artist_name}&type=track&market=ES&limit=1"
        # url = BASE_URL + f"search?q={song_name}%20{artist_name}&type=track&market=ES&limit=1"
        response = requests.get(url, headers=headers)
        # print(response.headers)
        return response.json()

    r1 = get_song(song, artist)
    r2 = get_song(song, artist_1st)

    # what if no results are returned
    if len(r1['tracks']['items']) == 0:
        if len(r2['tracks']['items']) == 0:
            return []
        song_id = r2['tracks']['items'][0]['id']
    else:
        song_id = r1['tracks']['items'][0]['id']

    # GET song features
    url = BASE_URL + f"audio-features/{song_id}"
    r = requests.get(url, headers=headers)
    r = r.json()

    return list(r.values())


def write_features(decade, offset):
    table_headers = ["song", "artist", "weeks_on_chart", "1st_appear"]
    spotify_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature']
    placeholder = [""] * len(spotify_features)
    header = table_headers + spotify_features
    filename = 'billboard100/aggregate-by-decade/' + decade

    table = []
    if offset == 0:
        table.append(header)

    def append_to_file(file, data):
        with open(file, 'a') as f:
            writer = csv.writer(f)
            for datapoint in data:
                writer.writerow(datapoint)

    with open(filename, 'r') as f:
        next(f)  # skip the header
        # skip to offset
        for _ in range(offset):
            next(f)
        reader = csv.reader(f)
        i = 0
        # for row in reader:
        for row in tqdm(reader):
            if i % 100 == 0:
                access_token = get_token()
                print(str(i) + ": " + access_token)
                append_to_file('billboard100/song-features/' + decade + '_features', table)
                table = []

            song = row[0]
            artist = row[1]
            features = get_features(song, artist, access_token)
            if len(features) == 0:
                features = placeholder
            table.append(row + features)
            i += 1

    append_to_file('billboard100/song-features/' + decade + '_features', table)


# date = datetime.date.fromisoformat('1970-01-03')
# end_date = datetime.date.today()
#
# while date < end_date:
#     print("processing..." + date.strftime("%Y-%m-%d"))
#     write_features(date.strftime("%Y-%m-%d"))
#     date = date + datetime.timedelta(7)

# song = "Save Your Tears"
# artists = "The Weeknd & Ariana Grande"
# token = "BQAns5u2INRa7ITTtX70VpzchBYx-MunthZaLU-nz5UczUUyNG8Lh28axltwois04rBl-1LbyPTLyslovK4"
# features = get_features(song, artists, token)
# print(features)
# print(clean(artists)[-1])

offsets = [5400, 4200, 3500, 3500, 4500, 1600]

start = 0
for decade, offset in zip(range(1970, 2030, 10)[start:], offsets[start:]):
    write_features(str(decade) + 's', offset)

# write_features("2020s", 0)
