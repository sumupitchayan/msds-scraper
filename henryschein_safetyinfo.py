#!/usr/bin/python

import os
import requests
from bs4 import BeautifulSoup as soup

# To add more practices, add it to the practices list below (with quotation marks:
# "Practice") and go to its Special Market's page on the HenrySchein website. Then,
# copy the HTML code of that webpage and paste it into a .html file -- name that
# file Practice_HS.html and make sure that that new .html file is located in the
# same folder as the other .html practice files (HSSafetyInfoCode). Finally, edit
# line 104 to match the file path of the HSSafetyInfo target folder on your computer.

practices = ["Amityville", "Bay Shore", "Brooklyn", "Clifton", "Commack",
            "Flushing", "Garwood", "Marlboro", "Massapequa Park", "Middle Island",
            "Midtown", "Riverhead", "Rockville Centre", "Smithtown", "Syosset",
            "Wantagh", "Woodside"]

###############################################################################

def get_safety_info(practice):
    location_file = open(practice +"_HS.html", "r")
    location_html = location_file.read()
    location_file.close()

    # PAGE SOUP OBJECT OF HTML FILE ------
    page_soup = soup(location_html, "html.parser")

    # MARK: - SDS numbers and Item counts:

    # Puts all of the SDS numbers into a list.
    sds_titles_raw = page_soup.findAll("td",{"class":"Title"})
    sds_titles = []
    for title in sds_titles_raw:
        if title.b != None:
            sds_titles.append(title)

    # Adds all of the SDS numbers to a list.
    sds_only = []
    for title in sds_titles:
        sds_only.append(title.b.a.string[0:7])

    # Adds all of the SDS number Item counts to a list.
    title_headers_items = page_soup.findAll("span",{"style":"font-weight:normal"})
    sds_item_count = []
    for title in title_headers_items:
        sds_item_count.append(title.span.string)

    # Combines SDS numers and Item counts to tuples in list.
    sds_and_items = []
    for i in range(0, len(sds_only)):
        tup = sds_only[i], sds_item_count[i]
        sds_and_items.append(tup)

    # Combines SDS numbers and Item counts to tuples in list.
    file_links = []
    for title in sds_titles:
        file_links.append(title.b.a["href"])

    # MARK: - Product names and HS Item #'s:

    # Puts all of the HS numbers into a list.
    product_cells = page_soup.findAll("td",{"style":"width: 100%; padding-left: 10px;"})
    product_names = []
    for cell in product_cells:
        name = str(cell.span.a["title"].encode('utf-8'))
        product_names.append(name)

    # Puts all of the HS Item #'s into an array
    hs_item_nrs = []
    for cell in product_cells:
        hs_item_nrs.append(cell.b.string.encode('utf-8'))

    # Puts Product Names and HSItem #'s into list of tuples.
    names_and_hsnrs = []
    for i in range(0, len(product_names)):
        tup = product_names[i], hs_item_nrs[i]
        names_and_hsnrs.append(tup)

    ordered_links = []
    def copy_link(item_count, link):
        for i in range(0, item_count):
            ordered_links.append(link)

    # Puts links into ordered list.
    for i in range(0, len(sds_and_items)):
        copy_link(int(sds_and_items[i][1].string), file_links[i])

    hsitem_name_link = []
    for i in range(0, len(product_names)):
        trip = hs_item_nrs[i], product_names[i], ordered_links[i]
        hsitem_name_link.append(trip)

    # MARK: - DOWNLOADING FILES AND RENAMING THEM

    def download_file(index):
        cur = hsitem_name_link[index]
        url = cur[2]
        r = requests.get(url, stream=True)
        raw_name = "HS Item #" + cur[0] + "- " + cur[1] + ".pdf"
        temp_name= raw_name
        file_name = temp_name.replace("/"," per ")

        file_path = "/Users/sumupitchayan/Desktop/HSSafetyInfo/" + file_name
        with open(file_path, 'wb') as f:
            f.write(r.content)

    # Downloads each file to the folder
    for i in range(0, len(hsitem_name_link)):
        download_file(i)

    print practice + " finished!"


# Loops through same process for each practice in the list.
for practice in practices:
    get_safety_info(practice)

print "Download of all HS Safety Info. Files = COMPLETE"
