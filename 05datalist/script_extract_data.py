#/usr/bin/python3

import xml.sax

filename = ''

class ContentHandler( xml.sax.ContentHandler ): 
  def __init__(self): 
    self.isBody            = False
    self.currentTag        = ''
    self.preferred         = ''
    self.CommonDataElement = ''
    self.CDE_version       = ''
    self.xml_order         = 0
    self.xml_depth         = 0
    print('file','tag','preferred_name','cde','cde_ver',
          'xml_value','xml_order','xml_depth',sep='\t')
    
  def startElement(self, tag, attributes): 
    self.currentTag  = tag
    self.xml_order  += 1
    self.xml_depth  += 1
    if 'preferred_name' in attributes: 
      self.preferred         = attributes['preferred_name']
    if 'cde' in attributes: 
      self.CommonDataElement = attributes['cde']
    if 'cde_ver' in attributes: 
      self.CommonDataElement = attributes['cde_ver']
    if tag == 'laml:patient':
      self.isBody = True 
  
  def characters(self, content):
    thisContent = content.strip() 
    thisTag     = self.currentTag
    if self.isBody and (thisTag != '') and not (thisContent == ''): 
      print(filename,thisTag,self.preferred,self.CommonDataElement,self.CDE_version,
            thisContent,self.xml_order,self.xml_depth,sep='\t')
  
  def endElement(self, tag): 
    self.currentTag        = ''
    self.CommonDataElement = ''
    self.CDE_version       = ''
    self.preferred         = ''
    self.xml_depth        -= 1
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

