import requests
import datetime
import smtplib
import ssl

#Email ID details


port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = input("Enter sender email: ")
receiver_email = input("Enter receiver email: ")
password = input("Enter password for sender email ID: ")
context = ssl.create_default_context()
message = """From: Vaxx Bot
To: <>
Subject: COWIN

"""

#User Inputs


Pin_code = int(input("Enter Pin Code: "))
age = int(input("Enter age: "))  # 20
numofdays = 6
details = ""
chat = ""
date = datetime.date.today().strftime("%d-%m-%y")


#Fetch Data


URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
    Pin_code, date)
response = requests.get(URL)

if response.ok:
    json = response.json()
    if json["centers"]:
        for center in json["centers"]:
           
            details = ("\n\nCenter name: " + str(center['name']))

            details = details + ("\nPrice: " + str(center['fee_type']))

            details = details + ("\nAvailable capacity: " +
                                 str(center['sessions'][0]['available_capacity']))

            if(center['sessions'][0]["vaccine"] != ''):

                details = details + ("\nVaccine: " + str(center['sessions'][0]['vaccine']))
            details = details + ("\nAvailable on: ")

            if(center['sessions'][0]['available_capacity'] < 1):
               details = ""
            for session in center["sessions"]:
                if (session["min_age_limit"] <= age) and (session['available_capacity'] > 0):

                    details = details + ("\n\t " + str(session['date']))

            chat = chat+details+"\n"
            details = ""


         #Send Email


        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message+chat)
            print("Email Sent !")

else:
    print("No available slots on {}".format(date))

