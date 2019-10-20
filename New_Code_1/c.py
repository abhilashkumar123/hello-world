import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import sys

def main():

	email = 'abhi.cvraman@gmail.com'
	#password = input("Enter the password : ")
	password=getpass.getpass("Enter your password: ")	# Here password will not be visible
	#send_to_email = ['abhilash.kumar@lntinfotech.com','Vamsi.TS@lntinfotech.com']
	send_to_email = ['abhi.cvraman@gmail.com','abhi.k.cvraman@gmail.com']
	subject = 'Test Mail'
	##messageHTML='''<!DOCTYPE html>
	#				<html>
	#				<head>
	#				<style>
	#				table, th, td {
	#				  border: 1px solid black;
	#				  border-collapse: collapse;
	#				}
	#				</style>
	#				</head>
	#				<body>
	#			'''
	##messageHTML = messageHTML + '''
	#								<h2>Alert to Buy Share</h2>
    #
	#								<table style="width:100%">
	#								  <tr>
	#									<th>Share Name</th>
	#									<th>Current Price</th> 
	#									<th>Alert Price</th>
	#								  </tr>
	#								  <tr>
	#									<td>Jill</td>
	#									<td>Smith</td>
	#									<td>50</td>
	#								  </tr>
	#								  <tr>
	#									<td>Eve</td>
	#									<td>Jackson</td>
	#									<td>94</td>
	#								  </tr>
	#								  <tr>
	#									<td>John</td>
	#									<td>Doe</td>
	#									<td>80</td>
	#								  </tr>
	#								</table>
    #
	#								</body>
	#								</html>
	#							'''
	#messagePlain = 'Visit nitratine.net for some great tutorials and projects!'
	messagePlain = 'HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOO!'
	msg = MIMEMultipart('alternative')
	msg['From'] = email
	msg['To'] = ",".join(send_to_email) 
	msg['Subject'] = subject
	try:
		# Attach both plain and HTML versions
		msg.attach(MIMEText(messagePlain, 'plain'))
		#msg.attach(MIMEText(messageHTML, 'html'))

		#server = smtplib.SMTP(host='smtp.office365.com', port=587)
		server = smtplib.SMTP(host='smtp.gmail.com', port=587)
		server.ehlo()
		server.starttls()
		server.login(email, password)
		text = msg.as_string()
		server.sendmail(email, send_to_email, text)
		print("Successfully sent email")
		server.quit()
	except:
		print("Error: unable to send email",sys.exc_info()[0])

if __name__ == "__main__": main()
