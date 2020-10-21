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
    def __init__(self, name, email, major):
        self.name = name
        self.email = email
        self.major = major

    def __str__(self):
        return self.name + ',' + self.email + ',' + self.major
    

'''
Search Directory
    Given a search query, this function returns the html generated for the search
    NOTE: This is currently broken, since the results are loaded with javascript 
    post: returns html search results
'''
def searchDirectory(search: str) -> str:
    # Construct URL
    search = search.replace(" ","+").replace(",", "%2C")
    urlBase = "https://directory.uci.edu/query/"
    otherParams = "?filter=all"
    url = urlBase + search + otherParams

    # Send search to uci directory
    htmlResult = requests.get(url)
    return htmlResult.text


'''
Get Vcard
    Given a UCInetID, this functions returns the vcard
    post: returns str vcard
'''
def getVcard(uci_net_id: str) -> str:
    # Send request for vcard
    vcardUrl = 'https://directory.uci.edu/people/' + uci_net_id + "/vcard"
    vcard = requests.get(vcardUrl)
    
    # Hack(chase): verify that this is vcard by checking the first letter
    #   It should be "B" for "BEGIN:VCARD"    
    if vcard.text[0] == 'B': return vcard.text
    else: return None


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
            vcard[lineData[0].split(';')[0].strip()] = lineData[1].strip()
    
    full_name = vcard["FN"] if "FN" in vcard else ""
    email = vcard["EMAIL"] if "EMAIL" in vcard else ""
    title = vcard["TITLE"] if "TITLE" in vcard else ""
    return Person(full_name, email, title)


'''
Find Person
    Given a search, this function returns a Person object or None if person not found
'''
def findPerson(search: str) -> Person:
    # Get vcard
    vcard = getVcard(search)

    # Assert that vcard exists
    if vcard == None:
        return None

    # Convert vcard to Person
    person = vcardToPerson(vcard)

    return person
    


'''
Multi Search
    Given a list of search queries, print the results
'''
def multiSearch(searches: [str]):
    print("Printing search results. . .")
    print("search,name,email")
    results = []
    for search in searches:
        results.append(findPerson(search))
        print(search + "," + str(results[-1]))

    print()

    option1 = '[1] Display all info'
    option2 = '[2] Display emails only'
    option3 = '[3] Display names only'
    option4 = '[4] Display majors only'
    optionh = '[h] Help - Display these instructions'
    optiond = '[d] Done - Enter a new search'

    instructions = "How would you like to display the information?\n    " + "\n    ".join([option1, option2, option3, option4, optionh, optiond])
        
    print(instructions)
    
    while True:
        response = input("  Enter display command: ")

        if response == '1':
            print("Printing everything. . .")
            for result in results: print(str(result))
        elif response == '2':
            print("Printing emails. . .")
            for result in results:
                print(str(result.email)) if type(result) == Person else print(result)
        elif response == '3':
            print("Printing names. . .")
            for result in results:
                print(str(result.name)) if type(result) == Person else print(result)
        elif response == '4':
            print("Printing majors. . .")
            for result in results:
                print(str(result.major)) if type(result) == Person else print(result)
        elif response == 'h':
            print(instructions)
        elif response == 'd':
            break
        else:
            print("INVALID COMMAND")
            print("  Type 'h' for a list of valid commands")

'''
[1] Single Search
    Look up one person
'''
def singleSearch():
    print(option1[4:])
    print(findPerson(input("  Search: ")))
    
'''
[2] Multi Search
    Look up multiple people at a time
'''
def multiSearchFromInput():
    print(option2[4:])
    print("Input each search on a new line. Enter 'done' when you are finished")

    # Read input for search queries
    searches = []
    search = input()
    while search != "done":
        searches.append(search.split('@')[0])
        search = input()
        
    print()
    multiSearch(searches)

'''
[3] Multi Search From File
    Look up multiple people from a file with a search query on each line
'''
def multiSearchFromFile():
    print(option3[4:])
    fileName = input("  Enter a file name: ")

    file = open(fileName)
    searches = [line.strip() for line in file]

    print()
    multiSearch(searches)



if __name__ == "__main__":
    # Print welcome message
    print("UCI Lookup")
    print()
    
    # Instructions for UI
    option1 = '[1] Single Search - Look up one person'
    option2 = '[2] Multi Search - Look up multiple people at a time'
    option3 = '[3] Multi Search From File - Look up multiple people from a file with a search querey on each line'
    optionh = '[h] Help - Display these instructions'
    optionq = '[q] Quit - End program'
    instructions = "Select one of the following options:\n  " + "\n  ".join([option1, option2, option3, optionh, optionq])

    # Print Instructions
    print(instructions)
    print()

    while(True):
        response = input("Enter Command: ")

        if response == '1':
            singleSearch()
        elif response == '2':
            multiSearchFromInput()
        elif response == '3':
            multiSearchFromFile()
        elif response == 'h':
            print(instructions)
        elif response == 'q':
            break
        else:
            print("INVALID COMMAND")
            print("  Type 'h' for a list of valid commands")

        print()

    print("Exiting program. . .")
