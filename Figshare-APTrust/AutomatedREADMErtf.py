# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:55:10 2021

@author: padma carstens
"""
#Following script creates README rtf file using information from Figshare article in review, works for both in review and published articles as long as all the fields are the same (currently this script accomodates metadata fields in the "Libraries" group on figshare which is modified and different from metadata fields in other groups). 


import os
from tkinter.messagebox import NO
#from figshare.figshare import Figshare
import figshare
from figshare.figshare import Figshare
from Read_VTDR_Spreadsheet import vtingsheet
from datetime import date
import re
import os
from PyRTF import *
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
  """
  Purpose:
    Retrieve figshare metadata with token and article id.  Create README.rtf and write the fields retrieved from figshare metadata and Ingest sheet into this file. Create a new README directory to save the README file

  :param Article ID: Figshare article id under "Cite" button for an article in review
  :param token: Figshare token: click circle on data.lib.vt.edu, then click "Applications" then click "Create Personal Token"
  """

  #If creating this AFTER the article is published then change "private" to "False" below
  fs=Figshare(token=token,private=True)

  #There is no versioning for article under review in figshare

  #Retrieve article information from Figshare
  details=fs.get_article_details(ArticleID,version=None)
  #Get the title of the article
  title=details["title"]
  #Get the author list
  authr=[]
  for i in range(len(details["authors"])):
   authrs=details["authors"][i]['full_name']
   authr.append(authrs)
  s=", "
  author=s.join(authr)

  #Get the categories list
  cat=[]
  for i in range(len(details["categories"])):
   cats=details["categories"][i]['title']
   cat.append(cats)
  Categoriesinfo=s.join(cat)
  #Get the corresponding author email id from spreadsheet
  #corremail=ingsheet['ingcemail']

  #Get the list of group ids
  groupidnames=fs.get_groupid_names(version=None)
  groupids=[]
  groupname=[]  
  for i in range(len(groupidnames)):
    groupid=groupidnames[i]['id']
    groupid_name=groupidnames[i]['name']
    groupids.append(groupid)
    groupname.append(groupid_name)
 
  fundinglist=[]
  for m in range(len(details['funding_list'])):
    fund=details['funding_list'][m]['title']
    fundinglist.append(fund)
  Funding=s.join(fundinglist)

  index=groupids.index(details['group_id'])# this gives the index of the group id displayed on figshare
  Group=groupname[index]#this gives the group name that the displayed group id on figshare corresponds to from the group id list 

  ItemType="Dataset"

  #Get the list of keywords
  keywords=s.join(details['tags'])
  #Strip html tags in description
  #One way of doing this:
  #x=re.sub('<[^<]+?>', '', Description)
  #In this code we are using BeautifulSoup
  #Description=(details['description']).strip('"xa0""<p>""</p>""</p>"<br>""<b>""<div>""</div>""\xa0"')
  Description=details['description']
  soup=BeautifulSoup(Description,features="html.parser")#,from_encoding="UTF-8")
  #Description=soup.get_text()
  # y=soup.get_text()
  y=soup.text
  y=y.replace(u'\xa0',u' ')
  #y=y.replace("’",)
  #y=y.replace("’","’")
  #y=y.replace(" ","\\line\\'20")
  y=y.replace("\n","\\line\n")
  #Desc
  #Description=soup.text
 
  #Description=Description.replace("\n","\\line\n")
  #Description=Description.replace(" ","\\line\\")
  #Get all the remaining fields 
  #Funding=details['funding']
  ResourceTitle=details['resource_title']
  ResourceDOI=details['resource_doi']
  License=details["license"]['name']
  Publisher=details['custom_fields'][0]['value']
  Location= details['custom_fields'][1]['value']
  #categorieslink= "https://drive.google.com/file/d/1DbQSnUuWw1xPZMmZYkucUnXtzvONyvTv/view?usp=sharing"  
  CorresAuthName=details['custom_fields'][2]['value']
  CorresAuthEmail=details['custom_fields'][3]['value']
  FilesFolders=details['custom_fields'][4]['value']
  #Remove html tags in files/folders
  soup=BeautifulSoup(FilesFolders,features="html.parser")
  x=soup.text
  x=x.replace("\n","\\line\n")
 #Replace bullets with rtf coding for bullets of different sizes
  x=x.replace("●","\\line\\bullet")
  x=x.replace("•","\\line\\bullet")
  x=x.replace(" – "," - ")

  #CorresAuthor=details['custom_fields'][4]['value']

  #Leave the metadata field empty/default value if the metadata fields are not filled in by the author
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

  #Add hyperlink to Resource DOI and References using RTF coding syntax:
  if ResourceDOI is None or ResourceDOI=='':
    ResourceDOI="Will be added after manuscript is accepted"
  else:
    ResourceDOI="{\\colortbl ;\\red0\\green0\\blue238;}{\\field{\\*\\fldinst HYPERLINK "+"\""+"https://doi.org/"+ResourceDOI+"\""+"}{\\fldrslt{\\ul\\cf1 "+str(ResourceDOI)+" }}}"
  if License is None or License=='':
    License="CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
  OtherRef=[]  
  if OtherRef is None or OtherRef=='':
    OtherRef=""
  else:
   for i in range(len(details["references"])):
     orefs=details["references"][i]
     OtherRefs="{\\colortbl ;\\red0\\green0\\blue238;}{\\field{\\*\\fldinst HYPERLINK "+"\""+orefs+"\""+"}{\\fldrslt{\\ul\\cf1 "+str(orefs)+" }}}"
     OtherRef.append(OtherRefs)
  OtherRef=s.join(OtherRef)
    
  if Publisher is None or Publisher=='':
    Publisher="University Libraries, Virginia Tech"
  if Location is None or Location=='':
    Location=""
  if FilesFolders is None or FilesFolders=='':
    FilesFolders=""


  #Create README.rtf and write the figshare fields to the file using rtf coding syntax     
  out_file_prefix = f"README.rtf"
  root_directory=os.getcwd()
  #Get the directory path from configurations.ini and make a directory with a timestamp and author name so it will not be overwritten if running this more than once for the same article id  
  readmefolder=datetime.now().strftime(README_Dir+'_%H_%M_%d_%m_%Y_'+str(authr[0]))
  readme_path=os.path.join(root_directory, readmefolder)  
  os.mkdir(readme_path)
  print("The new directory "+readmefolder+" is created")
  out_file_prefix1 = f"{readme_path}/{out_file_prefix}"
  f = open(out_file_prefix1,'w',encoding="utf-8")
  #str(Description)
  f.write("{\\rtf1\\ansi {\\b Title of Dataset:} "+str(title)+"\\line\n"+
        "{\\b Author(s):} "+str(author)+"\\line\n"+
        "{\\b Categories:} "+Categoriesinfo+"\\line\n"+        
        "{\\b Group:} "+str(Group)+"\\line\n"+
        "{\\b Item Type:} "+str(ItemType)+"\\line\n"+
        "{\\b Keywords:} "+str(keywords)+"\\line\n"+
        "{\\b Description:} "+y+"\\line\n"
        "{\\b Funding:} "+str(Funding)+"\\line\n"+
        "{\\b Resource Title:} "+str(ResourceTitle)+"\\line\n"+
        "{\\b Resource DOI:} "+str(ResourceDOI)+"\\line\n"+
        "{\\b Other References:} "+str(OtherRef)+"\\line\n"+
        "{\\b License:} "+str(License)+"\\line\n"+
        "{\\b Publisher:} "+str(Publisher)+"\\line\n"+
        "{\\b Location:} "+str(Location)+"\\line\n"+
        "{\\b Corresponding Author Name:} "+str(CorresAuthName)+"\\line\n"+
        "{\\b Corresponding Author E-mail Address:} "+str(CorresAuthEmail)+"\\line\n"+
        "{\\b Files/Folders in Dataset and Description of Files}"+"\\line\n"+
        x+ "\\line\n"+
        
        "}")
  f.close()

  return 

#Call this function to create README.rtf for the article id and token from configurations.ini  
readme_auto=create_readme(ArticleID,token)