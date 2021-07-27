
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#THIS WILL TRUNCATE BOTH TAG TABLES AND ALL RESOURCES! 
#               USE WITH EXTREME CAUTION!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin@123",
  database="main_db"
)

mycursor = mydb.cursor()

sql = "SET FOREIGN_KEY_CHECKS = 0;TRUNCATE TABLE resource_tag;SET FOREIGN_KEY_CHECKS = 1;" 
for result in mycursor.execute(sql, multi=True):
    print(result.fetchall())
sql = "SET FOREIGN_KEY_CHECKS = 0;TRUNCATE TABLE resource_resource_tags;SET FOREIGN_KEY_CHECKS = 1;" 
for result in mycursor.execute(sql, multi=True):
    print(result.fetchall())
    sql = "SET FOREIGN_KEY_CHECKS = 0;TRUNCATE TABLE resource_resource;SET FOREIGN_KEY_CHECKS = 1;" 
for result in mycursor.execute(sql, multi=True):
    print(result.fetchall())

agetags = [
    "All ages","Infant (0-1 years)","Toddler (1-3 years)","Preschool (3-4 years)","Child/Youth (0-17 years)","Child/Youth (0-13 years)","Adolescents/Teens (13-17 years)",
    "Transitional age (16-24 years)","Adult (18+)","Older Adult (55+)"
]

for tag in agetags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Age Group', 1);" 
    mycursor.execute(sql)

langtags = [
    "English","French","Panjabi (Punjabi)","Spanish","Italian","German","Cantonese",
    "Tagalog (Pilipino, Filipino)","Arabic","Mandarin","Portuguese","Cree","Ojibway","Oji Cree","Montagnais (Innu)","Mi''kmaq","Atikamekw","Blackfoot",
    "Inuktitut","Dene","Shuswap (Secwepemctsin)","Stoney","Mohawk","Gitxsan (Gitksan)","Kwakiutl (Kwak''wala)","Michif","Haida","Tlingit","Kutenai",
    "Chinese Simplified","Chinese Traditional"
]
for tag in langtags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Language', 1);" 
    mycursor.execute(sql)

orgtags = ["MDSC"]
for tag in orgtags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Org Group', 1);" 
    mycursor.execute(sql)

healthtag = [
    "Abuse","Acquired Immune Deficiency Syndrome (AIDS)","Addictions (including Drugs, Alcohol and Gambling)",
    "All/Any","Anger","Anorexia","Antisocial Personality Disorder (ASPD), Psychopathy, and Conduct Disorder","Anxiety","Asperger Syndrome","Attachment Problems",
    "Attention Deficit Disorders (ADD/ADHD)","Auditory Processing Disorder (APD)","Autism and Autism Spectrum Disorders","Behaviour and Conduct Problems",
    "Bipolar Disorders","Borderline Personality Disorder (BPD)","Bulimia","Bullying","Cancer","Adjustment disorders ","Delirium","Dementia including Alzheimer''s",
    "Depression","Developmental Coordination Disorder (DCD)","Developmental, Intellectual Delay and Disabilities","Personality disorders",
    "Domestic Violence","Down syndrome","Eating Disorders including Anorexia and Bulimia","Elimination Disorders",
    "Fetal Alcohol and Fetal Alcohol Spectrum Disorders (FASD)","Firesetting","Gender Identity Issues","General well-being","General Distress",
    "Grief and Bereavement","Hoarding","Infant and Early Childhood Mental Health (IECMH)","Insomnia","Learning Disorders","Medication Treatment",
    "Mental Health in General","Mood Disorders","Obsessive Compulsive Disorder (OCD)","Operational Stress Injury (OSI)",
    "Oppositional behaviours including oppositional defiant disorder (ODD)","Overweight and Obesity",
    "Pandemic (e.g. COVID/Coronavirus), Disasters and Related Emergencies","Parenting","Physical Disabilities",
    "Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse","Resiliency","Schizophrenia and Psychosis","School Refusal (and School Phobia)",
    "Self-harm including Self-cutting","Sensory Processing Disorders and Self-Regulation Problems","Separation and Divorce","Sleep Problems and Disorders",
    "Social Skills and Life Skills","Somatoform Disorders","Speech and Language","Stress","Substance use","Suicidal Ideation",
    "Technology Issues, including Internet, Cellphone, Social Media Addiction","Tourette Syndrome and Tic Disorders", "COVID-19"
]
for tag in healthtag:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Health Issue Group', 1);" 
    mycursor.execute(sql)

