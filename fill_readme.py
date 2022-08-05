# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:55:10 2021

@author: padma carstens
"""
#Following code creates README rtf file using information from Figshare article

from figshare.figshare import Figshare
from spreadsheet import vtingsheet
from datetime import date
import re
import os
from PyRTF import *
from bs4 import BeautifulSoup
from datetime import datetime

#Get the parameters from secrets.txt created in the curation folder
filename="secrets.txt"
fileObj=open(filename)
params={}
for line in fileObj:
    line=line.strip()
    key_value=line.split('=')
    if len(key_value)==2:
        params[key_value[0].strip()]=key_value[1].strip()

#Get the article id from secrets.txt 
ArticleID=params["ArticleID"]
#Get the Published Version number from secrets.txt
PublishedVersionNumber=params["PublishedVersionNumber"]
#Get the Ingest Version number from secrets.txt
IngestVersionNumber=params["IngestVersionNumber"]
#Get your figshare token from secrets.txt
token=params["token"]
#Get curator name from secrets.txt
CuratorName=params["CuratorName"]
ingsheet=vtingsheet(ArticleID,IngestVersionNumber)

def create_readme(ArticleID,token):
  #If creating this AFTER published then change private to False below
  fs=Figshare(token=token,private=True)
  #fs=Figshare(token=token,private=False)
  details=fs.get_article_details(ArticleID,version=None)
  title=details["title"]
  authr=[]
  for i in range(len(details["authors"])):
   authrs=details["authors"][i]['full_name']
   authr.append(authrs)
  s=","
  author=s.join(authr)
  cat=[]
  for i in range(len(details["categories"])):
   cats=details["categories"][i]['title']
   cat.append(cats)
  Categoriesinfo=s.join(cat)
  #corremail="Not yet available"
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
  #Description=Description.replace('\n',' ')
  #Description=Description.replace('\n',' ').replace('<b>',' ').replace
  Funding=details['funding']
  if Funding is None:
     Funding='None'
  ResourceTitle=details['resource_title']
  if ResourceTitle is None:
    ResourceTitle="Will be added after manuscript is accepted"
  ResourceDOI=details['resource_doi']
  if ResourceDOI is None:
    ResourceDOI="Will be added after manuscript is accepted"
  OtherRef=details['references']

  #Convert Other Ref to string:
  OtherRef=''.join(OtherRef)
  
  if title is None:
    title="-"
  if author is None:
    author="-"
   
  if OtherRef is None:
    OtherRef="Not Provided"
  #License="CC-0 1.0 Universal (CC0 1.0) Public Domain Dedication"
  License=details["license"]['name']
  #Publisher="University Libraries, Virginia Tech"
  #Language="English"
  Publisher=details['custom_fields'][0]['value']
  if Publisher is None:
     Publisher="University Libraries, Virginia Tech"
  Language=details['custom_fields'][1]['value']
  if Language is None:
    Language="English"
  Location= details['custom_fields'][2]['value']
  if Location is None:
    Location="Not provided"
  categorieslink= "https://drive.google.com/file/d/1DbQSnUuWw1xPZMmZYkucUnXtzvONyvTv/view?usp=sharing"
  #CorresAuthEmail=details['custom_fields'][3]['value']
  #FilesFolders=details['custom_fields'][4]['value']
  #soup1=BeautifulSoup(FilesFolders,features="html.parser")
  #FilesFolders=soup1.get_text()
  out_file_prefix = f"README.rtf"
  root_directory=os.getcwd()
  readmefolder=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/README_FILES_%H_%M_%d_%m_%Y_'+str(authr[0]))
  readme_path=os.path.join(root_directory, readmefolder)#"README_FILES_%Y%m%d_%H%M")
  #Check if README_FILES exists or not
  #isExist=os.path.exists(readme_path) #True or False
  #if not isExist:
  #  os.mkdir(readme_path)
    #print("The new directory README_FILES is created")
  os.mkdir(readme_path)
  out_file_prefix1 = f"{readme_path}/{out_file_prefix}"
  f = open(out_file_prefix1,'w')
  f.write("{\\rtf1\\ansi {\\b Title of Dataset:} "+str(title)+"\\line\n"+
        "{\\b Author(s):} "+str(author)+"\\line\n"+
        "{\\b Corresponding Author Email Address:} "+"\\line\n"+
        "{\\colortbl ;\\red0\\green0\\blue238;}{\\field{\\*\\fldinst HYPERLINK "+"\""+categorieslink+"\""+"}{\\fldrslt{\\ul\\cf1 "+"Categories: }}}"+Categoriesinfo+"\\line\n"+
        "{\\b Group:} "+str(Group)+"\\line\n"+
        "{\\b Item Type:} "+str(ItemType)+"\\line\n"+
        "{\\b Keywords:} "+str(keywords)+"\\line\n"+
        "{\\b Description:} "+str(Description)+"\\line\n"
        "{\\b Funding:} "+str(Funding)+"\\line\n"+
        "{\\b Resource Title:} "+str(ResourceTitle)+"\\line\n"+
        "{\\b Resource DOI:} "+str(ResourceDOI)+"\\line\n"+
        "{\\b Other References:} "+str(OtherRef)+"\\line\n"+
        "{\\b License:} "+str(License)+"\\line\n"+
        "{\\b Publisher:} "+str(Publisher)+"\\line\n"+
        "{\\b Language:} "+str(Language)+"\\line\n"+
        "{\\b Location:} "+str(Location)+"\\line\n"+
        "{\\b Files/Folders in Dataset and Description of Files}"+"\\line\n"+
        "}")
  f.close()

  return 
readme_auto=create_readme(ArticleID,token)