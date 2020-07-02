#/usr/bin/python3

import sys
import json

try:
  
  with open( sys.argv[1] ) as f:
    data = json.load(f)
  
  m = map(lambda file:file['file_id'],data['data']['hits'])
  j = json.dumps({"ids":sorted(set(m))}, indent=2)
  print(j)
  
except:
  sys.exit(1)


