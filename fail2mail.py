#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText
from datetime import date
from email.mime.multipart import MIMEMultipart
import re
import commands

jails = commands.getoutput('fail2ban-client status | grep "Jail list:"')
list = re.split(', ', jails)
list[0] = re.sub('`- Jail list:\t\t', '' , list[0])
listlen = len(list)
i = 0
mail = open('/tmp/mail.html', 'w+')
text = ''

while(i < listlen):
	fail = 'fail2ban-client status ' + list[i]
	text += commands.getoutput(fail) + '\n'
	i += 1

try:
	mail.write(''.join(text))
	mail.write('\n')
except: pass
finally:
	mail.close()

# to html format
html = """\
		<html>
		<head>
		</head>
		<body>
		"""
i = 0
try: 
	mail = open('/tmp/mail.html', 'r')
except: pass

mail = mail.readlines()
listlen = len(mail)

while i < listlen:
	mail[i] = re.sub('\|', '', mail[i])
	mail[i] = re.sub('-', '', mail[i])
	mail[i] = re.sub('`', '', mail[i]) 
	
	if re.search('Status ', mail[i]):
		html += '<h2>' + mail[i] + '</h2>'
		i += 1
	elif re.search('action', mail[i]):
		html += '<h4>' + mail[i] + '</h4>'
		i += 1
	elif re.search('filter', mail[i]):
		html += '<h4>' + mail[i] + '</h4>'
		i += 1
	else:
		html += '<br>' + mail[i]
		i += 1 

html += """\
		</body>
		</html>
		"""
# Mail Part
mailfrom = 'foo@bar.com'
rcptto = 'foo@bar.com'
msg = MIMEMultipart('alternative')
msg['Subject'] = ('Fail2Ban Statistics for ' + str(date.today()) + '')
msg['From'] = mailfrom
msg['To'] = rcptto

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')
msg.attach(part1)
msg.attach(part2)

mailserver = smtplib.SMTP('localhost')
mailserver.sendmail(mailfrom, rcptto, msg.as_string())
mailserver.quit()

