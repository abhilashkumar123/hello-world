import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import sys
import re
import getpass
import os

def Share_Price_Alert_Low(dict):
	Dict_Price_Alert_Low={}
	fsl=open("Share_Lower_Price.txt","r")
	print("*****Alert to Buy the Share*****")
	print("Share Name",'    ',"Current_Price",'    ',"Alert_Price")

	x=	'''<!DOCTYPE html>
			<html>
			<head>
			<style>
			table, th, td 
			{
			  border: 1px solid black;
			  border-collapse: collapse;
			}
			</style>
			</head>
			<body>
			<h2>Alert to Buy Share</h2>
			<table style="width:100%">
		  <tr>
			<th>Share Name</th>
			<th>Current Price</th> 
			<th>Alert Price</th>
		  </tr>
		'''
	try:
		for line in fsl:
			share_name=line.split('@')[0]
			#print(share_name)
			share_alert_price1=line.split('@')[1]
			share_alert_price=re.sub('\n','', share_alert_price1) #Remove \n from the line
			#print(share_alert_price)
			Dict_Price_Alert_Low[share_name]=share_alert_price
			if (Dict_Price_Alert_Low[share_name] > dict[share_name]):
				print(share_name.ljust(10),'    ',dict[share_name].ljust(13),'    ',Dict_Price_Alert_Low[share_name])
				#x=x+share_name.ljust(14)+'    '+dict[share_name].ljust(14)+'    '+Dict_Price_Alert_Low[share_name]+"\n"
				x=x+'''<tr>
						<td>'''+share_name+'''</td>
						<td>'''+dict[share_name]+'''</td>
						<td>'''+Dict_Price_Alert_Low[share_name]+'''</td>
						</tr>
					'''
		x=x+'''</table>
				</body>
				</html>
			'''
		#print(x)
		#return x
	except:
		print('Error',sys.exc_info()[0])
	fsl.close()

	Dict_Price_Alert_High={}
	if( os.path.exists("Share_Higher_Price.txt")):
		#lf.write("Share_Higher_Price.txt file is present\n")
		print("File Exist")
	else:
		#lf.write("Error :- Share_Higher_Price.txt file does not  present\n")
		sys.exit()
    
	fsh=open("Share_Higher_Price.txt","r")
	y=	'''<style>
			table, th, td 
			{
			  border: 1px solid black;
			  border-collapse: collapse;
			}
			</style>
			</head>
			<body>
			<h2>Alert to Sell Share</h2>
			<table style="width:100%">
		  <tr>
			<th>Share Name</th>
			<th>Current Price</th> 
			<th>Alert Price</th>
		  </tr>
		'''
	try:
		for line in fsh:
			share_name=line.split('@')[0]
			#print(share_name)
			share_alert_price1=line.split('@')[1]
			share_alert_price=re.sub('\n','', share_alert_price1) #Remove \n from the line
			#print(share_alert_price)
			Dict_Price_Alert_High[share_name]=share_alert_price
			if (Dict_Price_Alert_High[share_name] < dict[share_name]):
				#print(share_name.ljust(10),'    ',dict[share_name].ljust(13),'    ',Dict_Price_Alert_High[share_name])
				#y=y+share_name.ljust(14)+'    '+dict[share_name].ljust(14)+'    '+Dict_Price_Alert_High[share_name]+"\n"
				y=y+'''<tr>
						<td>'''+share_name+'''</td>
						<td>'''+dict[share_name]+'''</td>
						<td>'''+Dict_Price_Alert_High[share_name]+'''</td>
						</tr>
					'''
		#print(y)
	except:
		print('Error')
	fsh.close()

	z=x+y+	'''</table>
				</body>
				</html>
			'''
	print(z)
	return z

def Send_Email(x):
	email = 'abhilash.kumar@lntinfotech.com'
	#password = input("Enter the password : ")
	password=getpass.getpass("Enter your password: ")	# Here password will not be visible
	send_to_email = 'abhilash.kumar@lntinfotech.com'
	subject = 'ALERT Raised'
	#messagePlain = x
	messageHTML=x
	msg = MIMEMultipart('alternative')
	msg['From'] = email
	msg['To'] = send_to_email
	msg['Subject'] = subject
	try:
		# Attach both plain and HTML versions
		#msg.attach(MIMEText(messagePlain, 'plain'))
		msg.attach(MIMEText(messageHTML, 'html'))

		server = smtplib.SMTP(host='smtp.office365.com', port=587)
		server.starttls()
		server.login(email, password)
		text = msg.as_string()
		server.sendmail(email, send_to_email, text)
		print("Successfully sent email")
		server.quit()
	except:
		print("Error: unable to send email",sys.exc_info()[0])

def main():
	dict={'ICICIBANK': '410.90', 'LT': '1394.80', 'AXISBANK': '681.00', 'PVR': '1467.00', 'INFY': '777.40', 'YESBANK': '84.75', 'PNB': '68.15', 'SBIN': '303.10'}
	x=Share_Price_Alert_Low(dict)
	#print(dict)
	Send_Email(x)
if __name__ == "__main__": main()

