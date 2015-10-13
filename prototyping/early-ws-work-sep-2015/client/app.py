#!/usr/bin/python3
import sys
import requests
import json
from requests.auth import HTTPBasicAuth

def do_printAllTasks(taskURI='http://localhost:5000/'):
    """
    do_printAllTasks()

    Execute the web service request and retrieve
    all tasks. Then, add the tasks to a list
    (returnList) which will be returned to the user

    REMEMBER: This test strap REQUIRES to import requests:

    $ sudo -H pip install requests

    """

    returnList = []
    data = get_data(taskURI)
    for t in data['tasks']:
        returnList.append(t['uri'])
    return returnList

def get_data(taskURI='http://localhost:5000/'):
    r = requests.get(taskURI + "tasks")
    data = r.json()
    return data

def printEachTask(taskURI='http://localhost:5000/'):
    data = get_data(taskURI)
    for t in data['tasks']:
        print("Title:", t['title'])
        print("Description: ", t["description"])
        print("Complete: ", t["done"])
        print("link: ", t['uri'])
        print()

def getTaskString(uri):
    task = getTask(uri)
    returnValue = str(task['uri']) + ' ' + task['title'] + ' (' + task['description']+ ') ' + str(task['done'])
    return returnValue

def getTask(uri):
    r2 = requests.get(uri)
    task = r2.json()['task']
    task0 = task[0]
    return {'uri':task0['uri'], 'title':task0['title'], 'description':task0['description'], 'done':task0['done']}

def insertTask(title, description, done=False, taskURI='http://localhost:5000/'):
    payload = {'title':title, 'description':description, 'done':done}
    headers = {'Content-Type':'application/json'}
    uri = taskURI + 'tasks'
    r3 = requests.post(uri, data=json.dumps(payload), headers=headers)
    return r3.text

def updateTask(uri, title, description, done):
    payload = {'title':title, 'description':description, 'done':done}
    headers = {'Content-Type':'application/json'}
    r4 = requests.put(uri, data=json.dumps(payload), headers=headers)
    return r4.text

def deleteTask(uri):
    headers = {'Content-Type':'application/json'}
    r5 = requests.delete(uri, headers=headers)
    return r5.text

def do_Tests(wsURI='http://localhost:5000/'):
    print("Step 1: Getting list of tasks")
    returnList = do_printAllTasks(wsURI)
    for uriLink in returnList:
        print('URI:', uriLink)
    print()

    print('Step 2: Get each task')
    printEachTask(wsURI)
    print('')

    print('Step 3: Get task string with ID = 1')
    print(getTaskString(wsURI + "tasks/1"))
    print('')

    print('Step 4: Get task string with ID = 2')
    print(getTaskString(wsURI + "tasks/2"))
    print('')

    print('Step 5: Get task list with ID = 1')
    print(getTask(wsURI + "tasks/1"))
    print('')

    print('Step 6: Get task list with ID = 2')
    print(getTask(wsURI + "tasks/2"))
    print('')

    print('Step 7: Add a task')
    print(insertTask('Watch TV', 'Watch Mixology to relax', False, taskURI=wsURI))

    print('Step 8: Add a task')
    print(insertTask('Switch off your TV', 'and go and do something less boring instead!', False, taskURI=wsURI))

    print('Step 9: Update a task')
    data = get_data(wsURI)
    print(updateTask(data['tasks'][0]['uri'], 'New Title', 'New Description', True))

    if len(returnList) > 5:
        print('Step 10: Delete fifth task in the list')
        print(deleteTask(returnList[4]))

    print("Program end")

if __name__ == "__main__":
   argURI = "";
   if len(sys.argv) < 2:
       print ("Usage: {0} url".format(sys.argv[0]), file=sys.stderr)
       print ("Where url is the web service URI")
   else:
       argURI = sys.argv[1]
       if argURI[len(argURI)-1:] == "/":
           do_Tests(argURI)
       else:
           do_Tests(argURI + "/")
