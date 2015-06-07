import xml.etree.ElementTree as ET
from dbxml import *

__author__ = 'master'

error_file_exists = 'Lab with this name already exists'
result_OK = 'OK'
error_no_file = 'No file with this name'

collection_name = 'labs.dbxml'


# CREATE
# Creates lab with name and fields about and state
# Returns result of updating (error or success)
# If lab with this name already exist returns error message
def add(name, about=' ', state=' '):
    mgr = XmlManager()
    container = mgr.openContainer(collection_name)
    uc = mgr.createUpdateContext()
    try:
        container.putDocument(name, '<lab><about>%s</about><state>%s'
                                    '</state></lab>' % (about, state), uc)
    except:
        return error_file_exists
    return result_OK


# READ
# Reads all data (all labs in our case) from database
# Returns JSON-style list of dictionaries
def read():
    mgr = XmlManager()
    # Unused, but in other case function doesn't work
    container = mgr.openContainer("labs.dbxml")
    qc = mgr.createQueryContext()
    results = mgr.query("collection('%s')" % collection_name, qc)
    results.reset()

    items = []
    for value in results:
        document = value.asDocument()
        tree = ET.fromstring(value.asString())
        about = tree.find('about').text
        state = tree.find('state').text
        items.append({"name": document.getName(),
                      "about": about, "state": state})
    return items


# UPDATE
# Updates in lab with name field with new value
# Returns result of updating (error or success)
def update(name, field, new_value):
    mgr = XmlManager()
    uc = mgr.createUpdateContext()

    container = mgr.openContainer("labs.dbxml")

    document = container.getDocument(name)
    name = document.getName()
    content = document.getContent()

    if field == 'name':
        try:
            document.setName(new_value)
            container.updateDocument(document, uc)
        except:
            return error_file_exists
        return result_OK

    tree = ET.fromstring(content)
    tree.find(field).text = new_value

    content_new = ET.tostring(tree, encoding="utf8", method="html")

    document.setContent(content_new)
    container.updateDocument(document, uc)

    return result_OK


# DELETE
# Deletes lab with name from database
# If there is no lab with that name returns error message
def delete(name):
    mgr = XmlManager()
    container = mgr.openContainer(collection_name)
    uc = mgr.createUpdateContext()

    try:
        container.deleteDocument(name, uc)
    except:
        return error_no_file
    return result_OK


if __name__ == '__main__':
    # Testing
    print('Before')
    for item in read():
        print(item)

    # print('\n' + add('Lab 5', 'Unknown', 'Don\'t know nothing about it'))
    # print('\n' + delete('Lab for test'))
    # print('\n' + update('Lab 5', 'about', 'Don\'t know'))

    print('\nAfter')
    for item in read():
        print(item)
