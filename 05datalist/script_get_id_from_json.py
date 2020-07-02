#/usr/bin/python3

import sys
import json

if ( __name__ == '__main__' ):
  
  try: 
    filepath = sys.argv[1]
    
    with open(filepath) as f:
      data = json.load(f)
    
    publicId = data['dataElement']['dataElementDetails']['publicId']
    print(publicId)
  
  except:
    sys.exit(1)


