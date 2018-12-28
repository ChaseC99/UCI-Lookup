import requests
from lxml import html

if __name__ == "__main__":
    # Construct URL
    search = input("enter search: ").replace(" ","+").replace(",", "%2C")
    urlBase = "https://directory.uci.edu/index.php?basic_keywords="
    otherParams = "&modifier=Starts+With&basic_submit=Search&checkbox_employees=Employees&checkbox_students=Students&checkbox_departments=Departments&form_type=basic_search"

    url = urlBase + search + otherParams

    # Send search to uci directory
    htmlResult = requests.get(url)
    tree = html.fromstring(htmlResult.text)
    results = tree.xpath("//a[contains(@href, '&form_type=vcard')]/@href")

    # Send request for vcard
    vcardUrl = 'https://directory.uci.edu/' + results[0]
    vcardText = requests.get(vcardUrl).text  
    vcardLines = vcardText.split('\n')

    # Convert response to a dict
    vcard = dict()
    for line in vcardLines:
        lineData = line.split(':',1)
        vcard[lineData[0].strip()] = lineData[1].strip() 

    # Print info
    print('Name: ' + vcard["FN"])
    print('Email: ' + vcard["EMAIL"])
    
