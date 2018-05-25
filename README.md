![alt text](https://i.imgur.com/lPjJ5Mj.png)

**CertWatcher** is a new take on monitoring for Phishing Sites via CertStream. 
This differs from other on github in that it is more based towards the enterprise, and automation. 
It is meant to be a set and forget project, so that once configured correctly you can just be alerted on a daily basis, with potential Phishing sites affecting your organization. 


**Prerequisites**

Please install these required packages.

**Python3**
```
pip3 install certstream configparser subprocess argparse entropy datetime smtplib
```
To send email with Gmail,Yahoo,Live you will have to enable this, you must be logged in:
[Gmail](https://myaccount.google.com/lesssecureapps)
[Yahoo](https://help.yahoo.com/kb/SLN27791.html)
[Live](https://answers.microsoft.com/en-us/msoffice/forum/msoffice_outlook-mso_win10-mso_365hp/outlook-security/e92fbfb5-504e-4709-85ce-4996c5a6f14a?auth=1)

**Configuration Example**

Edit: config.txt

Separate everything with a comma.
```
[certstreamerz]
#Fill in with keywords for your companies websites.
keywords=google,facebook,paypal,paypol,.paypal,paypal.,-facebook,-facebook-,.google,.google-
#You can add or take away from this TLD list.
tlds=.ga,.gq,.ml,.cf,.tk,.xyz,.pw,.cc,.club,.work,.top,.support,.bank,.info,.study,.party,.click,.country,.stream,.gdn,.mom,.xin,.kim,.men,.loan,.download,.racing,.online,.ren,.gb,.win,.review,.vip,.party,.tech,.science
#This example will send you a report every 12 hours, 0 will be every 24. Thats is the only exception, change to whatever you would like.
email_report_interval=12
```
```
[email]
from_email=myaccount@example.com
to_email=example@example.com
email_username=myaccount@example.com
email_password=examplepassword123
#example: smtp.gmail.com, smtp.live.com, smtp.mail.yahoo.com
server=thesmtpserver
#gmail port:587, live port:25, yahoo port:587 
port=587
```
**Note - Regarding updating email interval after initial install**
```
When changing the Email interval in the config file, you will have to:
python certwatcher.py -c uninstall
then
python certwatcher.py -c install
This will not require you to stop/start agent agian
```
**Menu**
```
usage: certwatcher.py [-h] [-c {start,stop,restart,install,uninstall}]

optional arguments:
  -h, --help            show this help message and exit
  -c {start,stop,restart,install,uninstall}, --certstream {start,stop,restart,install,uninstall}
                        Please Select one
```
**Installation**

This makes two cron entries:
1) To restart the script every 24 Hours.
2) To send you an email on your hourly interval with a list of Phishing sites to check out.

```shell
git clone https://github.com/gunnerstahl/CertWatcher
python certwatcher.py -c install
```

**How to run**

```shell
python certwatcher.py -c start
```

**Uninstall**

```shell
python certwatcher.py -c uninstall
```

**Future Updates**

1) I will add a database function to store Phishing sites and then alert on them when they are accessible. - In Process
2) I will add the ability to auto change the alerting interval. - Done
3) Adding a GUI for Monitoring, Control, and Reporting of Phishing sites. - In Process

**Author**

* **Joshua Whitaker** 
* *Twitter* [@_Stahlz](https://twitter.com/_Stahlz)
* *Email* - [stahl@stahl.io](stahl@stahl.io)
* *Website* - [stahl.io](http://stahl.io)

**Acknowledgments**

* [x0rz](https://twitter.com/x0rz/) - I borrowed code from an earlier version of [phishing_catcher](https://github.com/x0rz/phishing_catcher)
* [6IX7ine](https://twitter.com/6IX7ine) - I used the text coloring from [ShodanWave](https://github.com/6IX7ine/shodanwave)
* [drdeathatefnet](https://twitter.com/drdeathatefnet)- For the logo and presentation.


