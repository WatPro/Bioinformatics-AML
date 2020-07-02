#/usr/bin/python3

import sys
import json

if ( __name__ == '__main__' ):
  
  try: 
    filepath = sys.argv[1]
    
    with open(filepath) as f:
      data = json.load(f)
    
    j = json.dumps(data, indent=2)
    print(j)
  
  except:
    sys.exit(1)


