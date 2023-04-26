import requests
from bs4 import BeautifulSoup
import csv

#html to text extracter
def extract_format_html_table(html):
    # parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # find the table containing the search results
    table = soup.find('table')

    # create a list to hold the table data
    table_data = []

    # loop through each row in the table
    for row in table.find_all('tr'):
        # create a list to hold the cell data for this row
        row_data = []
        # loop through each cell in the row
        for cell in row.find_all('td'):
            # append the cell data to the row_data list
            row_data.append(cell.text.strip())
        # append the row_data list to the table_data list
        table_data.append(row_data)

    return table_data




# Request to get the csrf token.
csrf_url = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf'

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "ci_session=adli3vf625qct9c0j497mid6rn8rrpmc",
    "Host": "ngodarpan.gov.in",
    "Referer": "https://ngodarpan.gov.in/index.php/search/",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Brave\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# Make a request to the csrf token endpoint
csrf_response = requests.get(csrf_url, headers=headers)

# Get the csrf_token from the response
csrf_token = csrf_response.json()['csrf_token']

# Set headers for the second POST request with csrf_token
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "175",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": f"ci_session=adli3vf625qct9c0j497mid6rn8rrpmc; csrf_cookie_name={csrf_token}",
    "Host": "ngodarpan.gov.in",
    "Origin": "https://ngodarpan.gov.in",
    "Referer": "https://ngodarpan.gov.in/index.php/search/",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Brave\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


# Set data for the second POST request
data = {
    "state_search": "",
    "district_search": "",
    "sector_search": "null",
    "ngo_type_search": "null",
    "ngo_name_search": "",
    "unique_id_search": "",
    "view_type": "detail_view",
    "csrf_test_name": f"{csrf_token}"
}

# Make a request to the search endpoint
list_of_ngos_url = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/search_index_new/0'
response = requests.post(list_of_ngos_url, headers=headers, data=data)

# Parse the HTML response and extract the table data
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')

# Create a CSV file with the table data
with open('ngodata.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        writer.writerow(cols)