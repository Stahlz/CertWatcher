import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import configparser
import datetime
from misc import redundant

initmisc = redundant()
today = initmisc.get_date()
get_pwd = initmisc.get_pwd()

yesterdays_date = today - datetime.timedelta(1)
yesterdays_date = yesterdays_date.strftime('%b-%d-%Y')

configfilepath = '{0}/config.txt'.format(get_pwd)
config = configparser.ConfigParser()
config.read(configfilepath)

url_list = []
read_file_name = '{0}/output/'.format(get_pwd) + yesterdays_date +'_CertStream' + '.log'

try:
    with open(read_file_name, 'r') as spliter:
        output = spliter.read()
        url_list.append(output)
    splitted = ''.join(url_list)
    del url_list
except:
    print('[-] Problem with opening file: {0}'.format(write_file_name))

from_email = config.get('email','from_email')
to_email = config.get('email','to_email')
email_user = config.get('email','email_username')
email_pass = config.get('email','email_password')
smtp_server = config.get('email', 'server')
smtp_port = config.get('email', 'port')

fromaddr = '{0}'.format(from_email)
toaddr = '{0}'.format(to_email)

msg = MIMEMultipart()

msg['from'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'CertStream Report for {0}'.format(yesterdays_date)

body = ('Please check on these possible Phishing Domains:' + '\n'
        '{0}'.format(splitted)
        )
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('{0}'.format(smtp_server), '{0}'.format(smtp_port))
server.starttls()
server.login(email_user, email_pass)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
