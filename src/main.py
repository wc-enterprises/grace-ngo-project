

import requests
from bs4 import BeautifulSoup
import json
import pickle
import time

# Set the expiry time for the CSRF token to 1.8 seconds
CSRF_EXPIRY_TIME = 1.8

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"

# Total pages of NGOs data for the state.
TOTAL_PAGES = None

INDEX_OF_0_SCORE = 3144
INDEX_OF_1_SCORE = 175
INDEX_OF_2_SCORE = 162
INDEX_OF_3_SCORE = 166
INDEX_OF_4_SCORE = 429
INDEX_OF_5_SCORE = 574

# Initialize the global variable to None to indicate that no token has been generated yet
csrf_token = None
csrf_expiry = 0


def get_csrf_token():
    global csrf_token
    global csrf_expiry

    current_time = int(time.time())

    # If the token has not yet been generated or has expired, generate a new token
    if not csrf_token or current_time >= csrf_expiry:
        # Request to get the csrf token.
        CSRF_URL = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf'

        # Loading headers
        with open('../csrf-headers.pkl', 'rb') as f:
            headers = pickle.load(f)
            response = requests.get(CSRF_URL, headers=headers)
            csrf_token = response.json()['csrf_token']
            csrf_expiry = current_time + CSRF_EXPIRY_TIME

    return csrf_token


def calculate_fund_stats(data):
    total_amount_sanctioned = 0
    funds_sources = set()
    latest_date = ""
    for item in data:
        amount_sanctioned = int(item["amount_sanctioned"])
        total_amount_sanctioned += amount_sanctioned
        funds_sources.add(get_fund_source_text(item["sourcefund"]))
        date = item["dateto"]
        if date > latest_date:
            latest_date = date

    funds_score = get_funds_score(total_amount_sanctioned)

    return {
        "Total Amount Sanctioned": total_amount_sanctioned,
        "Funds Sources": list(funds_sources),
        "Latest Date Funds Received": latest_date,
        "Funds Score": funds_score
    }


def get_fund_source_text(code):
    if code == "S":
        return "State"
    elif code == "C":
        return "Center"
    elif code == "O":
        return "Overseas"
    else:
        return code


def get_funds_score(total_amount_sanctioned):
    if total_amount_sanctioned == 0:
        return 0
    elif total_amount_sanctioned <= 100000:
        return 1
    elif total_amount_sanctioned <= 500000:
        return 2
    elif total_amount_sanctioned <= 1000000:
        return 3
    elif total_amount_sanctioned <= 5000000:
        return 4
    else:
        return 5


def collect_ngo_data(id):
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
        "id": f"{id}",
        "csrf_test_name": f"{csrf_token}"
    }

    # Make a request to the search endpoint
    search_url = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info'
    response = requests.post(search_url, headers=headers, data=data)

    data = json.loads(response.text)

    ngo_name = data['infor'].get('0', {}).get('ngo_name', None)
    if ngo_name is None:
        ngo_name = data.get('registeration_info', [{}])[
            0].get('nr_orgName', None)

    ngo_data = {
        'Unique Id': data['infor'].get('0', {}).get('UniqueID', None),
        'Ngo Name': ngo_name,
        'Mobile': data['infor'].get('0', {}).get('Mobile', None),
        'Email': data['infor'].get('0', {}).get('Email', None),
        'Telephone': data['infor'].get('0', {}).get('Off_phone1', None),
        'Website':  data['infor'].get('0', {}).get('ngo_url', None),
        'Address': data.get('registeration_info', [{}])[0].get('nr_add', None),
        'City': data.get('registeration_info', [{}])[0].get('nr_city', None),
        'State': data.get('registeration_info', [{}])[0].get('StateName', None),
        'FCRARegistrationNo': data.get('registeration_info', [{}])[0].get('fcrano', None),
        'DateOfRegistration': data.get('registeration_info', [{}])[0].get('ngo_reg_date', None),
        'Funds Info': calculate_fund_stats(data['source_info'])
    }

    return ngo_data


def get_onclick_params(soup):
    params = []
    for a_tag in soup.find_all('a', onclick=True):
        onclick = a_tag['onclick']
        # Extract the parameter value from the onclick attribute
        param_value = onclick.split("'")[1]
        params.append(param_value)
    return params


