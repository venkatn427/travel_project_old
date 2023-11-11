import csv
import json
from datetime import date
import os
import requests

error_files = []
from bs4 import BeautifulSoup
def get_all_details(image_data):
    all_data = []
    for image_metadata in image_data:
        out_data = {}
        try:
            if image_metadata['business_status'] == 'OPERATIONAL':
                out_data['place_name'] = image_metadata['name']
                if 'photos' in image_metadata:
                    html_data = image_metadata['photos'][0]['html_attributions'][0]
                    out_data['map_reflink'] = BeautifulSoup(html_data, 'html.parser').a['href']
                    out_data['map_nametag'] = BeautifulSoup(html_data, 'html.parser').a.text
                    out_data['photo_reference'] = image_metadata['photos'][0]['photo_reference']
                else:
                    out_data['map_reflink'] = ''
                    out_data['photo_reference'] = ''
                    out_data['map_nametag'] = ''
                out_data['latitude_google'] = image_metadata['geometry']['location']['lat']
                out_data['longitude_google'] = image_metadata['geometry']['location']['lng']
                out_data['google_place_id'] = image_metadata['place_id']
                if 'rating' in image_metadata:
                    out_data['google_place_rating'] = image_metadata['rating']
                    out_data['google_user_rating'] = image_metadata['user_ratings_total']
                else:
                    out_data['google_place_rating'] = ''
                    out_data['google_user_rating'] = ''
                out_data['place_types'] = image_metadata['types']
                out_data['google_place_vicinity'] = image_metadata['vicinity']
        except Exception as e:
            error_files.append(f"error while reading {out_data['place_name']}")
        all_data.append(out_data)
    return all_data

csv_file_path = "database/worldcities.csv"

def get_location_data(csv_file_path):
    print("loading world places data")
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_file.seek(0)
        next(csv_reader)  
        for val in csv_reader:  
            record = val
            print(f"Loading {record[0]} data")
            if record[6] == "IND":
                record_json = {}
                record_json['city'] = record[0]
                record_json['city_ascii'] = record[1]
                record_json['latitude'] = record[2]
                record_json['longitude'] = record[3]
                record_json['country'] = record[4]
                record_json['country_iso2'] = record[5]
                record_json['country_iso3'] = record[6]
                record_json['admin_name'] = record[7]
                record_json['capital'] = record[8]
                record_json['population'] = record[9]
                all_types = ["restaurant","point_of_interest","food","lodging","hindu_temple","place_of_worship","museum","tourist_attraction"]
                for type in all_types:
                    city = record[0]
                    lat = str(record[2])
                    lng = str(record[3])
                    test_api = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+lat+"%2C"+lng+"&type="+type+"&radius=200000&key=AIzaSyD5eTxgUd8qCGHFTHzSAMs8eSC3CvbSGbA"
                    response = requests.get(test_api)
                    image_metadata = response.json()['results']
                    out_data = get_all_details(image_metadata)
                    record_json['places_city'] = out_data
                    out_file_name = os.path.join("database/datafiles",f"{city}_{type}_{str(date.today())}_metadata.json")
                    with open(out_file_name, 'w') as json_file:
                        json.dump(record_json, json_file, indent=2)
            else:
                continue

get_location_data(csv_file_path)