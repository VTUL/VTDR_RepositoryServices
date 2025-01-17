#Following code creates README text file using information from Figshare article

from tkinter.messagebox import NO
from figshare.figshare import Figshare
from Read_VTDR_Spreadsheet import vtingsheet
from datetime import date
import re
import os
#from PyRTF import *
from bs4 import BeautifulSoup
from datetime import datetime

#Get the parameters from configurations.ini to retrieve information from an article on Figshare
import configparser
#config=configload.read_config()
config=configparser.ConfigParser()
config.read('configurations.ini')

#Get the ArticleID
ArticleID=config['FigshareSettings']['FigshareArticleID']
#Get the Published Version number 
PublishedVersionNumber=config['FigshareSettings']['PublishedVersionNumber']
#Remove "0" from the published version number 
intPublishedVersionNumber=int(PublishedVersionNumber[1])

#Get the Ingest Version number 
IngestVersionNumber=config['FigshareSettings']['IngestVersionNumber']
#Remove "0" from Ingest version number
intIngestVersionNumber=int(IngestVersionNumber[1])
#Get your figshare token 
token=config['FigshareSettings']['token']
#Get curator name 
CuratorName=config['FigshareSettings']['CuratorName']
#Get the directory in which to store README file
README_Dir=config['AutomatedREADMEPathSettings']['README_Dir']
#Get information from Ingest Sheet, access google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7 and get information about the article using article ID and version number.
ingsheet=vtingsheet(ArticleID,IngestVersionNumber)

