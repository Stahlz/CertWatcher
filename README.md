**CertWatcher** is a new take on monitoring for Phishing Sites via CertStream. 
This differs from other on github in that it is more based towards the enterprise, and automation. 
It is meant to be a set and forget project, so that once configured correctly you can just be alerted on a daily basis, with potential Phishing sites affecting your organization. 


**Prerequisites**

Please install these required packages.

To send email with Gmail,Yahoo,Live you will have to enable this, you must be logged in:
* [Gmail](https://myaccount.google.com/lesssecureapps)
* [Yahoo](https://help.yahoo.com/kb/SLN27791.html)
* [Live](https://answers.microsoft.com/en-us/msoffice/forum/msoffice_outlook-mso_win10-mso_365hp/outlook-security/e92fbfb5-504e-4709-85ce-4996c5a6f14a?auth=1)

**Python3**
```
sudo pip install argparse entropy datetime certstream configparser
```

**Configuration Example**

**Edit: config.txt**

Separate everything with a comma.
```
[certstreamerz]
#Fill in with keywords for your companies websites.
keywords=wellsfargo,paypal,login,sign-in,secure,update,money,sslsecure,amazon
#You can add or take away from this TLD list.
tlds=.ga,.gq,.ml,.cf,.tk,.xyz,.pw,.cc,.club,.work,.top,.support,.bank,.info,.study,.party,.click,.country,.stream,.gdn,.mom,.xin,.kim,.men,.loan,.download,.racing,.online,.ren,.gb,.win,.review,.vip,.party,.tech,.science
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
2) To send you an email every 24 hours with a list of Phishing sites to check out.

It's currently set for every 24 hours, in future versions i will add the ability to set the alerting delay.

```shell
cd /opt/
git clone https://github.com/gunnerstahl/CertWatcher.git
cd CertWatcher
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

**Tested With**
* [Kali](https://www.kali.org/)
* [Ubuntu](https://www.ubuntu.com/)

It should work on any linux os that can install Python/Cron

**Future Updates**

1) I will add a database function to store Phishing sites and then alert on them when they are accessible.
2) I will add the ability to auto change the alerting interval.

**Author**

* **Joshua Whitaker** 
* *Twitter* [@_Stahlz](https://twitter.com/_Stahlz)
* *Email* - [stahl@stahl.io](stahl@stahl.io)

**Acknowledgments**

* [x0rz](https://twitter.com/x0rz/) - I borrowed code from an earlier version of [phishing_catcher](https://github.com/x0rz/phishing_catcher)
* [6IX7ine](https://twitter.com/6IX7ine) - I used the text coloring from [ShodanWave](https://github.com/6IX7ine/shodanwave)


