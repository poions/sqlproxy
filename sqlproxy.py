# encoding: utf-8
import MySQLdb as mdb
import MySQLdb
import requests
import re,os
import urllib2
import threading
import json
import getopt,sys
import time
config = {
         "url":"http://127.0.0.1:8775"
        }
threads = 20
excludes = ['.jpg','.png','.bmp','.html','.gif','.avi','.mp3','.mp4','.css','.js','.rar','.zip','.doc','.docx','.pdf','.swf']

class Stop(threading.Thread): 
    def run(self): 
        while 1: 
            try: 
                if raw_input('') == 'q': 
                    os._exit(1) 
                else:
                    print "stopped by your action ( q )" 
            except: 
                os._exit(1) 
class Sqli(threading.Thread):
    def __init__(self,payload):
        threading.Thread.__init__(self)
        self.payload = payload

    def run(self):
        global threads
        url = config["url"]
        task = requests.get(url+"/task/new")
        task_id = task.json()
        task_id = task_id['taskid']
        headers = {'content-type': 'application/json'}
        r = requests.post(url+'/scan/'+task_id+'/start',data=json.dumps(self.payload),headers=headers)
        while 1:
            time.sleep(5)
            rstatus = requests.get(url+'/scan/'+task_id+'/status')
            # print self.payload['url']+"  is  "+rstatus.json()["status"]
            if rstatus.json()["status"] == 'terminated':
                break;
        t = url+'/scan/'+task_id+'/data'
        t_id = requests.get(t)
        result = t_id.json()
        if len(result['data'])==0: 
            print self.payload['url']+"  no sqli"
            print "="*50
            requests.get(url+'/scan/'+task_id+'/delete')
            requests.get(url+'/scan/'+task_id+'/stop')
            threads+=1
            return;
        with open("/var/www/html/result.txt","a+") as wf:
            wf.write(self.payload['url']+'\n')
            for l in  re.findall("'title':.*?'(.*?)'.*?'payload':.*?'(.*?)'",str(result)):
                wf.write(str(l)+'\n')
            wf.write("="*50+'\n')
        print self.payload['url']+"   sqli"
        print "="*50
        # requests.get(url+'/scan/'+task_id+'/stop')
        requests.get(url+'/scan/'+task_id+'/delete')
        threads+=1

def InitOptions():
    try:  
        opts,args = getopt.getopt(sys.argv[1:],"ht:u:",["help","thread=","url="])
        for option, value in opts:  
            if  option in ["-h","--help"]:  
                print """  
                usage:%s -t value or --thread=threads_num
                usage:%s -u value or --url=server_url
                """  
                sys.exit(1); 
            elif option in ['--thread', '-t']:  
                global threads 
                threads = int(value)
            elif option in ['--url', '-u']:
                config['url'] = value
    except getopt.GetoptError:  
        # print "option error! -h or --help"
        sys.exit(1); 

if __name__ == '__main__':

    InitOptions()
    try:
        conn = MySQLdb.connect(host='192.168.58.128',user='root',passwd='1q2w3e4r',db='wyproxy')
    except Exception, e:
        print e
        sys.exit()
    cursor = conn.cursor()
    Stop().start()
    _id = -1
    while 1:
        print threads
        if threads<=0: threads=0;continue
        sql = 'select id,url from capture where static_resource=0 and status_code=200 and content_length>0 and id>%d order by id asc' % _id
        cursor.execute(sql)
        rows = cursor.fetchall()
        for r in rows:
			if threads<=0: threads=0;continue
			if r[0] > _id:
				_id=r[0]
				sqlurl = (r[1])
				b = False
				for key in excludes:
					if key in sqlurl: b = True
				if b: 
                    # print "skip " + sqlurl
					continue
				print "Start injection"
				print sqlurl
				payload = {"url":sqlurl}
				threads-=1
				print threads
				Sqli(payload).start()
		time.sleep(5)

