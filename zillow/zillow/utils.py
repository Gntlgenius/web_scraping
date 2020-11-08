from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode
import json



URL = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22usersSearchTerm%22%3A%22Miami%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.375570048584%2C%22east%22%3A-80.11910795141603%2C%22south%22%3A25.637793410033606%2C%22north%22%3A25.90739047439762%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=false&includeList=true"

def cookie_parser():
    cookie_string = 'zguid=23|%24189b1c9f-5f01-4dbc-a7bf-c46d4a88f5bb; zgsession=1|a590eca9-b711-4b25-8771-54b164ecfa46; JSESSIONID=2761A32FF59B2D9397EF0E7ABB20BB6E; g_state={"i_p":1602761390600,"i_l":1}; __gads=ID=24b26d0583f02c5b:T=1602754373:S=ALNI_MaAzGO522OVdP73sgEPIWOkNI-3yA; AWSALB=RPSWsrqbMCTDn1D5KdeKKFVt561ymn/d/wg/vbY2trhRs5Lt3l6S9HPItOZM5kVBDWp0B3pnK1SM3olEQxyKJKT/tSMlKQmwHrQJ2RKz8Nyp6y3WBbnLXeNloPJg; AWSALBCORS=RPSWsrqbMCTDn1D5KdeKKFVt561ymn/d/wg/vbY2trhRs5Lt3l6S9HPItOZM5kVBDWp0B3pnK1SM3olEQxyKJKT/tSMlKQmwHrQJ2RKz8Nyp6y3WBbnLXeNloPJg; search=6|1605346511123%7Crect%3D25.924065538036224%252C-80.03585218359373%252C25.621078067956006%252C-80.45882581640623%26rid%3D12700%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0912700%09%09%09%09%09%09'
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies_dict = {}

    for key, morsel in cookie.items():
        cookies_dict[key] = morsel.value


    return cookies_dict

def parse_url(url, pagenumber):
    url_parse = urlparse(url)
    url_parse2 = parse_qs(url_parse.query)
    search_query_string = url_parse2.get('searchQueryState')[0]
    search_query_string= json.loads(search_query_string)
    search_query_string['pagination'] = {'currentPage':pagenumber}
    url_parse2.get('searchQueryState')[0] = search_query_string
    encoded_qs = urlencode(url_parse2, doseq=1)
    new_url = f"https://www.zillow.com/search/GetSearchPageState.htm?{encoded_qs}"
    return new_url

    
    

