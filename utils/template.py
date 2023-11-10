from bs4 import BeautifulSoup
from database_scripts import insert_or_update_location, create_table 

import os

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
            # state = title
            # location_title = section.find('h3').text
            # location_description = section.find('p').text
            # location_img = section.find("img")['src']
            # response = insert_or_update_location(state, location_title, location_description,locationcategory, location_img)
            count +=1 
            # print(f"{count} records inserted into database")
            state_data.append(section_data)
    return state_data

# html_files_load(html_files)

import requests

def download_image_fromurl(url, save_path):
    image_metadata[image_url] = {}
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        image_metadata[image_url]['download_status'] = response.status_code
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a file with binary write mode and write the content
            out_file_path = os.path.join("images", save_path)
            image_metadata[image_url]['localpath'] = out_file_path
            with open(out_file_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

details = html_files_load(html_files)

image_metadata = {}
for file in details:
    image_url = file['location_img']
    new_image_path = image_url.replace("https://", "").replace("/", "_")
    download_image_fromurl(image_url, new_image_path)
    
import json   
# Write JSON data to the file
with open("image_metadata.json", 'w') as json_file:
    json.dump(image_metadata, json_file)

print(f"JSON data saved ")