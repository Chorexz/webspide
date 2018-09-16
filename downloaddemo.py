import requests
import re
import os,zipfile,random,time


urlofpages=['https://github.com/search?l=Java&p={}&q=stars%3A>200&type=Repositories'.format(str(i))for i in range(53,90)] #获取某页的URL
urlfile=open('E:\\VScodeworkspace\\urlfile.txt','a+')
headers={'User_Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"}
numoffiles=0            #文件计数                                                        
print (urlofpages)
for urlofpage in urlofpages:

    results=requests.get(urlofpage,headers=headers)
    resultsofurl=re.findall('<a class=.*? data-hydro-click=.*? href="(.*?)">(.*?)</a>',results.text)
    for resultofurl in resultsofurl:
        time.sleep(random.randint(1,5))               #延时以免被ban
        urlofproj=('https://github.com'+resultofurl[0]) #得到项目url
        if urlfile.writable():
            urlfile.write(urlofproj+'\n')               #将项目url写入txt文件
            
        projresults=requests.get(urlofproj)          #请求项目url数据
        branchname=re.findall('<span class="js-select-button css-truncate-target">(.*?)</span>',projresults.text)   #得到zip包名
        zipurl=(urlofproj+'/archive/'+branchname[0]+'.zip')        #得到对应zip文件的url
        req=requests.get(zipurl)      #请求zip文件url的数据
        posi=resultofurl[1].index('/')  #获取/符号位置
        zip_name=('E:\VScodeworkspace\sourcecode'+resultofurl[1][posi:]+'.zip') #拼接本地zip文件名

        try:
            with open(zip_name,'wb') as code:
                code.write(req.content)     #将获取的数据写入本地zip文件
            download=True
        except:
            print("download error in "+resultofurl[1][posi:]+'.zip')
            download=False
        if download!=False:
            fz=zipfile.ZipFile(zip_name,'r')  
            try:          
                for zipf in fz.namelist():
                    fz.extract(zipf,'E:\VScodeworkspace\sourcecode1')    #解压zip中所有文件
                numoffiles+=1
               
            except:
                print('zipfile:'+resultofurl[1][posi+1:]+'.zip  extract error')
            fz.close()                 #关闭zip文件
           
        print("all files counts "+numoffiles)   #显示计数    
        if os.path.exists(zip_name):
            os.remove(zip_name)                   #解压后删除zip文件
                             
urlfile.close()             #关闭txt文件
print("download over")                                             
