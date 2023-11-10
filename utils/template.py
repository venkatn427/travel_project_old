from bs4 import BeautifulSoup
from database_scripts import insert_or_update_location, create_table, insert_load_world_data,create_indiancities
import os
import csv

# Specify the folder directory containing HTML files
folder_path = "all_htmlfiles"
create_table()
# List all files in the directory
files_in_folder = os.listdir(folder_path)

state_data = []
# Filter HTML files
html_files = [file for file in files_in_folder if file.endswith(".html")]
csv_files = [file for file in files_in_folder if file.endswith(".csv")]

# Read the HTML file
def html_files_load(html_files):
    for file_path in html_files:
        locationcategory = file_path.replace(".html", "").split("_")[1]
        html_path = os.path.join(folder_path, file_path)
        # print(html_path)
        with open(html_path, "r", encoding="utf-8") as file:
            html_data = file.read()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_data, 'html.parser')

        # Extract and print specific elements
        title = soup.title
        h1 = soup.h1
        paragraph = soup.p
        list_items = soup.find_all('li')

        article_data = soup.article

        title = soup.title.text
        count = 0
        for section in article_data.find_all('section'):
            section_data = {}
            section_data['state'] = title
            section_data['location_title'] = section.find('h3').text
            section_data['location_description'] = section.find('p').text
            section_data['location_img'] = section.find("img")['src']
            state = title
            location_title = section.find('h3').text
            location_description = section.find('p').text
            location_img = section.find("img")['src']
            insert_or_update_location(state, location_title, location_description,locationcategory, location_img)
            count +=1 
            state_data.append(section_data)
        print(f"{count} records inserted into database")
    return state_data

# html_files_load(html_files)

import requests

def download_image_fromurl(url, save_path, image_metadata):
    image_metadata[url] = {}
    try:
        response = requests.get(url)
        image_metadata[url]['download_status'] = response.status_code
        if response.status_code == 200:
            out_file_path = os.path.join("images", save_path)
            image_metadata[url]['localpath'] = out_file_path
            with open(out_file_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

import json   

def downloages_all():
    image_metadata = {}
    details = html_files_load(html_files)
    for file in details:
        image_url = file['location_img']
        new_image_path = image_url.replace("https://", "").replace("/", "_")
        download_image_fromurl(image_url, new_image_path, image_metadata) 
    with open("image_metadata.json", 'w') as json_file:
        json.dump(image_metadata, json_file)

csv_file_path = "/Users/venkat/Desktop/TravelProjecr/travel_project/database/worldcities.csv"

def load_world_data_csv(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_file.seek(0)
        next(csv_reader)  
        for val in csv_reader:
            record = val
            city = record[0]
            city_ascii = record[1]
            latitude = record[2]
            longitude = record[3]
            country = record[4]
            country_iso2 = record[5]
            country_iso3 = record[6]
            admin_name = record[7]
            capital = record[8]
            population = record[9]
            insert_load_world_data(city,city_ascii,latitude,longitude,country,country_iso2,country_iso3,admin_name,capital,population)

load_world_data_csv(csv_file_path)
create_indiancities