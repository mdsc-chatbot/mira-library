import mysql.connector
import csv
from HeaderToFieldLookup import getVer, getSQLIndex
from sys import exit

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin@123",
  database="main_db"
)

mycursor = mydb.cursor()

taglist = []
fields = "("
fieldvalues = []
valuessql = "("

maxdistress = -1
mindistress = 11
#try:
with open('./data.csv',newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    #get row lables
    needHeader = True
    for row in reader:
      if needHeader:
        version = getVer(row)
        needHeader = False
        continue
      for i in range(len(row)):
        field = row[i]
        if field != "":
          tag = getSQLIndex(version, i, field)
          if tag == -1:
            print("Stopping import. Import will be rolled back. See above error for details.")
            mydb.rollback()
            exit("Quitting.")
          if tag <= 12:
            #handle field entry
            if tag == 0: #skip tags
              continue 
            elif tag == 1: #username
              fields+="created_by_user, "
              fieldvalues.append(str("FROM IMPORT: " + field))
              valuessql+="%s, "
            elif tag == 2: #title
              fields+="title, "
              fieldvalues.append(field)
              valuessql+="%s, "
            elif tag == 4: #resource description
              fields+="description, "
              fieldvalues.append(field)
              valuessql+="%s, "
            elif tag == 5: #resource type
              fields+="resource_type, "
              if field == "Information/Education (user intent: information or learning more about a topic)":
                fieldvalues.append("RS")
              elif field == "Both":
                fieldvalues.append("BT")
              elif field == "A program or service (user intent: mental health system navigation)":
                fieldvalues.append("SR")
              else:
                print("Unknown resource type '" + field + "'")
                mydb.rollback()
                exit("Rollback finished. Quitting.")
              valuessql+="%s, "
            elif tag == 6: #distress
              if i == 19:
                mindistress = min(mindistress, 8)
                maxdistress = max(maxdistress, 10)
              elif i == 20:
                mindistress = min(mindistress, 5)
                maxdistress = max(maxdistress, 7)
              elif i == 21:
                mindistress = min(mindistress, 1)
                maxdistress = max(maxdistress, 4)
            elif tag == 9: #specific url
              fields+="url, "
              fieldvalues.append(field)
              valuessql+="%s, "
            elif tag == 8:
              fields+="general_url, "
              fieldvalues.append(field)
              valuessql+="%s, "
            elif tag == 10:
              fields+="definition, "
              fieldvalues.append(field)
              valuessql+="%s, "
            elif tag == 11:
              fields+="`references`, "
              fieldvalues.append(field)
              valuessql+="%s, "
            else:
              print("Unknown field tag '" + tag + "'")
              mydb.rollback()
              exit("Rollback finished. Quitting.")
          else:
            taglist.append(tag - 12)
          
      #add final distress values for row
      if mindistress > 0 and maxdistress < 11:
        fields+="distress_level_min, "
        fieldvalues.append(mindistress)
        valuessql+="%s, "
        fields+="distress_level_max, "
        fieldvalues.append(maxdistress)
        valuessql+="%s, "

      fields+="attachment, category_id, public_view_count, review_status)"
      fieldvalues.append('')
      fieldvalues.append(1)
      fieldvalues.append(0)
      fieldvalues.append("approved")
      valuessql+="%s, %s, %s, %s)"

      #insert record and return auto-id
      sql = "INSERT INTO resource_resource " + fields + " VALUES " + valuessql +";"
      mycursor.execute(sql, fieldvalues)

      #mydb.commit()
      id = mycursor.lastrowid

      #add related tags using tag list and retrived auto-id
      for tag in taglist:
        sql = "INSERT INTO resource_resource_tags (tag_id, resource_id) VALUES (%s, %s);"
        mycursor.execute(sql,(tag, id))

      #clear data for next row
      taglist = []
      fields = "("
      fieldvalues = []
      valuessql = "("
      maxdistress = -1
      mindistress = 11
#except:
  #mydb.rollback()
  #exit("Unknown Error. Quitting.")

#finally commit
mydb.commit()
#mydb.rollback()
print(mycursor.rowcount, "records inserted.")
print("Import successful")