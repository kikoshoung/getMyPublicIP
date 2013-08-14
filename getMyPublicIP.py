# this provide a way to get public ip address from tp-link  
import httplib, urllib, sys, re, base64, time  
  
if len(sys.argv) < 3:  
    print "useage: ", sys.argv[0], " username password"  
    quit()  
  
# wether show the error message.  
showErrorMessage = 0  
  
# 192.168.1.1  
conn = httplib.HTTPConnection("192.168.1.1")  
  
# set request headers  
headers = {"User-Agent": "python host",  
    "Content-type": "application/x-www-form-urlencoded",  
    "Authorization": "Basic %s" % base64.encodestring('%s:%s' % (sys.argv[1], sys.argv[2]))[:-1],  
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  
    "Accept-Language": "zh-cn,zh;q=0.5",  
    "Accept-Encoding": "gzip, deflate",  
    "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7",  
    "Connection": "keep-alive"}  
  
# get status page  
conn.request("GET", "/userRpm/StatusRpm.htm", "", headers)  
response = conn.getresponse()  
keyword = re.search(' wanPara [^\)]*?\)', response.read())  
response.close()  
conn.close()  
  
# search the public ip address  
found = 0  
publicIP = ""  
if keyword:  
    arr = re.findall('([\d]*?,)|(\"[^\"]*?\",)', keyword.group(0))  
    if arr:  
        if len(arr) > 3:  
            publicIP = re.search('(?<=\")[^\"]*?(?=\")', arr[2][1])  
            if publicIP:  
                publicIP = publicIP.group(0)  
                found = 1  
  
if found == 1:  
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +' - '+ publicIP  
else:  
    if showErrorMessage == 1:  
        print "Public ip address not found."  
