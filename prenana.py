


import requests
from bs4 import BeautifulSoup
import json




def get_csrf_token():
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

    return csrf_token


def get_ngo_data(id):

    print('\033[32m' + f'Taking data for ngo with id {id}!' + '\033[0m')

    csrf_token = get_csrf_token()
    # Set headers for the second POST request with csrf_token
    headers = {
    "Accept": "/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "53",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": f"ci_session=adli3vf625qct9c0j497mid6rn8rrpmc; csrf_cookie_name={csrf_token}",
    "Host": "ngodarpan.gov.in",
    "Origin": "https://ngodarpan.gov.in",
    "Referer": "https://ngodarpan.gov.in/index.php/search/",
    "sec-ch-ua":"\"Chromium\";v=\"112\", \"Brave\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }

    print(headers, "headers")


    # Set data for the second POST request
    data = {
        "id": f"{id}",
        "csrf_test_name": f"{csrf_token}"
    }
    print("data", data)

    # Make a request to the search endpoint
    search_url = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info'
    response = requests.post(search_url, headers=headers, data=data)
    print("Response", response)

    data = json.loads(response.text)
   
    if data['infor'] and data['infor'].get('0') and data['infor']['0'].get('ngo_name'):
        contactDetails = {
            'Ngo Name': data['infor']['0']['ngo_name'],
            'Mobile': data['infor']['0']['Mobile'],
            'Email': data['infor']['0']['Email'],
            'Website':  data['infor']['0']['ngo_url'],
            'Address': data['registeration_info'][0]['nr_add']
        }

        # Open a file in write mode and use the json.dump() function to write the dictionary to it
        with open('data.json', 'a') as file:
            json.dump(contactDetails, file, indent=4, separators=(',', ': '))
            file.write(',\n')




"""Loop through 1000 ids and get the details in a json"""
for i in range(41,1000):
    get_ngo_data(i)
