import requests
from lxml import html

'''
Person
    This class represents a person at UCI.
    Attributes:
        name - str
        email - str
'''
class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return self.name + ',' + self.email
    

'''
Search Directory
    Given a search query, this function returns the html generated for the search
    post: returns html search results
'''
def searchDirectory(search: str) -> str:
    # Construct URL
    search = search.replace(" ","+").replace(",", "%2C")
    urlBase = "https://directory.uci.edu/index.php?basic_keywords="
    otherParams = "&modifier=Starts+With&basic_submit=Search&checkbox_employees=Employees&checkbox_students=Students&checkbox_departments=Departments&form_type=basic_search"
    url = urlBase + search + otherParams

    # Send search to uci directory
    htmlResult = requests.get(url)
    return htmlResult.text


'''
Get Vcard
    Given html search results, this functions pulls out the vcard
    post: returns str vcard
'''
def getVcard(htmlText: str) -> str:
    # Pull vcard link from html
    tree = html.fromstring(htmlText)
    results = tree.xpath("//a[contains(@href, '&form_type=vcard')]/@href")

    # Assert that vcard for that search exists
    if len(results) == 0:
        return None

    # Send request for vcard
    vcardUrl = 'https://directory.uci.edu/' + results[0]
    vcard = requests.get(vcardUrl)
    return vcard.text


'''
Vcard to Person
    Converts a vcard to a Person object
    post: returns a Person object or None if vcard doesn't exist
'''
def vcardToPerson(vcardText: str) -> Person:
    vcardLines = vcardText.split('\n')

    # Convert response to a dict
    vcard = dict()
    for line in vcardLines:
        lineData = line.split(':',1)
        if len(lineData) == 2:
            vcard[lineData[0].strip()] = lineData[1].strip()

    return Person(vcard["FN"], vcard["EMAIL"])


'''
Find Person
    Given a search, this function returns a Person object or None if person not found
'''
def findPerson(search: str) -> Person:
    # Get HTML from search
    htmlResult = searchDirectory(search)

    # Get vcard
    vcard = getVcard(htmlResult)

    # Assert that vcard exists
    if vcard == None:
        return None

    # Convert vcard to Person
    person = vcardToPerson(vcard)

    return person
    


if __name__ == "__main__":
    print(findPerson(input("search: ")))
