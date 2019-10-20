import sys
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import re
from os import path
import getpass
import smtplib
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from email.mime.multipart import MIMEMultipart 

def Create_Log_File():
	Full_File_Name= os.path.basename(sys.argv[0])
	#print(Full_File_Name)
	File_Name=Full_File_Name.split('.')[0]
	Log_File=File_Name+".log"
	#print(Log_File)
	try:
		if(os.path.exists(Log_File)):
			#print("File Exist")
			os.remove(Log_File)
		else:
			print("File doesn't exist")
		lf=open(Log_File,"a")
		return lf
	except :
		print('Error occurred while opening file Log_File',Log_File,sys.exc_info()[0])
	
def Browse_URL(url,lf):
	" This function will open browser and will open given url.Return will be browser element "
	try:
		lf.write("Inside Browse_URL Function\n")
		# webdriver path set 
		browser = webdriver.Chrome("chromedriver.exe") 
		# To maximize the browser window 
		browser.maximize_window()
		# Open URL
		browser.get(url) 
		time.sleep(5)
		lf.write("Exiting from Browse_URL Function\n")
		return browser
	except:
		k=sys.exc_info()[0]
		lf.write(k)
		lf.write("\n")
		print("ERROR Check Log File")
		lf.write("Error occurred while getting the price of share ")
		lf.write(Share_Name_Code)
		lf.write("\n")

def Price_By_Name_Code(browser,Share_Name_Code,lf):
	" This function will take share name or code as input and return price of that share"
	browser.refresh()
	a=browser.find_element_by_xpath("//input[@name='companyED']")
	a.send_keys(Share_Name_Code)
	time.sleep(3)
	a.click()
	a.send_keys(Keys.ENTER)
	time.sleep(3)
	try:
		Price=browser.find_element_by_xpath("//span[@id='lastPrice']").text
		share_Price=Price
		return share_Price
	except:
		print('Error occurred while getting the price of ',Share_Name_Code,' ',sys.exc_info()[0])
		k=sys.exc_info()[0]
		lf.write(k)
		lf.write("\n")
		print("ERROR Check Log File")
		ltr="Error occurred while getting the price of share "+Share_Name_Code+"\n"
		lf.write(ltr)
		browser.refresh()
		Price="NAV"
		share_Price=Price
		return share_Price
		
def Share_Price_Alert_Low(dict,lf):
	lf.write("************** Inside Share_Price_Alert_Low Function *********************\n")
	Dict_Price_Alert_Low={}
	
	if( os.path.exists("Share_Lower_Price.txt")):
		lf.write("Share_Lower_Price.txt file is present\n")
		#print("File Exist")
	else:
		lf.write("Error :- Share_Lower_Price.txt file does not  present\n")
		sys.exit()
		
	lf.write("Prepare body part for Share_Lower_Price.txt BUY share\n")
	fsl=open("Share_Lower_Price.txt","r")
	print("Alert to Buy the Share")
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
		print("Error: While comparing Alert Price",sys.exc_info()[0])
		ltr=sys.exc_info()[0]+' '+"Error Occurred while comparing alert price with share price"+"\n"
		lf.write(ltr)
		lf.write("*****************************************************************************************\n")
		#sys.exit()
	fsl.close()

	Dict_Price_Alert_High={}
	if( os.path.exists("Share_Higher_Price.txt")):
		lf.write("Share_Higher_Price.txt file is present\n")
		#print("File Exist")
	else:
		lf.write("Error :- Share_Higher_Price.txt file does not  present\n")
		#sys.exit()

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
		print("Error: While comparing Alert Price",sys.exc_info()[0])
		ltr=sys.exc_info()[0]+' '+"Error Occurred while comparing alert price with share price High"+"\n"
		lf.write(ltr)
		lf.write("*****************************************************************************************\n")
		#sys.exit()
	fsh.close()

	z=x+y+	'''</table>
				</body>
				</html>
			'''
	print(z)
	ltr="Comparision is done email body message is prepared.\n"
	lf.write(ltr)
	lf.write("Mail Body Part in HTML Format is :- \n")
	lf.write(z)
	lf.write("\n")
	lf.write("************************************************************************************\n")
	return z

	#Send_Email(x)
	#print(Dict_Price_Alert_Low)
	#print(Dict_Price_Alert_Low.keys())
	#print(Dict_Price_Alert_Low.values())

