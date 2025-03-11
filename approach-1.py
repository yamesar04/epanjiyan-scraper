import requests
import os
import json
from bs4 import BeautifulSoup

from request_params import *


class CaptchaDecoder:

    def __init__(self):
        pass  # To implement

    def get_captcha(self):
        pass

    def tesseract_decode_captcha(self):
        pass


class ScrapeFreshParams:

    """Class to support all stages of params generation
    1. Initial Params
    2. Location Type
    3. District
    4. Tehsil
    5. SRO
    """

    @classmethod
    def call(cls) -> str | None:
        try:
            # Initial Params
            params_raw = cls._get_start_params()
            parsed_params = cls._parse_params(params_raw)

            # Select location
            page_html = cls._select_location_type(params=parsed_params)

            updated_params_string = cls._update_params_in_payload(
                payload, parsed_params)

            return updated_params_string
        except Exception as e:
            print(f"EXCEPTION IN ScrapeFreshParams: {e}")

    @classmethod
    def _get_start_params(cls) -> str | None:
        url = "https://epanjiyan.rajasthan.gov.in/e-search-page.aspx"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cookie': 'ASP.NET_SessionId=ykuxxz0arxutmgihbnq1ludd; ASP.NET_SessionId=1srltie0e4ivniqmflcvblb1'
        }
        res = requests.get(url, headers=headers)
        res.raise_for_status()

        if res.status_code == 200:
            return res.text

    @classmethod
    def _select_location_type(cls, params: dict) -> str | None:
        url = "https://epanjiyan.rajasthan.gov.in/e-search-page.aspx"

        payload = "ctl00%24ScriptManager1=ctl00%24upContent%7Cctl00%24ContentPlaceHolder1%24rbtrural&ScriptManager1_HiddenField=&__EVENTTARGET=ctl00%24ContentPlaceHolder1%24rbtrural&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=&__VIEWSTATEGENERATOR=59A5EC9F&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=0&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=&ctl00%24ContentPlaceHolder1%24a=rbtrural&ctl00%24ContentPlaceHolder1%24ddlDistrict=-%20Select%20District%20-&ctl00%24ContentPlaceHolder1%24ddlSRO=-%20Select%20SRO%20-&ctl00%24ContentPlaceHolder1%24ddldocument=%20--%20Select%20--%20&ctl00%24ContentPlaceHolder1%24txtexcutent=&ctl00%24ContentPlaceHolder1%24txtclaiment=&ctl00%24ContentPlaceHolder1%24txtexecutentadd=&ctl00%24ContentPlaceHolder1%24txtprprtyadd=&ctl00%24ContentPlaceHolder1%24txtimgcode=&ctl00%24hdnCSRF=&__ASYNCPOST=true&"
        payload = cls._update_params_in_payload(
            payload=payload, new_params=params)

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://epanjiyan.rajasthan.gov.in',
            'Referer': 'https://epanjiyan.rajasthan.gov.in/e-search-page.aspx',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'X-MicrosoftAjax': 'Delta=true',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cookie': 'ASP.NET_SessionId=ykuxxz0arxutmgihbnq1ludd; ASP.NET_SessionId=1srltie0e4ivniqmflcvblb1'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response.raise_for_status()

        if response.status_code == 200:
            return response.text

    @classmethod
    def _parse_params(cls, page_markup: str) -> dict:
        """Parse params from page source to dict"""
        params_list = ['__VIEWSTATE', '__EVENTVALIDATION']
        params = {}

        soup = BeautifulSoup(page_markup, features='html.parser')

        for param in params_list:
            selector = f"input[id={param}]"
            value = soup.select_one(selector).get('value')
            params[param] = value

        return params

    @classmethod
    def _update_params_in_payload(cls, payload: str, new_params: dict) -> str:
        for param, value in new_params.items():
            payload = payload.replace(f"{param}=", f"{param}={value}")

        return payload


if __name__ == '__main__':
    params = ScrapeFreshParams.call()
    # WIP
