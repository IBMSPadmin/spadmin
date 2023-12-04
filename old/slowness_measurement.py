import time
from re import search, IGNORECASE, escape, findall, MULTILINE, compile

#from lib import utilities

def regexpgenerator(regexp):
    savelastchar = ''
    if regexp[-1] == '=':
        savelastchar = regexp[-1] + '(?!.*\w+\s)'
        regexp = regexp[: -1]
    # # save v2 with regexp pattern
    # match = search( '(=.*)$', regexp )
    # if match:
    #   savelastchar = match[ 1 ]
    #   regexp = regexp.replace( match[ 1 ], '' )  

    result = ''
    for part in regexp.split():

        if part[0].isupper():

            tmpregexp = part
            tmpstring = part
            # print( part + str( time.time() ) )
            for x in part:
                if tmpstring[-1].isupper():
                    break
                tmpstring = part[0:len(tmpstring) - 1]
                tmpregexp += '|' + tmpstring

            result += '(' + tmpregexp + ')'

        else:
            result += '(' + part + ')'

        result += '\s+'

    return result[:-3] + savelastchar

# 20231129 135234 DEBUG 13 and searching for regexp pattern [Query Volume [\w\*\-\.\/\\\$]+ (\w+=.*){1,} ACCess=]
# 20231129 135234 DEBUG 13 and searching for regexp pattern [^(Query|Quer|Que|Qu|Q)\s+(Volume|Volum|Volu|Vol|Vo|V)\s+([\w\*\-\.\/\\\$]+)\s+((\w+=.*){1,})\s+(ACCess|ACCes|ACCe|ACC)=(?!.*\w+\s)]
# 20231129 135234 INFO   DEBUG IF START ---------------- 
# 20231129 135236 INFO   DEBUG IF END ---------------- 

key    = "Query Volume [\w\*\-\.\/\\\$]+ (\w+=\w*\s+){1,} ACCess="
#           Query                   Volume                         [\w\*\-\.\/\\\$]+     (\w+=.*){1,}     ACCess=
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

import timeit

print( "1" )
t = time.time()
print( genkey )
print( ' '.join( tokens ) ) 

print( type( genkey ) )

search( genkey, ' '.join( tokens ).lower() )
print( time.time() - t )

print()

print( "1g" )
t = time.time()
print( genkey )
print( ' '.join( tokens ) ) 

print( regexpgenerator( key ) )

search( regexpgenerator( key ), ' '.join( tokens ) )
print( time.time() - t )

# print()

# print( "1i" )
# t = time.time() 
# search( genkey, ' '.join( tokens ), IGNORECASE )
# print( time.time() - t )

# print()

# print( "2i" )
# t = time.time() 
# print( regexpgenerator( key ) )
# print(' '.join( tokens ))
# alma = '^' + regexpgenerator( key ) + extradelimiter
# search( genkey, ' '.join( tokens ) + extradelimiter, IGNORECASE )
# print( time.time() - t )

# print()

# print( "3lower" )
# t = time.time() 
# search( ( '^' + regexpgenerator( key ) + extradelimiter ).lower(), (' '.join( tokens ) + extradelimiter ).lower() )
# print( time.time() - t )

# from string import ascii_letters, ascii_lowercase

# alpha, lower = [ s.encode( 'ascii' ) for s in [ ascii_letters, ascii_lowercase] ]
# table = bytes.maketrans( alpha, lower * 2 )           # convert to lowercase
# # deletebytes = bytes(set(range(256)) - set(alpha)) # delete nonalpha

# print()

# print( "4translate" )
# t = time.time() 
# print("AAAAAAAA".translate(table))
# search( ( '^' + regexpgenerator( key ) + extradelimiter ).translate( table ), ( ' '.join( tokens ) + extradelimiter ).translate( table ) )
# print( time.time() - t )

# print()

# print( "4translate" )

# a = str( '^' + regexpgenerator( key ) ).translate( table )
# b = str( ' '.join( tokens ) ).translate( table )

# t = time.time()
# print( type(a) )
# print( a )
# print( b )
# search( a, b )
# print( time.time() - t )

# print()

# print( "1" )
# t = time.time()
# print( genkey )
# print( ' '.join( tokens ) ) 
# search( genkey, ' '.join( tokens ) )
# print( time.time() - t )

print()

print( "5strdecode" )

a = compile( ( '^' + regexpgenerator( key ).lower() ) )
b = ( ' '.join( tokens ) ).lower()

# a = a.encode('ascii', 'replace')
# b = b.encode('ascii', 'replace')

t = time.time()
print( type(a) )
print( a )
print( b )
search( a, b )
print( time.time() - t )

