import re
import json
import requests    
import time
import shutil

def par(x,i):
    k=1
    while(i<len(x)):
        if x[i]=='(':
            k=k+1
        elif x[i]==')':
            k=k-1
            if k==0:
                return(i)
        i=i+1



def expression_list(ex):
    op=['+','-','*','/','%']
    if '(' in ex:
        x=re.sub(' ','',ex)
        i=0
        z=[]
        y=''
        k=0
        while(i<len(x)):
            sag=0
            if x[i] in op:
                if '(' in y:
                    a=x[k:]
                    j=i
                    r=par(a,a.find('(')+1)
                    end=r+k
                    while i<len(x):
                        if x[i] in op:
                            if i<end:
                                i=i+1
                            else:
                                y=y+x[j:i]
                                z.append(y)
                                z.append(x[i])
                                y=''
                                i=i+1
                                sag=-1
                                break
                        else:
                            i=i+1
                    if sag==0:
                        y=y+x[j:]
                        z.append(y)
                        break
                else:
                    k=i+1
                    z.append(y)
                    z.append(x[i])
                    y=''
                    i=i+1
            else:
                y=y+x[i]
                if(i==len(x)-1):
                    z.append(y)
                i=i+1

        return(z)
    else:
        x=re.sub(' ','',ex)
        i=0
        z=[]
        y=''
        while(i<len(x)):
            if x[i] in op:
                z.append(y)
                z.append(x[i])
                y=''
            else:
                y=y+x[i]
                if(i==len(x)-1):
                    z.append(y)
            i=i+1
        return(z)

def expression(ex_list):
    ex_dic={}
    if len(ex_list)==1:
        if '(' in ex_list[0]:
            r=call(ex_list[0])
            return(r)
        else:
            if ex_list[0].isnumeric():
                return(int(ex_list[0]))
            else:
                return(ex_list[0])
    else:
        ex_dic["type"]=ex_list[1]
        if '(' in ex_list[0]:
            ex_dic["A"]=call(ex_list[0])
        else:
            if ex_list[0].isnumeric():
                ex_dic["A"]=int(ex_list[0])
            else:
                ex_dic["A"]=ex_list[0]
        if len(ex_list)==3:
            if '(' in ex_list[2]:
                ex_dic["B"]=call(ex_list[2])
                return(ex_dic)
            else:
                if ex_list[2].isnumeric():
                    ex_dic["B"]=int(ex_list[2])
                else:
                    ex_dic["B"]=ex_list[2]
                return(ex_dic)
        else:
            ex_list.remove(ex_list[0])
            ex_list.remove(ex_list[0])
            ex_dic["B"]=expression(ex_list)
            return(ex_dic)


def arg_list(a):
    i=0
    c=[]
    b=''
    while  i<len(a):
        if a[i]=='(':
            r=par(a,i+1)
            b=b+a[i:r+1]
            c.append(b)
            b=''
            i=r+1
        else:
            if(a[i]==','):
                c.append(b)
                b=''
            else:
                b=b+a[i]
        i=i+1
        if i==len(a):
            c.append(b)
    return(c)




def arg(args):
    args1=[]
    for arg in args:
        arg_list=expression_list(arg)
        r=expression(arg_list)            
        args1.append(r)
    return(args1)

def call(func):
    call_dic={}
    start=func.find('(')
    name=func[0:start]
    call_dic["type"]="function call"
    call_dic["function name"]=name
    func=re.sub(' ','',func)
    start=func.find('(')
    end=func.rfind(')')
    args=func[start+1:end]
    args=arg_list(args)
    r=arg(args)
    call_dic["args"]=r
    return(call_dic)


