#!/usr/bin/python3


PLUG_NAME    = "renameF"

import os
import sys

USE_R2  = False

if "radare2" in os.environ.get('PATH',''):
    USE_R2  = True
else:
    print("ERROR: The plugin must be run in radare2")
    sys.exit(0)

#returns a list containing the 10000 most used words in the english language 
def english():
    a_file = open("10000-english.txt", "r")
    listE= []
    for line in a_file:
        listE.append(line.strip())
    a_file.close()
    return listE  

def getFunctionInfo(r2,englishWords):
    lines=r2.cmd("afl").split('\n')
    for i in range(len(lines)):
        line=lines[i].split()
        if line != []:
            f_name=line[len(line)-1]
            if f_name.startswith('fcn.'): #for any function not yet renamed
                f_address=line[0]
                f_size=line[len(line)-2]
                renameFunction(englishWords,r2,f_name,f_address,f_size)
                
#rename the function in the form word1_word2_(a letter reflecting the function's size_ the number of distinct xref to the function_number of distinct xref from the function)
def renameFunction(english_words,r2,f_name,f_address,f_size):
    number=int(f_address, 16)
    #we devide the function's address in the decimal form to 2 numbers: the first 4 integers and the second 4 integers
    #this partition is more than enough to cover all the functions' addresses
    n1=number//10000%10000 # "%10000" is added as a precaution but it is not necessary in practise and it doesn't change anything  
    n2=number%10000
    f_name=english_words[n1]+'_'+english_words[n2]+"_("+rangeSize(int(f_size))+"_"+xref_to(r2,f_address)+"_"+xref_from(r2,f_address)+")"
    r2.cmd("afn %s %s" % (f_name, f_address))

def rangeSize(n):
    # define 3 classes of size: below 100 bytes, between 100 and 1000 bytes and above 1000 bytes
    if n<100:
        return "s"
    elif n<1000:
        return "m"
    else:
        return "l"
    
def distinct_functions(t,pos):
    if t!="":  
        if "\n" in t:
            distinct=0
            function_names=[]
            for line in t.strip().split("\n"):
                if line.split(" ")[pos] not in function_names:
                    function_names.append(line.split(" ")[pos])
                    distinct+=1
            return str(distinct)
        else :
            return "1"
    else:
        return "0"
        
#returns the number of distinct functions that call the function having f_address as address
def xref_to(r2,f_address):
    #return(r2.cmd("axt "+f_address+" ~CALL ~?").strip())  can be used if the goal is to retrieve the number of functions that call f_address (not distinct) 
    t=r2.cmd("axt "+f_address+" ~CALL").strip()
    return distinct_functions(t,0)    
    
#returns the number of distinct functions that are called by the function having f_address as address
def xref_from(r2,f_address):
    r2.cmd("s "+f_address)
    t=r2.cmd("axff[j] ~CALL").strip()
    return distinct_functions(t,3)

#list all functions
def listFunctionsAfterRename(r2):
    print(r2.cmd("afl"))

def renameF():
    import r2pipe
    r2=r2pipe.open()
    r2.cmd("aaa")
    englishWords=english()
    getFunctionInfo(r2,englishWords)
    listFunctionsAfterRename(r2)
    
if USE_R2:
    renameF()