usertags = [
    "Healthcare worker/Nurse","Healthcare worker/Practising or Retired Physician","Healthcare worker/Other","Healthcare worker/First Responder",
    "Healthcare worker/Medical Student","Healthcare worker/Resident Doctor","Military","Veterans","General Public / All",
    "Family member of physician or medical learner","Family member of healthcare worker (other)"
]
for tag in usertags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'User Group', 1);" 
    mycursor.execute(sql)

gendertags = ["Male","Female", "Gender fluid, non-binary, and/or two spirit", "Any/General", "LGBTQ2s+"]
for tag in gendertags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Gender/Orientation Group', 1);" 
    mycursor.execute(sql)

timetags = [
    "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","24/7","From 1am","From 2am","From 3am","From 4am","From 5am","From 6am","From 7am",
    "From 8am","From 9am","From 10am","From 11am","From 12am","From 1pm","From 2pm","From 3pm","From 4pm","From 5pm","From 6pm","From 7pm","From 8pm","From 9pm",
    "From 10pm","From 11pm","From 12pm","Until 1am","Until 2am","Until 3am","Until 4am","Until 5am","Until 6am","Until 7am","Until 8am","Until 9am","Until 10am",
    "Until 11am","Until 12am","Until 1pm","Until 2pm","Until 3pm","Until 4pm","Until 5pm","Until 6pm","Until 7pm","Until 8pm","Until 9pm","Until 10pm","Until 11pm",
    "Until 12pm"
]
for tag in timetags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Dates and Times', 1);" 
    mycursor.execute(sql)


locationtags = ["All Canada","Alberta Wide","Nova Scotia Wide","Alberta City","Alberta Region","Nova Scotia City","Nova Scotia Region"]
for tag in locationtags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Locations', 1);" 
    mycursor.execute(sql)


albertaCityTags = [
    "Abee","Acadia","Aetna","Airdrie","Alder","Aldersyde","Alexander","Brooks","Calgary","Camrose","Canmore","Cochrane","Cold Lake","Edmonton",
    "Fort Sasketchewan","Grand Centre (Cold Lake)","Grande Prairie","High River","Lacombe","Leduc","Lethbridge","Lloydminster","Medicine Hat","Okotoks","Red Deer",
    "Spruce Grove","St. Albert","Stony Plain","Strathmore","Sylvan Lake","Wetaskiwin","Wood Buffalo (Fort McMurray)"
]
for tag in albertaCityTags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Locations/Alberta Cities', 1);" 
    mycursor.execute(sql)


albertaRegionTags = [
    "Aspen Regional Health","Calgary Health Region","Capital Health","Chinook Health Region","David Thompson Health Region","East Central Health",
    "Northern Lights Health Region","Palliser Health Region","Peace Country"
]
for tag in albertaRegionTags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Locations/Alberta Regions', 1);" 
    mycursor.execute(sql)

nsCityTags = [
    "Advocate","Amherst","Annapolis","Antigonish","Baddeck","Berwick","Bridgewater","Canso","Dartmouth","Digby","Elmsdale","Evanston","Fall River","Glace Bay",
    "Guysborough","Halifax","Inverness","Kentville","Liverpool","Lower Sackville","Lunenburg","Middle Musquodoboit","Middleton","Musquodoboit Harbour",
    "Neil''s Harbour","New Glasgow","New Waterford","North Sydney","Parrsboro","Pictou","Pugwash","Sheet Harbour","Shelburne","Sherbrooke","Springhill",
    "Sydney","Tatamagouche","Truro","Windsor","Wolfville","Yarmouth"
]
for tag in nsCityTags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Locations/Nova Scotia Cities', 1);" 
    mycursor.execute(sql)

nsRegionTags = ["Central Nova Scotia","Eastern Nova Scotia","Northern Nova Scotia","Western Nova Scotia"]
for tag in nsRegionTags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Locations/Nova Scotia Regions', 1);" 
    mycursor.execute(sql)

resCatTags = ["Peer-Support","Crisis Support/Distress Counselling","Online Course/Webinar","Informational (text, document, and/or video for information only)"]
for tag in resCatTags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Resource Category', 1);" 
    mycursor.execute(sql)

resFormatTags = ["Website","Definition/Stat","Phone Number","Online Chat","Email","Online Course","Video","Picture/Graphic","Physical Address","Text Messaging"]
for tag in resFormatTags:
    sql = "INSERT INTO resource_tag(name, tag_category, approved) VALUES ('" + tag + "', 'Resource Format', 1);" 
    mycursor.execute(sql)

mydb.commit()
print(mycursor.rowcount, " tags inserted.")