def create_readme(ArticleID,token):
  #If creating this AFTER published then change private to False below
  fs=Figshare(token=token,private=True)
  #NO VERSIONING IN INGEST!!
  details=fs.get_article_details(ArticleID,version=None)
  title=details["title"]
  authr=[]
  for i in range(len(details["authors"])):
   authrs=details["authors"][i]['full_name']
   authr.append(authrs)
  s=", "
  author=s.join(authr)
  cat=[]
  for i in range(len(details["categories"])):
   cats=details["categories"][i]['title']
   cat.append(cats)
  Categoriesinfo=s.join(cat)
  corremail=ingsheet['ingcemail']
  groupidnames=fs.get_groupid_names(version=None)
  groupids=[]
  groupname=[]  
  for i in range(len(groupidnames)):
    groupid=groupidnames[i]['id']
    groupid_name=groupidnames[i]['name']
    groupids.append(groupid)
    groupname.append(groupid_name)

  index=groupids.index(details['group_id'])# this gives the index of the group id displayed on figshare
  Group=groupname[index]#this gives the group name that the displayed group id on figshare corresponds to from the group id list 

  ItemType="Dataset"
  keywords=s.join(details['tags'])
  #Strip html tags in description
  #One way of doing this:
  #x=re.sub('<[^<]+?>', '', Description)
  #In this code we are using BeautifulSoup
  #Description=(details['description']).strip('"<p>""</p>""<br>""<b>""<div>""</div>"')
  Description=details['description']
  soup=BeautifulSoup(Description,features="html.parser")
  Description=soup.get_text()
  #Description=soup.body.find('div', attrs={'class':'container'}).text
  #Description=Description.replace('\n',' ')
  #Description=Description.replace('\n',' ').replace('<b>',' ').replace
  Funding=details['funding']
  ResourceTitle=details['resource_title']
  ResourceDOI=details['resource_doi']
  License=details["license"]['name']
  Publisher=details['custom_fields'][0]['value']
  Location= details['custom_fields'][1]['value']
  #categorieslink= "https://drive.google.com/file/d/1DbQSnUuWw1xPZMmZYkucUnXtzvONyvTv/view?usp=sharing"  
  CorresAuthEmail=details['custom_fields'][2]['value']
  FilesFolders=details['custom_fields'][3]['value']
  soup=BeautifulSoup(FilesFolders,features="html.parser")
  x=soup.text
  #x=x.replace("\n","\\line\n")
 #open in both notepad and word to see how this works
  #x=x.replace("●","\\line\\bullet")
  #x=x.replace("•","\\line\\bullet")
  #string_name=x
  #for element in range(0,len(string_name)):
  # if element=='â':
  #  print("YES")
  CorresAuthor=details['custom_fields'][4]['value']
  if title is None or title=="":
    title=""
  if author is None or author=="":
    author=""
  if CorresAuthEmail is None or CorresAuthEmail=="":
    CorresAuthEmail=""
  if Categoriesinfo is None or Categoriesinfo=='':
    Categoriesinfo=""
  if Group is None or Group=='':
    Group=""
  if ItemType is None or ItemType=='':
    ItemType=""
  if keywords is None or keywords=='':
    keywords=""
  if Description is None or Description=='':
    Description=""
  if Funding is None or Funding=='':
    Funding=""
  if ResourceTitle is None or ResourceTitle == "":
    ResourceTitle="Will be added after manuscript is accepted"

  if ResourceDOI is None or ResourceDOI=='':
    ResourceDOI="Will be added after manuscript is accepted"
  #else:
   # ResourceDOI="\*\\fldinst HYPERLINK "+"\""+"https://doi.org/"+ResourceDOI+"\""+"}{\\fldrslt{\\ul\\cf1 "+str(ResourceDOI)+" }}}"
  if License is None or License=='':
    License="CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
  OtherRef=[]  
  if OtherRef is None or OtherRef=='':
    OtherRef=""
  else:
   # OtherRef=details["references"]
   for i in range(len(details["references"])):
     orefs=details["references"][i]
     OtherRefs=str(orefs)#+" }}}"
     OtherRef.append(OtherRefs)
  OtherRef=s.join(OtherRef)
    
  if Publisher is None or Publisher=='':
    Publisher="University Libraries, Virginia Tech"
  if Location is None or Location=='':
    Location=""
  if FilesFolders is None or FilesFolders=='':
    FilesFolders=""
        
  out_file_prefix = f"README.txt"
  root_directory=os.getcwd()

  readmefolder=datetime.now().strftime(README_Dir+'_%H_%M_%d_%m_%Y_'+str(authr[0]))
  readme_path=os.path.join(root_directory, readmefolder)  
  os.mkdir(readme_path)
  print("The new directory "+readmefolder+" is created")
  out_file_prefix1 = f"{readme_path}/{out_file_prefix}"
  f = open(out_file_prefix1,'w',encoding="utf-8")
  
  f.write(" Title of Dataset: "+str(title)+"\n"+
        " Author(s): "+str(author)+"\n"+
        " Categories: "+Categoriesinfo+"\n"+        
        " Group: "+str(Group)+"\n"+
        " Item Type: "+str(ItemType)+"\n"+
        " Keywords: "+str(keywords)+"\n"+
        " Description: "+str(Description)+"\n"
        " Funding: "+str(Funding)+"\n"+
        " Resource Title: "+str(ResourceTitle)+"\n"+
        " Resource DOI: "+str(ResourceDOI)+"\n"+
        " Other References: "+str(OtherRef)+"\n"+
        " License: "+str(License)+"\n"+
        " Publisher: "+str(Publisher)+"\n"+
        " Location: "+str(Location)+"\n"+
        " Corresponding Author Name: "+str(CorresAuthor)+"\n"+
        " Corresponding Author E-mail Address: "+str(CorresAuthEmail)+"\n"+
        " Files/Folders in Dataset and Description of Files"+"\n"+
        x)
  f.close()

  return 
readme_auto=create_readme(ArticleID,token)

import re

def info(self):
    #text_browser = self.dockwidget.text_browser
    file_path = os.getenv("readmetxt_filepath")
    f = open(file_path, 'r', encoding="utf-8")
    text = f.read()
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    for x in urls:
        if x in text:
            text = text.replace(x, x.replace('http', '<a href="http').replace(')', '">') + x + '</a>')

    #textBrowser.setHtml(text)
    #textBrowser.setOpenExternalLinks(True)
    #self.dockwidget.show()