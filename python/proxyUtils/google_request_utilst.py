import requests 
from bs4 import BeautifulSoup

from sqlite import db_connector
#https://browser-info.ru/
#https://eax.me/google-captcha-bypass/

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Sec-Fetch-Mode' :'navigate',
        'Sec-Fetch-User' : '?1',
        'X-Client-Data' : 'CJO2yQEIo7bJAQjEtskBCKmdygEIqKPKAQjiqMoBCJetygEIza3KAQjLrsoBCMqvygEY77DKAQ==',
        'Sec-Fetch-Site' : 'none',
        'Accept-Language' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie' : 'CGIC=EhQxQzFQUkZJX2VuVUE4NTFVQTg1MiJ2dGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCxpbWFnZS9hcG5nLCovKjtxPTAuOCxhcHBsaWNhdGlvbi9zaWduZWQtZXhjaGFuZ2U7dj1iMw; HSID=A1v01VOKGh_rx0bp5; SSID=ABH4jh5qJouNia01I; APISID=HuH2mBbgGB8AV_oh/AT7xzx0U5RrrECvHZ; SAPISID=NHvFf3CYatr1vPKU/Ak1kCbwCaQDO5sGRm; SID=nwepq7B-oVJgKqJFrMCPYo8dNFHnxXfOTCIgvdJOkP4agOxQ8XnK0b6CyYD83thGu3tnWQ.; SEARCH_SAMESITE=CgQI6Y0B; GOOGLE_ABUSE_EXEMPTION=ID=12973be559dbb5e9:TM=1568558521:C=r:IP=46.211.91.74-:S=APGng0uc77oKklvhpZIswH4gxm_B2gEwJg; NID=188=OaALve_JWHP6MTdQTLwjX4pU8IzxAtgcYJbemp4u72rN7iRjq0G2qTxOBX1xKGlefxkAx-S8hhPhYl4MyOMt2oC5NMH9of6ga3Vr07-WO8vZ_GlbOwRf_YQrGKOPGxKHxY8uOIAu--w598YiKi7XLhKUMPBnw3fwSNKIHCX2iTGt4Ya0hCy_m5mjM7EFOu5e3_5HtzC9QBN0E899fFQVkKpFllbebnEn1a5nTXyJ581E; DV=E1cjEvAsln1RgPVShWwBWS9ucBRW09a-g7kjb7seaQEAAGCtLueKQ3momgAAABBCjJMXcI0dPAAAABkAJvXWMmlVwlMFAA; 1P_JAR=2019-09-15-14; SIDCC=AN0-TYtGG9tlbmkvB9i9i6ujppGIMsNSXzWG-Pbr7fGx7paZpFOS8FNXGQtfNDqNnAt5RQG54A',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive'
    }


def parseNextPages(links):
    result = []
    for link in links:
        if link != None and "/search?" in link:
            result.append(link)
    return result

def get_google_response(session, url):
    response = session.get(url, headers=headers_Get)

    with open("1.html", "w") as f:
        f.write(str(response.content))
    soup = BeautifulSoup(response.content, "html.parser")
    output = []

    for link in soup.findAll('a'):
        output.append(link.get('href'))
    return output

def next_google(search, session):
    url = "https://www.google.com/" + search
    return get_google_response(session, url)


def google(query, session): 
    query = '+'.join(query.split())
    url = 'https://www.google.com/search?q=' + query + '&ie=utf-8&oe=utf-8'
    return get_google_response(session, url)

def filter_hard_sites(hadr_list, link):
    for hard in hadr_list:
        if link == hard:
            return False
    return True

query  = "site:ru filetype:txt +:80 +:8080 +:3128"


#session = requests.Session()
#response = google(query, session)
#pagesLink = parseNextPages(response)

#for pages in pagesLink:
    #response = response + google(query, pages)

#links = filterLink(response)

#failed = 0
#size = len(links)


#hard_sites = ["https://proxydb.ru/ru-ru/buy-proxy", "http://proxydb.ru/ru-ru/socks-proxy-list"
                #"http://proxydb.ru/ru-ru/soft",]

#save_proxy("ftp://www.iformula.ru/1000prxy.txt")
#print("size = {}".format(size))
#failed = parse_sites(links)
#print("parsed {} from {}".format(size - failed, size))