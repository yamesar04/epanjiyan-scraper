import requests

url = "https://epanjiyan.rajasthan.gov.in/e-search-page.aspx"

payload = "ctl00%24ScriptManager1=ctl00%24upContent%7Cctl00%24ContentPlaceHolder1%24gridsummary&ScriptManager1_HiddenField=&ctl00%24ContentPlaceHolder1%24a=rbtrural&ctl00%24ContentPlaceHolder1%24ddlDistrict=1&ctl00%24ContentPlaceHolder1%24ddlTehsil=1&ctl00%24ContentPlaceHolder1%24ddlSRO=1&ctl00%24ContentPlaceHolder1%24ddlcolony=-Select-&ctl00%24ContentPlaceHolder1%24ddldocument=17&ctl00%24ContentPlaceHolder1%24txtexcutent=&ctl00%24ContentPlaceHolder1%24txtclaiment=2&ctl00%24ContentPlaceHolder1%24txtexecutentadd=&ctl00%24ContentPlaceHolder1%24txtprprtyadd=&ctl00%24ContentPlaceHolder1%24txtimgcode=PM4ENA&ctl00%24hdnCSRF=&__EVENTTARGET=ctl00%24ContentPlaceHolder1%24gridsummary&__EVENTARGUMENT=Page%24page_num&__LASTFOCUS=&__VIEWSTATE=&__VIEWSTATEGENERATOR=&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=256&__EVENTVALIDATION=&__VIEWSTATEENCRYPTED=&__ASYNCPOST=true&"
headers = {
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}


if __name__ == '__main__':

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
