import time
from re import search, IGNORECASE, escape, findall

from lib import utilities

# 20231129 135234 DEBUG 13 and searching for regexp pattern [Query Volume [\w\*\-\.\/\\\$]+ (\w+=.*){1,} ACCess=]
# 20231129 135234 DEBUG 13 and searching for regexp pattern [^(Query|Quer|Que|Qu|Q)\s+(Volume|Volum|Volu|Vol|Vo|V)\s+([\w\*\-\.\/\\\$]+)\s+((\w+=.*){1,})\s+(ACCess|ACCes|ACCe|ACC)=(?!.*\w+\s)]
# 20231129 135234 INFO   DEBUG IF START ---------------- 
# 20231129 135236 INFO   DEBUG IF END ---------------- 

key    = "Query Volume [\w\*\-\.\/\\\$]+ (\w+=.*){1,} ACCess="
genkey = "^(Query|Quer|Que|Qu|Q)\s+(Volume|Volum|Volu|Vol|Vo|V)\s+([\w\*\-\.\/\\\$]+)\s+((\w+=.*){1,})\s+(ACCess|ACCes|ACCe|ACC)=(?!.*\w+\s)"
tokens = ['query',
 'vol',
 '/sp/filedevs/file001',
 'ACCess=READWrite',
 'STatus=EMPty',
 'STatus=EMPty',
 'STatus=EMPty',
 'STatus=EMPty',
 'STatus=EMPty',
 'STatus=EMPty',
 'STatus=EMPty',
 'STatus=']

extradelimiter = '='

print( time.time() )
search( genkey, ' '.join( tokens ) )
print( time.time() )

print()

print( time.time() )
search( '^' + utilities.regexpgenerator( key ) + extradelimiter, ' '.join( tokens ) + extradelimiter, IGNORECASE )
print( time.time() )
