import bs4
import os
from urllib import request

BF_EXTENSION = "ext"
BF_LOCATION = "location"
BF_DAY = "day"
BF_TIME = "time"

REP_DATA = "RRN_Data"
URL_BISON_FUTE_RRN = "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/Evenementiel-DIR/grt/RRN/"

def fileNameinfo(href):
    mapInfo = {}
    # Extenion
    list_elt_href = href.split(".")
    mapInfo[BF_EXTENSION] = list_elt_href[-1]
    fileName = "".join(list_elt_href[:-1])
    return fileName

def hasExtension(href, ext):
    list_elt_href = href.split(".")
    return list_elt_href[-1] == ext

os.makedirs(REP_DATA, exist_ok=True)

request_text = request.urlopen(URL_BISON_FUTE_RRN).read()
page = bs4.BeautifulSoup(request_text, "lxml")

for link in page.findAll("a"): #[1:10]:
    if hasExtension(link.get("href"), "xml"):
        fileLink = link.get("href")
        fileName = fileNameinfo(fileLink)
        if not fileName == "content":
            path_to_save_rep = os.path.join(REP_DATA, "{}00".format(fileName[:len(fileName) - 2]))
            zip_path_to_save_rep = "{}.zip".format(path_to_save_rep)
            if not os.path.isfile(zip_path_to_save_rep):
                os.makedirs(path_to_save_rep, exist_ok=True)
                path_to_save_file = os.path.join(path_to_save_rep, fileLink)

                if not os.path.isfile(path_to_save_file):
                    request.urlretrieve(URL_BISON_FUTE_RRN + fileLink, path_to_save_file)
                    print(fileLink, " downloaded")
                else:
                    print(path_to_save_file, " already exists")
            else:
                print(zip_path_to_save_rep, " already exists")
