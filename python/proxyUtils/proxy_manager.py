from sqlite import db_connector
from google_request_utilst import google, parseNextPages, next_google
from os import path
import requests 
from proxy_link_false_condition import false_condition,false_part_condition

proxy_query = "site:ru filetype:txt +:80 +:8080 +:3128"

class poxy:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

def comp(string, expressions):
    for condition in expressions:
        if condition == string:
            return True

def has_string(string, expressions):
    for condition in expressions:
        if condition in string:
            return True


class ProxyManager:
    def __init__(self, db_path):
        self.connector = db_connector(db_path)
        self.session = requests.Session()
        self.session.timeout = 10
        self.failedCount = 0
        self.size = 0
        self.failed = []
        self.success = []
        self.not_implemented= []

    def get_links(self):
        print("Get sites info....")
        response = []
        links = google(proxy_query, self.session)
        pages_links = parseNextPages(links)
        for page_link in pages_links:
            response = response + next_google(page_link, self.session)
        
        filtered_links = self.filterLink(response)
        self.__save_links_to_txt(filtered_links)
        return filtered_links
    

    def print_result(self):
        print("----------------Success saved----------------")
        for link in self.success:
            print("{}\n".format(link))

        print("----------------Fail----------------")
        for link in self.failed:
            print("{}\n".format(link))


        print("----------------Not implemented----------------")
        for link in self.not_implemented:
            print("{}\n".format(link))
            
        print("parsed {} from {}".format(self.size - self.failedCount, self.size))


    def parse_proxy(self, file_path = "sites.txt"):
        with open(file_path, "r") as f:
            data = f.read()
        
        links = data.split("\n")

        links = self.filterLink(links)

        print("size = {}".format(self.size))
        self.parse_sites(links)


    def __save_links_to_txt(self, links, path = ""):
        file_path = "sites.txt"
        data = "\n".join(links)
        with open(file_path, "w") as f:
            f.write(data)
        print("file {} is saved".format(file_path))

    def filterLink(self, links):
        filtered  = []

        for link in links:
            if not comp(link, false_condition) and not has_string(link, false_part_condition):
                filtered.append(link)

        self.size = len(filtered)
        return filtered

    def parse_proxy_page(self, page: str):
        result = []
            
        for line in page.split(b'\n'):
            line = str(line, "utf-8")
            for char in "\r\t":
                line.replace(char, "")
            if line == b'\r':
                continue

            for proxy in line.split(" "):
                if proxy == " " or len(proxy) < 4:
                    continue

                pair = proxy.split(":")
                result.append(poxy(pair[0], pair[1]))

        return result

    def prepare_link(self, link):
        begin = link[0: 3]
        if begin == "ftp":
            link = "http://"  + link[6:]
            print("link transformed to {}".format(link))
            self.prepare_link(link)

        begin = link[0:6]
        if begin == "/url?q":
            endPoint = link.find(".txt")
            link = link[7:endPoint + len(".txt")]
            print("link transformed to {}".format(link))
            self.prepare_link(link)
        return link

    def save_proxy(self, link):
        link = self.prepare_link(link)
        session = requests.Session()
        expectedExtention = ".txt"
        current_extention = link[-4:]

        if(current_extention == expectedExtention):
            response = session.get(link).content
            res = self.parse_proxy_page(response)

            self.save_to_db(res)
        else:
            print("not implemented")
            self.not_implemented.append(link)


    def save_to_db(self, proxy_list):
        conx = db_connector("build\instagram.db")
        conx.crete_table("proxy_list", "host string UNIQUE, port int, status string")

        for proxy in proxy_list:
            try:
                conx.insert("proxy_list", "'{}','{}','{}'".format(proxy.host, proxy.port, "unknown"))
            except:
                pass
        print("proxy saved!")

    def parse_sites(self, links):

        for link in links:
            print("parsing site {}\n".format(link))

            try:
                self.save_proxy(link)
                self.success.append(link)
            except:
                print("failed to parse site: {}".format(link))
                self.failed.append(link)
                self.failedCount = self.failedCount +1
        return self.failedCount

manager = ProxyManager("instagram.db")
manager.parse_proxy()