def ngo_list(stateId, state, startValue):
    global TOTAL_PAGES

    NGO_LIST_URL = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/search_index_new/' + \
        str(startValue)

    csrf_token = get_csrf_token()

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "177",
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
        "state_search": f"{stateId}",
        "district_search": "",
        "sector_search": "null",
        "ngo_type_search": "null",
        "ngo_name_search": "",
        "unique_id_search": "",
        "view_type": "detail_view",
        "csrf_test_name": f"{csrf_token}"
    }

    # Make a request to the search endpoint
    response = requests.post(NGO_LIST_URL, headers=headers, data=data)
    # Parse the HTML response and extract the table data
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_search_params(stateId, state, startValue):
    soup = ngo_list(stateId, state, startValue)
    table = soup.find('table')
    unique_id_to_get_ngo_info = get_onclick_params(table)
    return unique_id_to_get_ngo_info


def get_total_pages(stateId, state):
    soup = ngo_list(stateId, state, 0)
    total_ngos = soup.select_one(".pagination span").text.split()[-1]
    return int(total_ngos)//10


def main(stateId, state):
    print("############################ Starting to collect NGO data ############################")
    global TOTAL_PAGES
    global INDEX_OF_0_SCORE
    global INDEX_OF_1_SCORE
    global INDEX_OF_2_SCORE
    global INDEX_OF_3_SCORE
    global INDEX_OF_4_SCORE
    global INDEX_OF_5_SCORE

    if (not TOTAL_PAGES):
        TOTAL_PAGES = get_total_pages(stateId, state)

    print(GREEN + "Total pages: " + str(TOTAL_PAGES))
    print(GREEN + "Date collection of NGOs started.")
    for i in range(466,TOTAL_PAGES):
        search_params = get_search_params(stateId, state, i*10)

        for val in search_params:
            ngo_data = collect_ngo_data(val)
            funds_score = ngo_data['Funds Info']['Funds Score']
            del ngo_data['Funds Info']['Funds Score']

            if funds_score == 0:
                INDEX_OF_0_SCORE += 1
                index = INDEX_OF_0_SCORE
            elif funds_score == 1:
                INDEX_OF_1_SCORE += 1
                index = INDEX_OF_1_SCORE
            elif funds_score == 2:
                INDEX_OF_2_SCORE += 1
                index = INDEX_OF_2_SCORE
            elif funds_score == 3:
                INDEX_OF_3_SCORE += 1
                index = INDEX_OF_3_SCORE
            elif funds_score == 4:
                INDEX_OF_4_SCORE += 1
                index = INDEX_OF_4_SCORE
            elif funds_score == 5:
                INDEX_OF_5_SCORE += 1
                index = INDEX_OF_5_SCORE

            # Open a file in write mode and use the json.dump() function to write the dictionary to it
            with open(f'{state}-{funds_score}.json', 'a') as file:
                file.write(f'{index}. ')
                json.dump(ngo_data, file, indent=4,
                          separators=(',', ': '))
                file.write('\n')
            name = ngo_data["Ngo Name"]
            print(YELLOW + f"Entered {name} data successfully.")
        print(
            RED + f"Page {i+1} data collected successfully of " + str(TOTAL_PAGES)+"pages.")

    print(GREEN + "Total No funds received NGOs: " + str(INDEX_OF_0_SCORE))
    print(GREEN + "Total Received less than 1 lakh NGOs: " +
          str(INDEX_OF_1_SCORE))
    print(GREEN + "Total Received between 1 lakh and 5 lakhs NGOs: " +
          str(INDEX_OF_2_SCORE))
    print(GREEN + "Total Received between 5 lakhs and  10 lakhs NGOs: " +
          str(INDEX_OF_3_SCORE))
    print(GREEN + "Total Received between 10 lakhs and 50 lakhs NGOs: " +
          str(INDEX_OF_4_SCORE))
    print(GREEN + "Total More than 50 lakhs received NGOs: " +
          str(INDEX_OF_5_SCORE))


main("27", "maharashtra")
