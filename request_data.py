import requests

def request(url,params = None):

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.lenskart.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.lenskart.com/',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'x-accept-language': 'en',
        'x-api-client': 'desktop',
        'x-b3-traceid': '991777960663655',
        'x-country-code': 'IN',
        'x-country-code-override': 'IN',
        'x-customer-type': 'NEW',
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(response.text)
        print(response.status_code)
        return None



def get_lat_log(pincode):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.lenskart.com/',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-storage-access': 'active',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'x-browser-channel': 'stable',
        'x-browser-copyright': 'Copyright 2026 Google LLC. All Rights Reserved.',
        'x-browser-validation': 'jaO2vvOiPp81rvmaLFByfP/P8kY=',
        'x-browser-year': '2026',
        'x-client-data': 'CKmdygEIkqHLAQiFoM0B',
    }
    pincode = "4s"+str(pincode)
    response = requests.get(f'https://maps.googleapis.com/maps/api/js/GeocodeService.Search?{pincode}&7sIN&9sen&r_url=https%3A%2F%2Fwww.lenskart.com%2Flenskart-air-la-e13033-c1-eyeglasses.html&callback=_xdc_._o2lebb&key=AIzaSyC17loXXrcP_zTaS_5ET2DG5Reae3qWUXs&token=10426',headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(response.text)
        print(response.status_code)
        return None

