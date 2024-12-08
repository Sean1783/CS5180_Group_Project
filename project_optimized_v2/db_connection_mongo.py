from pymongo import MongoClient

def connectDataBase():
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")

def createPage(col, url, html, status_message):
    page = {
        "url": url,
        "html": html,
        "status_message": status_message,
        "target": False
    }
    col.insert_one(page)

def findPage(col, query):
    return col.find_one(query)

def findPages(col, query):
    return col.find(query)

def flagPage(col, url):
    return col.update_one({ 'url': url }, { "$set": { "target": True } })

def addProfessor(col, name, title_department, email, phone, office, office_hours, sections, accolades, navigation_links):
    professor = {
        "name": name,
        "title_department": title_department,
        "email": email,
        "phone": phone,
        "office": office,
        "office_hours": office_hours,
        "sections": sections,
        "accolades": accolades,
        "navigation_links": navigation_links
    }
    col.insert_one(professor)