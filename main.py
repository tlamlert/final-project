# import requests
# import json
#
# token = 'BQC6eXdgsT67y8xJKp_bO6ciDS_MJJArn_UhPOWtZz29YbMgIu90yy2T5gQNFrSdYVAyUILLrFHiWCIDAAtHjGKUJsIIz2_w5aks3xf2YO_6k_gVEV6OdDNmXbDU4sXi0k4nCaDeOonhYV0j1dNTUADMABKcO19slG4'
# headers = {'Accept': 'application/json',
#            'Content-Type': 'application/json',
#            'Authorization': 'Bearer ' + token}
#
# # track_name = ""
# # artist_name = ""
# track_name = "angels"
# artist_name = "khalid"
#
# # url = "https://api.spotify.com/v1/search?q=track:{} artist:{}&type=track&limit=1".format(track_name, artist_name)
# url = "https://api.spotify.com/v1/search?q=track:{}&type=track&limit=1".format(track_name)
# response = requests.get(url, headers=headers)
# result = json.loads(response.text)
#
# # print(result)
# print(result["tracks"]["items"][0]["uri"][14:])

import datetime

start_date = datetime.date.fromisoformat("2015-01-01")
next_sat = start_date + datetime.timedelta( (5-start_date.weekday()) % 7 )
print(next_sat.strftime("%Y-%m-%d"))

# date = datetime.date.fromisoformat("2022-03-01")
# # print(date)
# # today = datetime.date.today()
# # print(today)
#
# while (date <= datetime.date.today()):
#     print(date)
#     date = date + datetime.timedelta(1)