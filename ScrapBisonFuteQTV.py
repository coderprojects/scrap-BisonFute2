import os
from urllib import request
import re
import xml.etree.ElementTree as ET
from datetime import datetime

BF_EXTENSION = "ext"
BF_LOCATION = "location"
BF_DAY = "day"
BF_TIME = "time"

REP_DATA = "QTV_Data"
URL_BISON_FUTE_QTV = "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/QTV-DIR/qtvDir.xml"

def get_namespace(element):
  m = re.match('\{.*\}', element.tag)
  return m.group(0) if m else ''

# The filename doesn't contain a date so we have to get the date from the XML file
def getPublicationDate(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    namespace = get_namespace(root)
    publicationTime = root.find('./{0}payloadPublication/{0}publicationTime'.format(namespace)).text
    return publicationTime

def hasExtension(href, ext):
    list_elt_href = href.split(".")
    return list_elt_href[-1] == ext


os.makedirs(REP_DATA, exist_ok=True)

request_text = request.urlopen(URL_BISON_FUTE_QTV)
publicationDate = getPublicationDate(request_text)
if publicationDate:
    publicationDate = datetime.strptime(publicationDate, '%Y-%m-%dT%H:%M:%S.%f%z')
    # Get the day from publication date for the directory
    publicationDay = publicationDate.strftime('%Y%m%d')
    # Get the day from publication date for the output file name
    publicationTime = publicationDate.strftime('%H%M%S')
    path_to_save_rep = os.path.join(REP_DATA, publicationDay)
    os.makedirs(path_to_save_rep, exist_ok=True)
    path_to_save_file = os.path.join(path_to_save_rep, "qtvDir_{}_{}.xml".format(publicationDay, publicationTime))
    if not os.path.isfile(path_to_save_file):
        request.urlretrieve(URL_BISON_FUTE_QTV, path_to_save_file)
        print(URL_BISON_FUTE_QTV, " downloaded")
    else:
        print(path_to_save_file, " already exists")