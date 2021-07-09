import csv
import mysql.connector

ver1line = ["COMPLETE,RESPNUM,RESPONDENT,UIP,StartDate,StartTime,endDate,EndTime,Timetaken,UID,LONGITUDE,LATITUDE,browser,os,Q24_Name_Enter_01,Q2_Name_01,Q3_OrgDesc_01,Q4_OrgServGeneral_01,Q11_Resource_Type,Q8_Distress_01,Q8_Distress_02,Q8_Distress_03,Q8_Distress_04,Q8_Distress_04_V,Q9_Category_User_01,Q9_Category_User_02,Q9_Category_User_03,Q9_Category_User_04,Q9_Category_User_05,Q9_Category_User_06,Q9_Category_User_07,Q9_Category_User_08,Q9_Category_User_09,Q9_Category_User_10,Q9_Category_User_11,Q9_Category_User_12,Q9_Category_User_13,Q9_Category_User_14,Q9_Category_User_15,Q9_Category_User_16,Q9_Category_User_16_V,Q25_Language_01,Q25_Language_02,Q25_Language_03,Q25_Language_04,Q25_Language_05,Q25_Language_06,Q25_Language_07,Q25_Language_08,Q25_Language_09,Q25_Language_10,Q25_Language_11,Q25_Language_12,Q25_Language_13,Q25_Language_14,Q25_Language_15,Q25_Language_16,Q25_Language_17,Q25_Language_18,Q25_Language_19,Q25_Language_20,Q25_Language_21,Q25_Language_22,Q25_Language_23,Q25_Language_24,Q25_Language_25,Q25_Language_26,Q25_Language_27,Q25_Language_28,Q25_Language_29,Q25_Language_30,Q25_Language_30_V,Q15_Service_Program_Type_01,Q15_Service_Program_Type_02,Q15_Service_Program_Type_03,Q15_Service_Program_Type_04,Q15_Service_Program_Type_05,Q15_Service_Program_Type_05_V,Q13_Age_01,Q13_Age_02,Q13_Age_03,Q13_Age_04,Q13_Age_05,Q13_Age_06,Q13_Age_07,Q13_Age_08,Q13_Age_09,Q13_Age_10,Q13_Age_11,Q13_Age_11_V,Q12_Province_01,Q12_Province_02,Q12_Province_03,Q12_Province_04,Q12_Province_05,Q12_Province_06,Q12_Province_06_V,Q27_Alberta_City_Region_01,Q27_Alberta_City_Region_02,Q27_Alberta_City_Region_03,Q27_Alberta_City_Region_04,Q27_Alberta_City_Region_05,Q27_Alberta_City_Region_06,Q27_Alberta_City_Region_07,Q27_Alberta_City_Region_08,Q27_Alberta_City_Region_09,Q27_Alberta_City_Region_10,Q27_Alberta_City_Region_11,Q27_Alberta_City_Region_12,Q27_Alberta_City_Region_13,Q27_Alberta_City_Region_14,Q27_Alberta_City_Region_15,Q27_Alberta_City_Region_16,Q27_Alberta_City_Region_17,Q27_Alberta_City_Region_18,Q27_Alberta_City_Region_19,Q27_Alberta_City_Region_20,Q27_Alberta_City_Region_21,Q27_Alberta_City_Region_22,Q27_Alberta_City_Region_23,Q27_Alberta_City_Region_24,Q27_Alberta_City_Region_25,Q27_Alberta_City_Region_26,Q27_Alberta_City_Region_27,Q27_Alberta_City_Region_28,Q27_Alberta_City_Region_29,Q27_Alberta_City_Region_30,Q27_Alberta_City_Region_31,Q27_Alberta_City_Region_32,Q27_Alberta_City_Region_33,Q27_Alberta_City_Region_34,Q27_Alberta_City_Region_35,Q27_Alberta_City_Region_36,Q27_Alberta_City_Region_37,Q27_Alberta_City_Region_38,Q27_Alberta_City_Region_39,Q27_Alberta_City_Region_40,Q27_Alberta_City_Region_41,Q27_Alberta_City_Region_42,Q27_Alberta_City_Region_42_V,Q29_Nova_Scotia_City_Region_01,Q29_Nova_Scotia_City_Region_02,Q29_Nova_Scotia_City_Region_03,Q29_Nova_Scotia_City_Region_04,Q29_Nova_Scotia_City_Region_05,Q29_Nova_Scotia_City_Region_06,Q29_Nova_Scotia_City_Region_07,Q29_Nova_Scotia_City_Region_08,Q29_Nova_Scotia_City_Region_09,Q29_Nova_Scotia_City_Region_10,Q29_Nova_Scotia_City_Region_11,Q29_Nova_Scotia_City_Region_12,Q29_Nova_Scotia_City_Region_13,Q29_Nova_Scotia_City_Region_14,Q29_Nova_Scotia_City_Region_15,Q29_Nova_Scotia_City_Region_16,Q29_Nova_Scotia_City_Region_17,Q29_Nova_Scotia_City_Region_18,Q29_Nova_Scotia_City_Region_19,Q29_Nova_Scotia_City_Region_20,Q29_Nova_Scotia_City_Region_21,Q29_Nova_Scotia_City_Region_22,Q29_Nova_Scotia_City_Region_23,Q29_Nova_Scotia_City_Region_24,Q29_Nova_Scotia_City_Region_25,Q29_Nova_Scotia_City_Region_26,Q29_Nova_Scotia_City_Region_27,Q29_Nova_Scotia_City_Region_28,Q29_Nova_Scotia_City_Region_29,Q29_Nova_Scotia_City_Region_30,Q29_Nova_Scotia_City_Region_31,Q29_Nova_Scotia_City_Region_32,Q29_Nova_Scotia_City_Region_33,Q29_Nova_Scotia_City_Region_34,Q29_Nova_Scotia_City_Region_35,Q29_Nova_Scotia_City_Region_36,Q29_Nova_Scotia_City_Region_37,Q29_Nova_Scotia_City_Region_38,Q29_Nova_Scotia_City_Region_39,Q29_Nova_Scotia_City_Region_40,Q29_Nova_Scotia_City_Region_41,Q29_Nova_Scotia_City_Region_42,Q29_Nova_Scotia_City_Region_43,Q29_Nova_Scotia_City_Region_44,Q29_Nova_Scotia_City_Region_45,Q29_Nova_Scotia_City_Region_46,Q29_Nova_Scotia_City_Region_46_V,Q10_MHConcern_01,Q10_MHConcern_02,Q10_MHConcern_03,Q10_MHConcern_04,Q10_MHConcern_05,Q10_MHConcern_06,Q10_MHConcern_07,Q10_MHConcern_08,Q10_MHConcern_09,Q10_MHConcern_10,Q10_MHConcern_11,Q10_MHConcern_12,Q10_MHConcern_13,Q10_MHConcern_14,Q10_MHConcern_15,Q10_MHConcern_16,Q10_MHConcern_17,Q10_MHConcern_18,Q10_MHConcern_19,Q10_MHConcern_20,Q10_MHConcern_21,Q10_MHConcern_22,Q10_MHConcern_23,Q10_MHConcern_24,Q10_MHConcern_25,Q10_MHConcern_26,Q10_MHConcern_27,Q10_MHConcern_28,Q10_MHConcern_29,Q10_MHConcern_30,Q10_MHConcern_31,Q10_MHConcern_32,Q10_MHConcern_33,Q10_MHConcern_34,Q10_MHConcern_35,Q10_MHConcern_36,Q10_MHConcern_37,Q10_MHConcern_38,Q10_MHConcern_39,Q10_MHConcern_40,Q10_MHConcern_41,Q10_MHConcern_42,Q10_MHConcern_43,Q10_MHConcern_44,Q10_MHConcern_45,Q10_MHConcern_46,Q10_MHConcern_47,Q10_MHConcern_48,Q10_MHConcern_49,Q10_MHConcern_50,Q10_MHConcern_51,Q10_MHConcern_52,Q10_MHConcern_53,Q10_MHConcern_54,Q10_MHConcern_55,Q10_MHConcern_56,Q10_MHConcern_57,Q10_MHConcern_58,Q10_MHConcern_59,Q10_MHConcern_60,Q10_MHConcern_61,Q10_MHConcern_62,Q10_MHConcern_63,Q10_MHConcern_64,Q10_MHConcern_65,Q10_MHConcern_66,Q10_MHConcern_67,Q10_MHConcern_67_V,Q5_Resource_Format_01,Q5_Resource_Format_02,Q5_Resource_Format_03,Q5_Resource_Format_04,Q5_Resource_Format_05,Q5_Resource_Format_06,Q5_Resource_Format_07,Q5_Resource_Format_08,Q5_Resource_Format_09,Q5_Resource_Format_10,Q5_Resource_Format_11,Q5_Resource_Format_11_V,Q6_General_URL_01,Q16_Specific_URL_01,Q17_Phone_01,Q18_Text_Messaging_01,Q20_Email_01,Q19_Address_01,Q23_Definition_or_stat_01,Q30_References_01,Q14_TimeZone_01,Q14_TimeZone_02,Q14_TimeZone_03,Q14_TimeZone_04,Q14_TimeZone_05,Q14_TimeZone_06,Q14_TimeZone_07,Q21_DaysofWeekHrs_01_01,Q21_DaysofWeekHrs_01_02,Q21_DaysofWeekHrs_01_03,Q21_DaysofWeekHrs_01_04,Q21_DaysofWeekHrs_01_05,Q21_DaysofWeekHrs_01_06,Q21_DaysofWeekHrs_01_07,Q21_DaysofWeekHrs_01_08,Q21_DaysofWeekHrs_01_09,Q21_DaysofWeekHrs_01_10,Q21_DaysofWeekHrs_01_11,Q21_DaysofWeekHrs_01_12,Q21_DaysofWeekHrs_01_13,Q21_DaysofWeekHrs_01_14,Q21_DaysofWeekHrs_01_15,Q21_DaysofWeekHrs_01_16,Q21_DaysofWeekHrs_01_17,Q21_DaysofWeekHrs_01_18,Q21_DaysofWeekHrs_01_19,Q21_DaysofWeekHrs_01_20,Q21_DaysofWeekHrs_01_21,Q21_DaysofWeekHrs_01_22,Q21_DaysofWeekHrs_01_23,Q21_DaysofWeekHrs_01_24,Q21_DaysofWeekHrs_01_25,Q21_DaysofWeekHrs_01_26,Q21_DaysofWeekHrs_02_01,Q21_DaysofWeekHrs_02_02,Q21_DaysofWeekHrs_02_03,Q21_DaysofWeekHrs_02_04,Q21_DaysofWeekHrs_02_05,Q21_DaysofWeekHrs_02_06,Q21_DaysofWeekHrs_02_07,Q21_DaysofWeekHrs_02_08,Q21_DaysofWeekHrs_02_09,Q21_DaysofWeekHrs_02_10,Q21_DaysofWeekHrs_02_11,Q21_DaysofWeekHrs_02_12,Q21_DaysofWeekHrs_02_13,Q21_DaysofWeekHrs_02_14,Q21_DaysofWeekHrs_02_15,Q21_DaysofWeekHrs_02_16,Q21_DaysofWeekHrs_02_17,Q21_DaysofWeekHrs_02_18,Q21_DaysofWeekHrs_02_19,Q21_DaysofWeekHrs_02_20,Q21_DaysofWeekHrs_02_21,Q21_DaysofWeekHrs_02_22,Q21_DaysofWeekHrs_02_23,Q21_DaysofWeekHrs_02_24,Q21_DaysofWeekHrs_02_25,Q21_DaysofWeekHrs_02_26,Q21_DaysofWeekHrs_03_01,Q21_DaysofWeekHrs_03_02,Q21_DaysofWeekHrs_03_03,Q21_DaysofWeekHrs_03_04,Q21_DaysofWeekHrs_03_05,Q21_DaysofWeekHrs_03_06,Q21_DaysofWeekHrs_03_07,Q21_DaysofWeekHrs_03_08,Q21_DaysofWeekHrs_03_09,Q21_DaysofWeekHrs_03_10,Q21_DaysofWeekHrs_03_11,Q21_DaysofWeekHrs_03_12,Q21_DaysofWeekHrs_03_13,Q21_DaysofWeekHrs_03_14,Q21_DaysofWeekHrs_03_15,Q21_DaysofWeekHrs_03_16,Q21_DaysofWeekHrs_03_17,Q21_DaysofWeekHrs_03_18,Q21_DaysofWeekHrs_03_19,Q21_DaysofWeekHrs_03_20,Q21_DaysofWeekHrs_03_21,Q21_DaysofWeekHrs_03_22,Q21_DaysofWeekHrs_03_23,Q21_DaysofWeekHrs_03_24,Q21_DaysofWeekHrs_03_25,Q21_DaysofWeekHrs_03_26,Q21_DaysofWeekHrs_04_01,Q21_DaysofWeekHrs_04_02,Q21_DaysofWeekHrs_04_03,Q21_DaysofWeekHrs_04_04,Q21_DaysofWeekHrs_04_05,Q21_DaysofWeekHrs_04_06,Q21_DaysofWeekHrs_04_07,Q21_DaysofWeekHrs_04_08,Q21_DaysofWeekHrs_04_09,Q21_DaysofWeekHrs_04_10,Q21_DaysofWeekHrs_04_11,Q21_DaysofWeekHrs_04_12,Q21_DaysofWeekHrs_04_13,Q21_DaysofWeekHrs_04_14,Q21_DaysofWeekHrs_04_15,Q21_DaysofWeekHrs_04_16,Q21_DaysofWeekHrs_04_17,Q21_DaysofWeekHrs_04_18,Q21_DaysofWeekHrs_04_19,Q21_DaysofWeekHrs_04_20,Q21_DaysofWeekHrs_04_21,Q21_DaysofWeekHrs_04_22,Q21_DaysofWeekHrs_04_23,Q21_DaysofWeekHrs_04_24,Q21_DaysofWeekHrs_04_25,Q21_DaysofWeekHrs_04_26,Q21_DaysofWeekHrs_05_01,Q21_DaysofWeekHrs_05_02,Q21_DaysofWeekHrs_05_03,Q21_DaysofWeekHrs_05_04,Q21_DaysofWeekHrs_05_05,Q21_DaysofWeekHrs_05_06,Q21_DaysofWeekHrs_05_07,Q21_DaysofWeekHrs_05_08,Q21_DaysofWeekHrs_05_09,Q21_DaysofWeekHrs_05_10,Q21_DaysofWeekHrs_05_11,Q21_DaysofWeekHrs_05_12,Q21_DaysofWeekHrs_05_13,Q21_DaysofWeekHrs_05_14,Q21_DaysofWeekHrs_05_15,Q21_DaysofWeekHrs_05_16,Q21_DaysofWeekHrs_05_17,Q21_DaysofWeekHrs_05_18,Q21_DaysofWeekHrs_05_19,Q21_DaysofWeekHrs_05_20,Q21_DaysofWeekHrs_05_21,Q21_DaysofWeekHrs_05_22,Q21_DaysofWeekHrs_05_23,Q21_DaysofWeekHrs_05_24,Q21_DaysofWeekHrs_05_25,Q21_DaysofWeekHrs_05_26,Q21_DaysofWeekHrs_06_01,Q21_DaysofWeekHrs_06_02,Q21_DaysofWeekHrs_06_03,Q21_DaysofWeekHrs_06_04,Q21_DaysofWeekHrs_06_05,Q21_DaysofWeekHrs_06_06,Q21_DaysofWeekHrs_06_07,Q21_DaysofWeekHrs_06_08,Q21_DaysofWeekHrs_06_09,Q21_DaysofWeekHrs_06_10,Q21_DaysofWeekHrs_06_11,Q21_DaysofWeekHrs_06_12,Q21_DaysofWeekHrs_06_13,Q21_DaysofWeekHrs_06_14,Q21_DaysofWeekHrs_06_15,Q21_DaysofWeekHrs_06_16,Q21_DaysofWeekHrs_06_17,Q21_DaysofWeekHrs_06_18,Q21_DaysofWeekHrs_06_19,Q21_DaysofWeekHrs_06_20,Q21_DaysofWeekHrs_06_21,Q21_DaysofWeekHrs_06_22,Q21_DaysofWeekHrs_06_23,Q21_DaysofWeekHrs_06_24,Q21_DaysofWeekHrs_06_25,Q21_DaysofWeekHrs_06_26,Q21_DaysofWeekHrs_07_01,Q21_DaysofWeekHrs_07_02,Q21_DaysofWeekHrs_07_03,Q21_DaysofWeekHrs_07_04,Q21_DaysofWeekHrs_07_05,Q21_DaysofWeekHrs_07_06,Q21_DaysofWeekHrs_07_07,Q21_DaysofWeekHrs_07_08,Q21_DaysofWeekHrs_07_09,Q21_DaysofWeekHrs_07_10,Q21_DaysofWeekHrs_07_11,Q21_DaysofWeekHrs_07_12,Q21_DaysofWeekHrs_07_13,Q21_DaysofWeekHrs_07_14,Q21_DaysofWeekHrs_07_15,Q21_DaysofWeekHrs_07_16,Q21_DaysofWeekHrs_07_17,Q21_DaysofWeekHrs_07_18,Q21_DaysofWeekHrs_07_19,Q21_DaysofWeekHrs_07_20,Q21_DaysofWeekHrs_07_21,Q21_DaysofWeekHrs_07_22,Q21_DaysofWeekHrs_07_23,Q21_DaysofWeekHrs_07_24,Q21_DaysofWeekHrs_07_25,Q21_DaysofWeekHrs_07_26"]

