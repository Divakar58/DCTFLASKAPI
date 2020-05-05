from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Attachment,FileContent,FileName,FileType,Disposition
import os
import pandas as pd
from dotenv import load_dotenv
import base64


load_dotenv()

df=pd.DataFrame({'a':[1,2,3,4,5],'b':[9,8,7,6,5],'c':[6,4,5,6,7]})
df.to_csv('data.csv')
message=Mail(
    from_email='divakarkareddy@gmail.com',
    to_emails='divakar.kareddy@duckcreek.com',#divakar.kareddy@duckcreek.com
    subject='Recommendations Mail',
    html_content='Please {name}, find the attached recommendation in excel',
    
)
with open('data.csv', 'rb') as f:
    data = f.read()
    f.close()
encoded_file = base64.b64encode(data).decode()

attachedFile = Attachment(
    FileContent(encoded_file),
    FileName('data.csv'),
    FileType('application/csv'),
    Disposition('attachment')
)
message.attachment = attachedFile

sendgrid=SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

res=sendgrid.send(message)

print(res.status_code,res.headers)
if res.status_code=='200':
    print("Mail send")