def func(name,i,func_names):
    dicfunc={}
    dicfunc["type"]="function definition"
    dicfunc["function name"]=name
    start=i.find('(')
    i=re.sub(' ','',i)
    start=i.find('(')
    end=par(i,start+1)
    args=i[start+1:end]
    args=arg_list(args)
    if(args==['']):
        dicfunc["args"]=[]
    else:
        args=arg(args)
        dicfunc["args"]=args    
    start=i.find(')')
    ex=i[start+1:]
    ex_list=expression_list(ex)
    r=expression(ex_list)
    dicfunc["expression"]=r
    return(dicfunc)

def rfunc(i,expressions):
    dic_rfunc={}
    start=i.find('(')
    name=i[6:start]
    dic_rfunc['type']="recursive function definition"
    dic_rfunc['function name']=name
    i=re.sub(' ','',i)
    start=i.find('(')
    end=i.find(')')
    args=i[start+1:end].split(',')
    if args==['']:
        dic_rfunc['args']=[]
    else:
        args=arg(args)
        r=args[len(args)-1]
        args.remove(args[len(args)-1])
        if args==['']:
            dic_rfunc['args']=[]
        dic_rfunc["args"]=args
    dic_rfunc['recursive arg']=r
    base=expressions[0]
    rec=expressions[1]
    base=base[2:]
    rec=rec[2:]
    base_list=expression_list(base)
    base_ex=expression(base_list)
    dic_rfunc['base expression']=base_ex
    rec_list=expression_list(rec)
    rec_ex=expression(rec_list)
    x={}
    x["recursive value name"]=expressions[1][0]
    x['expression']=rec_ex
    dic_rfunc['recursive expression']=x
    return(dic_rfunc)

def json1(size,funcs):
    dic={}
    dic["height"]=int(size.split()[0])
    dic["width"]=int(size.split()[1])
    list_funcs=[]
    func_names=["drawPoint","drawLine","drawCircle"]
    j=0
    while(j<len(funcs)):
        i=funcs[j]
        i=i.strip()
        if(i[0]=='f'):
            x=5
            name=''
            while(i[x]!='('):
                name=name+i[x]
                x=x+1
            func_names.append(name)
            r=func(name,i,func_names)
            list_funcs.append(r)
            j=j+1
        elif(i[0]=='r'):
            expressions=[]
            b=funcs[j+1]
            b=b.strip()
            expressions.append(b)
            c=funcs[j+2]
            c=c.strip()
            expressions.append(c)
            r=rfunc(i,expressions)
            list_funcs.append(r)
            j=j+3
    dic["functions"]=list_funcs
    return(dic)





def main():
    file=open('sample.sp')
    text=file.read()
    list_text=text.split('\n')
    while '' in list_text:
        list_text.remove('')
    #valid(list_text)
    size=list_text[0]
    list_text.remove(list_text[0]) 
    funcs=list_text
    x=json1(size,funcs)
    z=json.dumps(x, indent=2)
    return(z)

main()

def valid(list_text):
    size=list_text[0]
    size=size.split()
    #print(list_text)
    if len(size)==2:
        if size[0].isnumeric() and size[0].isnumeric():
            sag=1
        else:
            return("program is not valid:\n error in line 1:\n height and width not defined")
    else:
        return("program is not valid:\n error in line 1:\n height and width not defined")
    x=0
    for i in list_text:
        if "main(" in i:
            x=1
            break
    if x==0:
        return("program is not valid:\n error in program:\n there is no function main")
   





def req():
    jsn=main()
    res=requests.post("http://127.0.0.1:1020/job",json=jsn)
    i=res.json()
    r=requests.get("http://127.0.0.1:1020/job/{}".format(i))
    ex=r
    while(True):
        z=requests.get("http://127.0.0.1:1020/job/{}".format(i))
        print(z.json())
        if z.json()!=r.json():
            break
    x=z.json()
    url=x["download url"]
    l=requests.get("http://127.0.0.1:1020{}".format(url),stream=True)
    with open('image.jpg', 'wb') as out_file:
        shutil.copyfileobj(l.raw, out_file)
req()