def getVer(LableRow):
    for row in csv.reader(ver1line, delimiter=','):
        if LableRow == row:
            return 1
    return -1

def getSQLIndex(version, csvIndex, rowtext):
    lookupname = ""
    lookupcat = ""
    csvIndex += 1 #zero indexing
    if version != 1:
        print("BAD FILE VERSION: The header line for the csv being imported is unrecognized.")
        return -1
    if csvIndex <= 14:
        return 0 #skip
    if csvIndex == 15:
        return 1 #user name
    elif csvIndex == 16:
        return 2 #resource name
    elif csvIndex == 17:
        return 3 #comments
    elif csvIndex == 18:
        return 4 #desc of resource services
    elif csvIndex == 19:
        return 5 # resources, service or both
    elif csvIndex == 20 or csvIndex == 21 or csvIndex == 22:
        return 6 #distress
    elif csvIndex == 32:
        lookupname = "General Public / All"
        lookupcat = "User Group"
    elif csvIndex == 35:
        lookupname = "Male"
        lookupcat = "Gender/Orientation Group"
    elif csvIndex == 40 or csvIndex == 41:
        return 0
    elif csvIndex == 42:
        lookupname = "English"
        lookupcat = "Language"
    elif csvIndex == 43:
        lookupname = "French"
        lookupcat = "Language"
    elif csvIndex == 44:
        lookupname = "Panjabi (Punjabi)"
        lookupcat = "Language"
    elif csvIndex == 45:
        lookupname = "Spanish"
        lookupcat = "Language"
    elif csvIndex == 46:
        lookupname = "Italian"
        lookupcat = "Language"
    elif csvIndex == 47:
        lookupname = "German"
        lookupcat = "Language"
    elif csvIndex == 50:
        lookupname = "Arabic"
        lookupcat = "Language"
    elif csvIndex == 52:
        lookupname = "Portuguese"
        lookupcat = "Language"
    elif csvIndex == 71 or csvIndex == 72:
        return 0 #skip other
    elif csvIndex == 73:
        lookupname = "Peer-Support"
        lookupcat = "Resource Category"
    elif csvIndex == 74:
        lookupname = "Crisis Support/Distress Counselling"
        lookupcat = "Resource Category"
    elif csvIndex == 75:
        lookupname = "Online Course/Webinar"
        lookupcat = "Resource Category"
    elif csvIndex == 76:
        lookupname = "Informational (text, document, and/or video for information only)"
        lookupcat = "Resource Category"
    elif csvIndex == 79:
        lookupname = "All ages"
        lookupcat = "Age Group"
    elif csvIndex == 84:
        lookupname = "Child/Youth (0-13 years)"
        lookupcat = "Age Group"
    elif csvIndex == 85:
        lookupname = "Adolescents/Teens (13-17 years)"
        lookupcat = "Age Group"
    elif csvIndex == 86:
        lookupname = "Transitional age (16-24 years)"
        lookupcat = "Age Group"
    elif csvIndex == 87:
        lookupname = "Adult (18+)"
        lookupcat = "Age Group"
    elif csvIndex == 88:
        lookupname = "Older Adult (55+)"
        lookupcat = "Age Group"
    elif csvIndex == 89 or csvIndex == 90:
        return 0
    elif csvIndex == 91:
        lookupname = "All Canada"
        lookupcat = "Locations"
    elif csvIndex == 92:
        lookupname = "Alberta Wide"
        lookupcat = "Locations"
    elif csvIndex == 96 or csvIndex == 97:
        return 0
    elif csvIndex == 189:
        lookupname = "Anxiety"
        lookupcat = "Health Issue Group"
    elif csvIndex == 190:
        lookupname = "Depression"
        lookupcat = "Health Issue Group"
    elif csvIndex == 191:
        lookupname = "General well-being"
        lookupcat = "Health Issue Group"
    elif csvIndex == 192:
        lookupname = "Substance use"
        lookupcat = "Health Issue Group"
    elif csvIndex == 195:
        lookupname = "Addictions (including Drugs, Alcohol and Gambling)"
        lookupcat = "Health Issue Group"
    elif csvIndex == 197:
        lookupname = "Anorexia"
        lookupcat = "Health Issue Group"
    elif csvIndex == 201:
        lookupname = "Attention Deficit Disorders (ADD/ADHD)"
        lookupcat = "Health Issue Group"
    elif csvIndex == 203:
        lookupname = "Autism and Autism Spectrum Disorders"
        lookupcat = "Health Issue Group"
    elif csvIndex == 205:
        lookupname = "Bipolar Disorders"
        lookupcat = "Health Issue Group"
    elif csvIndex == 207:
        lookupname = "Bulimia"
        lookupcat = "Health Issue Group"
    elif csvIndex == 211:
        lookupname = "Delirium"
        lookupcat = "Health Issue Group"
    elif csvIndex == 212:
        lookupname = "Dementia including Alzheimer''s"
        lookupcat = "Health Issue Group"
    elif csvIndex == 215:
        lookupname = "Personality disorders"
        lookupcat = "Health Issue Group" 
    elif csvIndex == 218:
        lookupname = "Eating Disorders including Anorexia and Bulimia"
        lookupcat = "Health Issue Group" 
    elif csvIndex == 224:
        lookupname = "Grief and Bereavement"
        lookupcat = "Health Issue Group"
    elif csvIndex == 225:
        lookupname = "Hoarding"
        lookupcat = "Health Issue Group"
    elif csvIndex == 227:
        lookupname = "Insomnia"
        lookupcat = "Health Issue Group"
    elif csvIndex == 228:
        lookupname = "Learning Disorders"
        lookupcat = "Health Issue Group"
    elif csvIndex == 229:
        lookupname = "Medication Treatment"
        lookupcat = "Health Issue Group"
    elif csvIndex == 230:
        lookupname = "Mental Health in General"
        lookupcat = "Health Issue Group"
    elif csvIndex == 231:
        lookupname = "Mood Disorders"
        lookupcat = "Health Issue Group"
    elif csvIndex == 232:
        lookupname = "Obsessive Compulsive Disorder (OCD)"
        lookupcat = "Health Issue Group"
    elif csvIndex == 239:
        lookupname = "Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse"
        lookupcat = "Health Issue Group"
    elif csvIndex == 241:
        lookupname = "Schizophrenia and Psychosis"
        lookupcat = "Health Issue Group"
    elif csvIndex == 243:
        lookupname = "Self-harm including Self-cutting"
        lookupcat = "Health Issue Group"
    elif csvIndex == 250:
        lookupname = "Stress"
        lookupcat = "Health Issue Group"
    elif csvIndex == 251:
        lookupname = "Suicidal Ideation"
        lookupcat = "Health Issue Group"
    elif csvIndex == 254 or csvIndex == 255:
        return 0
    elif csvIndex == 256:
        lookupname = "Website"
        lookupcat = "Resource Format"
    elif csvIndex == 257:
        lookupname = "Phone Number"
        lookupcat = "Resource Format"
    elif csvIndex == 258:
        lookupname = "Online chat"
        lookupcat = "Resource Format"
    elif csvIndex == 259:
        lookupname = "Email"
        lookupcat = "Resource Format"
    elif csvIndex == 260:
        lookupname = "Online course"
        lookupcat = "Resource Format"
    elif csvIndex == 261:
        lookupname = "Definition/Stat"
        lookupcat = "Resource Format"
    elif csvIndex == 264:
        lookupname = "Physical Address"
        lookupcat = "Resource Format"
    elif csvIndex == 265:
        lookupname = "Text Messaging"
        lookupcat = "Resource Format"
    elif csvIndex == 268:
        return 8 #general URL
    elif csvIndex == 269:
        return 9 #specific URL
    elif csvIndex == 270:
        return 12 #phone number
    elif csvIndex == 271:
        return 13 #txt number
    elif csvIndex == 272:
        return 14 #email
    elif csvIndex == 273:
        return 15 #address
    elif csvIndex == 274:
        return 10 #Definition/stat Text
    elif csvIndex == 275:
        return 11 #refrence Text
    elif csvIndex == 276:
        lookupname = "24/7"
        lookupcat = "Dates and Times"
    elif csvIndex > 276:
        print("time tag, skip for now")
        return 0
    else:
        print("UNHANDLED TAG: Import index '" + str(csvIndex) + "' is unhandled. Please add the missing logic then run the importer again.")
        return -1

    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin@123",
        database="main_db"
    )

    sql = "SELECT id FROM resource_tag WHERE tag_category = '" + lookupcat + "' AND name = '" + lookupname +"';"
    mycursor = mydb.cursor()
    mycursor.execute(sql, multi=True)

    for id in mycursor:
        #1-15 are resource fields
        #16-999 are tags(so subtract 15 to get actual tag id in database)
        return id[0]+15
    
    print("DB TAG MISSING: csv column '" +lookupcat+"/"+lookupname+ "' recognized, but couldn't find the tag in the database. Has the tag creator script been run?")
    return -1