def Send_Email(z,lf):
	lf.write("********************** Inside Send_Email function ****************************\n")
	#email = 'abhilash.kumar@lntinfotech.com'
	email = 'abhi.cvraman@gmail.com'
	#password = input("Enter the password : ")
	password=getpass.getpass("Enter your password: ")	# Here password will not be visible
	#send_to_email = 'abhilash.kumar@lntinfotech.com'
	send_to_email = ['abhi.k.cvraman@gmail.com','ashish.nitjsrcse@gmail.com','abhi.cvraman@gmail.com']
	subject = 'ALERT Raised'
	#messagePlain = z
	messageHTML=z
	msg = MIMEMultipart('alternative')
	msg['From'] = email
	#msg['To'] = send_to_email
	msg['To'] = ",".join(send_to_email) 	# For more that one recipient
	msg['Subject'] = subject
	try:
		# Attach both plain and HTML versions
		#msg.attach(MIMEText(messagePlain, 'plain'))
		msg.attach(MIMEText(messageHTML, 'html'))

		#server = smtplib.SMTP(host='smtp.office365.com', port=587)
		server = smtplib.SMTP(host='smtp.gmail.com', port=587)
		server.ehlo()
		server.starttls()
		server.login(email, password)
		text = msg.as_string()
		server.sendmail(email, send_to_email, text)
		print("Successfully sent email")
		lf.write("Email Successfully send\n")
		server.quit()
	except:
		print("Error: unable to send email",sys.exc_info()[0])
		ltr="Error: unable to send email"+"\n"
		lf.write(sys.exc_info()[0])
		lf.write(ltr)
		sys.exit()

def main():
	Dict_Share_Price = {}
	lf=Create_Log_File()
	lf.write("Calling Browse_URL Function\n")
	browser=Browse_URL('https://www.nseindia.com',lf)
	try:
		if( os.path.exists("Share_Price.txt")):
			#print("File Exist")
			os.remove("Share_Price.txt")
		else:
			print("File doesn't exist")
		fh=open("List_Of_Share.txt","r")
		fo=open("Share_Price.txt","a")
		lf.write("File List_Of_Share.txt & Share_Price.txt opened\n")
	except :
		print('Error occurred while opening file List_Of_Share.txt/Share_Price.txt',sys.exc_info()[0])
		lf.write(sys.exc_info()[0])
		lf.write("Error occurred while opening file List_Of_Share.txt/Share_Price.txt\n")
	else:
		# START :- Take share name from List_Of_Share.txt file and search and write data into "Share_Price.txt" File
		lf.write("************************************************************\n")
		ltr="Taking share name from List_Of_Share.txt file and passing this name to function Price_By_Name_Code\n"
		lf.write(ltr)
		for line in fh.readlines():
			Share_Name_Code=line.split('@')[0]
			Share_Code1=line.split('@')[1]
			Share_Code=re.sub('\n','', Share_Code1) #Remove \n from the line
			#print(Share_Name_Code)
			lf.write(Share_Name_Code)
			lf.write(" :- \n")
			ltr="Calling Price_By_Name_Code function for getting the price of share "+Share_Name_Code+"\n"
			lf.write(ltr)
			share_Price=Price_By_Name_Code(browser,Share_Name_Code,lf)
			str=re.sub(',','', share_Price) # Remove Comma(,) from the line
			str1=str+'    '+line	# Add share name and code to the share price string
			fo.write(str1)	# No need to write "\n" bcz line itself contains an ENTER
			Dict_Share_Price[Share_Code]=str
			ltr="price of share "+Share_Name_Code +" is "+share_Price+"\n"
			lf.write(ltr)
		lf.write("**************************************************************************************\n")
		ltr="Share price data kept in Share_Price.txt file and also stored in Dict_Share_Price dictionary\n"
		lf.write(ltr)
		lf.write("**************************************************************************************\n")
		ltr="Dictionary data is \n"
		lf.write(ltr)
		#lf.write(str(Dict_Share_Price))	# Not Working
		lf.write("\n")
		#print(Dict_Share_Price)
		browser.close()

	lf.write("**************************************************************************************\n")
	ltr="Calling Share_Price_Alert_Low Function which will return mail body part which will passed as parameter to Send_Email function \n"
	lf.write(ltr)
	z=Share_Price_Alert_Low(Dict_Share_Price,lf)
	ltr="Calling Send_Email function for sending mail\n"
	Send_Email(z,lf)
	# END
	lf.write("************************COMPLETED************************")
	fh.close()
	fo.close()
	lf.close()

if __name__ == "__main__": main()
