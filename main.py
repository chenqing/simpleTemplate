#!/usr/bin/env python
#coding=utf-8
import sys
import os
import shutil
import re
import time

class simpleTemplate:
    cwd_path = os.getcwd() 
    tpl_path = []
    def __init__(self,viewpath,outpath):
        """
            input:  viewpath,default is ./views
            output：outpath,default is ./html
        """
        self.viewpath = viewpath if os.path.exists(viewpath) else self.cwd_path + "/views"
        self.outpath = outpath if os.path.exists(outpath) else   self.cwd_path  + "/html"
        
    def handle_tpl(self):
        """
            input:  none,defalut is the viewpath
            output: tpl file list
        """
        tpl = [] 
        if os.path.exists(self.viewpath):
            for root , dirs , files in os.walk(self.viewpath): 
                for file in files:
                    f = os.path.join(root,file)
                    
                    if f.split('.')[-1] == "tpl":
                        tpl.append(f)
        else:
            print self.viewpath + "is not found"
            return False
        return tpl

    def handle_html(self,li,file):
        """
            Multidimensional list manage
            input : list
            output: One-dimensional list 
        """
        try:
            f = open(file,'a')
            for i in li:
                if isinstance(i,list) and len(i) > 0 :
                    self.handle_html(i,file)
                elif isinstance(i,list) and len(i) == 0 :
                    continue
                else:
                    print i
                    f.write("%s\n" % i)
                    f.flush()
            f.close()
        except:
            print "can not open file" + file

    def handle_dir(self,tpl_file):
        """
            input: tpl_file ,if tpl_file in "include dir ",then next
            output: none , if no exists the path in template path then create it in output path  else continue
        """
        dir_name = os.path.dirname(tpl_file)
        html_dir = dir_name.replace(self.cwd_path,'./').replace('views','html',1) if os.path.isabs(dir_name) else dir_name.replace('views','html',1)
        if not  os.path.exists(html_dir):
            if os.makedirs(html_dir):
                print 'cretae dir' + html_dir + 'success'


    def compile(self,tpl_file,data):
        """
            input: tpl_file ,xxx.tpl
            output: a  compiled list
        """
        htmls = []
        res = re.compile(r'.*<%(.*)%>.*')
        if os.path.exists(tpl_file) :
            for line in open(tpl_file).readlines():
                try:
                    t = res.findall(line)[0].replace('"','').replace("'","").split(' ')
                except:
                    htmls.append(line)
                    continue
                if t[1] == 'include':
                    if t[2].split('.')[-1] == 'tpl':
                        htmls.append(self.compile(self.viewpath + '/' + t[2],data))
                elif t[1].lstrip().startswith('='):
                    htmls.append(line.replace('<%','').replace('%>','').replace(t[1],data[t[1].replace('=','')]))

        return htmls

            
    def render(self,data):
        """
            input:  data,is a dict  ,example : {title:'hello world'}
        """
        html = []
        
        res = re.compile(r'.*<%(.*)%>.*')
        for file in self.handle_tpl():
            if os.path.dirname(file).split('/')[-1] == 'include':
                continue
            fs = file.replace('views','html').replace('.tpl','.html')
            html.append(self.compile(file,data))
            self.handle_dir(file)
            if os.path.isfile(fs) :
                shutil.move(fs,fs+'-'+ str(int(time.time())))
                open(fs, 'w').close() 
            self.handle_html(html,fs)


if __name__ == '__main__':

    s = simpleTemplate('views','html')
    s.render({'title':'hello','content':'world'})
