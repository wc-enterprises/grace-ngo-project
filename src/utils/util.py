import pickle

csrf_headers = {
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

with open('csrf-headers.pkl', 'wb') as f:
    pickle.dump(csrf_headers, f)
