from bs4 import BeautifulSoup
from init_db import insert_or_update_location, create_table, select_all_from_table

import os

# Specify the folder directory containing HTML files
folder_path = "allhtmlfiles"

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
            # section_data = {}
            # section_data['state'] = title
            # section_data['location_title'] = section.find('h3').text
            # section_data['location_description'] = section.find('p').text
            # section_data['location_img'] = section.find("img")['src']
            state = title
            location_title = section.find('h3').text
            location_description = section.find('p').text
            location_img = section.find("img")['src']
            response = insert_or_update_location(state, location_title, location_description,locationcategory, location_img)
            count +=1 
            print(f"{count} records inserted into database")
            # state_data.append(section_data)
