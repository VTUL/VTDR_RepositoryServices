# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:55:10 2021

@author: padma
"""
curator="Padma "
import fontstyle
IngestAccessionNumber= "I00180"
PublishedAccessionNumber= "P00154"
#Enter requestor name
Requestor="BrownR"
#Enter corresponding author name
CorrespondingAuthor="BrownR"
#Enter version
Version="01"
#Enter published date in YYYYMMDD format 
DatePublished= "20211025"  
#Enter DOI:
DOI="abc"
#Enter Title:
Title="abc"
authoremail="xyz@x.edu"
college="abc"
dept="abc"
comment="abc"
DateIngested="20210202"


f = open('ArchivalPackage.rtf',"w")
f.write("This Archival Information Package created by "+curator+"on "+DatePublished+"\n"+
        "Virginia Tech Curation Services\n"+
        "*****************************\n"+
        "Accession # for Ingest: "+ IngestAccessionNumber+"\n"+
        "Accession # for Publication: "+PublishedAccessionNumber+"\n"+
        "Requestor: "+Requestor+"\n"+
        "Corresponding Author: "+CorrespondingAuthor+"\n"+
        "Version #: "+"\n"+
        "Date Published: "+"\n"+
        "DOI: "+DOI+"\n"+
        "Dataset Title: "+Title+"\n"+
        "Corresponding Author Email: "+authoremail+"\n"+
        "College: "+college+"\n"+
        "Department: "+dept+"\n"+
        "Date of Most Recent Comment: "+DatePublished+"\n"+
        "Most Recent Comment: "+comment+"\n"+
        "Bag Containing Original Content: "+IngestAccessionNumber+"_"+Requestor+"_"+CorrespondingAuthor+"_"+"v"+Version+"_"+DateIngested+".tar"+"\n"
        "*****************************"+"\n"+
        "DisseminationContent (directory) contains"+"\n"+
        "	-content and metadata made accessible through the Virginia Tech Data Repository; more information about this repository can be found at http://doi.org/10.17616/R3JF54 "+"\n"+
        "VTCurationServicesActions (directory) contains"+"\n"+
        "	-e-mail correspondence, provenance log(s), a form for capturing metadata from the Virginia Tech research, and any other files associated with actions conducted by Virginia Tech "+"\n"+
        "Curation Services to augment the original files and metadata transferred to Virginia Tech Curation Services by a Virginia Tech researcher for their publication as a dataset")
f.close()
