#/usr/bin/python3

import xml.sax

filename = ''

class ContentHandler( xml.sax.ContentHandler ): 
  def __init__(self): 
    self.isBody            = False
    self.currentTag        = ''
    self.CommonDataElement = ''
    self.preferred         = ''
    print('filename','tag','cde','value','preferred_name',sep='\t')
    
  def startElement(self, tag, attributes): 
    self.currentTag = tag
    if 'cde' in attributes: 
      self.CommonDataElement = attributes['cde']
    if 'preferred_name' in attributes: 
      self.preferred         = attributes['preferred_name']
    if tag == 'laml:patient':
      self.isBody = True 
  
  def characters(self, content):
    thisContent = content.strip() 
    thisTag     = self.currentTag
    if self.isBody and (thisTag != '') and not (thisContent == ''): 
      print(filename,thisTag,self.CommonDataElement,thisContent,self.preferred,sep='\t')
  
  def endElement(self, tag): 
    self.currentTag        = ''
    self.CommonDataElement = ''
    self.preferred         = ''
    if tag == 'laml:patient':
      self.isBody = False

import sys
import os
import re

if ( __name__ == '__main__'):
  
  parser = xml.sax.make_parser()
  Handler = ContentHandler()
  parser.setContentHandler( Handler )
  
  for filepathline in sys.stdin.readlines(): 
    filepath = re.sub('(\r?\n)*$','',filepathline)
    if os.path.isfile(filepath):
      filename = re.sub('^.*/','',filepath)
      parser.parse(filepath) 


