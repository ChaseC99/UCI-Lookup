# IMPORTS
from ldap3 import Connection

# CLASSES
'''
Person
    This class represents a person at UCI.
    Attributes:
        name - str
        email - str
'''
class Person:
    def __init__(self, entry):
        self.allInfo = entry
        self._parse_entry()
    
    def _parse_entry(self):
        entry = self.allInfo

        # Get Name
        self.name = str(entry['displayName']) if 'displayName' in entry else ''
        
        # Get UCINetID
        self.netID = str(entry['uid']) if 'uid' in entry else ''

        # Get Email
        self.email = str(entry['mail']) if 'mail' in entry else ''

        # Get Major
        self.major = str(entry['major']) if 'major' in entry else ''

        # Get Year
        self.year = str(entry['uciStudentLevel']) if 'uciStudentLevel' in entry else ''
        
    def __str__(self):
        return self.netID + ',' + self.name + ',' + self.email + ',' + self.major + ',' + self.year
    

# INFORMATION RETRIEVAL
#   The following functions are how we retrieve individual's information
#   from OIT's LDAP Directory Information 
'''
Entry To Person
    LDAP3 returns an entry object with lots of information on the individual.
    This function takes that information and converts it to a Person object.
    Return a Person
'''
def _entryToPerson(entry) -> Person:
    return Person(entry)


'''
Establish Connection
    Set up a connection with LDAP3
    Return a Connection object
'''
def _establishConnection():
    return Connection("ldap://ldap.oit.uci.edu", auto_bind=True)


'''
Find Person
    Given a single UCINetID, return the assosiated person
    If no results are found, return None
'''
def findPerson(netID: str) -> Person:
    conn = _establishConnection()
    conn.search("dc=uci,dc=edu", f"(uid={netID})", attributes=['*'])

    if conn.entries:
        return _entryToPerson(conn.entries[0])
    
    return None


'''
Find People
    Given a list of UCINetIDs, return the available person objects
'''
def findPeople(netIDs: [str]) -> Person:
    conn = _establishConnection()
    # To search for multiple people, we structure our query like so
    #   (|(uid=person1)(uid=person2)(uid=person3))
    search_query = '(|' + ''.join(['(uid='+netID+')' for netID in netIDs]) + ')'
    conn.search("dc=uci,dc=edu", search_query, attributes=['*'])

    # Convert results to Person objects
    results = []
    for entry in conn.entries:
        results.append(_entryToPerson(entry))

    # Sort Person objects by NetID
    results.sort(key=lambda person: person.netID)

    return results


# CLI INTERFACE
#   The following code provides a CLI interface for the user to access
#   information from OIT's LDAP Directory Information 
'''
Multi Search
    Given a list of search queries, print the results
'''
def multiSearch(searches: [str]):
    print("Loading results. . .")
    results = findPeople(searches)
    
    print("Printing search results. . .")
    found_netIDs = set()
    for result in results:
        print(str(result))
        found_netIDs.add(result.netID)
    print()

    missing_netIDs = set()
    for search in searches:
        if not search in found_netIDs:
            missing_netIDs.add(search)
    
    if missing_netIDs:
        print("Unable to find the following searches:", missing_netIDs)
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
        print()
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
    person = findPerson(input("  Search: ").split('@')[0])
    print(person)

    displayAllInfo = input('\n  Show all info? [y/N]: ') in {'y', 'Y'}
    if displayAllInfo:
        print("Displaying all info. . .\n")
        print(person.allInfo)

    
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
