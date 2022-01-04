import os,datetime
import sendgrid
import codecs
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import mysql.connector

# The table "to_ from twilio_from_and_to_emails" contains 5 columns (to_, name, domain, Updated, updated_date)
# query2 retrieves the emails where Updated column is marked as 'No'. We can change the query as per need.

from_='sitakanta@retainiq.io'   #address of the sender
query2="select to_,domain from twilio_from_and_to_emails where Updated='No'"   #selecting all the emails who have from_ as their sender in the db.
db = mysql.connector.connect(user='admin', password='ZeroPointZero', host='crawl.cvfknof9hjcx.us-east-1.rds.amazonaws.com',database='crawl')
cursor = db.cursor()
cursor.execute(query2)
result2=cursor.fetchall()
cursor.close()
today=datetime.date.today()
today=str(today.strftime("%Y-%m-%d"))
mails=[]
mails_later=[]
sub="TRYING EMAIL TWILIO"
TEMPLATE_ID ='d-b3223e72728145d6bdaee6d0a9f44946'   #template ID as available on sendgrid

    
sub="TEST EMAIL WITH TEMPLATE_ID"       #subject of the mail.
to_emails_=[]

try:
    for mail_ in result2:
        to_emails_=[]
        store=mail_[1]
        email_id=mail_[0]
        #print(store)
        to_email_temp=To(email=email_id,
                         dynamic_template_data={
                             'store_name': store,
                             }
                         )
        to_emails_.append(to_email_temp)
        temp=(
            today,
            email_id,
            )
        mails_later.append(temp)
        message = Mail(
            from_email=from_,
            to_emails=to_emails_,
            subject=sub,
            )
        message.template_id = TEMPLATE_ID
        sg = SendGridAPIClient('########')
        response = sg.send(message)
        print(response.status_code)
except Exception as e:
    print(e)
    exit()
query3="update twilio_from_and_to_emails set Updated='Yes', updated_date = %s where to_ = %s"
cursor = db.cursor()
cursor.executemany(query3,mails_later)
db.commit()
cursor.close()

