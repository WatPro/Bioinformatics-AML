#/usr/bin/python3

import sys
import json
import re

if ( __name__ == '__main__' ):
  
  print('public_id','perferred_question','element_definition','concept_definition',sep='\t')
  
  for filepathline in sys.stdin.readlines(): 
    
    filepath = re.sub('(\r?\n)*$','',filepathline)
    with open(filepath) as f:
      data = json.load(f)
    
    try: 
      publicId=data['dataElementConcept']['selectedDataElement']['publicId']
      perferred=data['dataElementConcept']['selectedDataElement']['preferredQuestionText']
      elementDefinition=data['dataElementConcept']['selectedDataElement']['definition']
      conceptDefinition=data['dataElementConcept']['dataElementConceptDetails']['definition']
      print(publicId,perferred,elementDefinition,conceptDefinition,sep='\t')
    except TypeError: 
        continue


