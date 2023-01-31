import json
from PIL import Image, ImageDraw
import copy
import time


class pillow():
    def __init__(self,main_args,args,name):
        self.main_args=main_args
        self.args=args
        self.name=name
    def draw(self):
        a=ImageDraw.Draw(pillow.img)
        if self.name=="drawLine":
            a.line(self.args[0:4],fill=tuple(self.args[4:]))
        elif self.name=="drawPoint":
            a.point(self.args[0:2],fill=tuple(self.args[2:]))
        elif self.name=="drawCircle":
            x=(self.args[0]-self.args[2],self.args[1]-self.args[2])
            y=(self.args[0]+self.args[2],self.args[1]+self.args[2])
            a.ellipse([x,y],fill=tuple(self.args[3:]))
        elif self.name=="drawEllipse":
            a.ellipse(self.args[0:4],fill=tuple(self.args[4:]))



def argeval(r,main_args,args):
    for j in range(0,len(args)):
        r=r.replace(args[j],str(main_args[j]))
    r=eval(r)
    return(r)


def recfunc(args,main_args,bex,rex,funcs):
    k=rex["recursive value name"]
    rex=rex["expression"]
    r=func(main_args,args,bex,funcs)
    r=str(r)
    r=argeval(r,main_args,args)
    main_args.append(r)
    args.append(k)
    for i in range(1,main_args[-2]+1):
        main_args[-2]=i
        x=func(main_args,args,rex,funcs)
        x=str(x)
        x=argeval(x,main_args,args)
        main_args[-1]=x
    return(x)


def func(main_args,args,ex,funcs):
    #l=2**5000000
    #h=2**8000000
    op=['+','-','/','*','%']
    names=["drawLine","drawPoint","drawCircle","drawEllipse"]
    if type(ex)==dict:
        if ex["type"]=="function call":
            if ex["function name"] in names:
                ex_args=copy.deepcopy(ex["args"])
                for k in range(len(ex_args)):
                    if type(ex_args[k])==dict:
                        r=func(main_args,args,ex_args[k],funcs)
                        if type(r)==str:
                            for j in range(0,len(args)):
                                r=r.replace(args[j],str(main_args[j]))
                            r=eval(r)
                        ex_args[k]=r
                k=0
                while k<len(ex_args):
                    if ex_args[k] in args:
                        x=args.index(ex_args[k])
                        ex_args[k]=main_args[x]
                    k=k+1
                c=pillow(main_args,ex_args,ex["function name"])
                c.draw()
                return(0)        
            elif ex["function name"]=="if":
                ex_args=ex["args"]
                r=func(main_args,args,ex_args[0],funcs)
                r=argeval(r,main_args,args)
                if r==0:
                    ex_args[2]
                    r=func(main_args,args,ex_args[2],funcs)
                    r=argeval(r,main_args,args)
                    return(r)
                else:
                    ex_args[1]
                    r=func(main_args,args,ex_args[1],funcs)
                    r=argeval(r,main_args,args)
                    return(r)
            else:
                name=ex["function name"]
                for i in funcs:
                    if name==i["function name"]:
                        ex_args=copy.deepcopy(ex["args"])
                        for k in range(len(ex_args)):
                            if type(ex_args[k])==dict:
                                r=func(main_args,args,ex_args[k],funcs)
                                if type(r)==str:
                                    for j in range(0,len(args)):
                                        r=r.replace(args[j],str(main_args[j]))
                                    r=eval(r)
                                ex_args[k]=r
                        k=0
                        while k<len(ex_args):
                            if ex_args[k] in args:
                                x=args.index(ex_args[k])
                                ex_args[k]=main_args[x]
                            k=k+1
                        if i["type"]=="function definition":
                            args=i["args"]
                            ex=i["expression"]
                            r=func(ex_args,args,ex,funcs)
                        else:
                            args=i["args"]
                            args.append(i["recursive arg"])
                            bex=i["base expression"]
                            rex=i["recursive expression"]
                            r=recfunc(args,main_args,bex,rex,funcs)
                        for i in range(0,len(args)):
                            r=r.replace(args[i],str(ex_args[i]))
                        r=eval(r)
                        return(r)
        else:
            if type(ex["A"])==dict:
                x=str(func(main_args,args,ex["A"],funcs))
                r=x+ex["type"]
                if type(ex["B"])==dict:
                    x=str(func(main_args,args,ex["B"],funcs))
                    r=r+x
                else:
                    r=r+str(ex["B"])
            else:
                
                r=str(ex["A"])+ex["type"]
                if type(ex["B"])==dict:
                    x=str(func(main_args,args,ex["B"],funcs))
                    r=r+x
                else:
                    
                    r=r+str(ex["B"])
            return(r)

    else:
        return ex
    

def opn():
    jsn=open("client.json")
    jsn=jsn.read()
    jsn=json.loads(jsn)
    return(jsn)

def main_ex(ex,ex_list):
    print(ex)
    op=['+','-','*','/','%']
    if ex["type"]=="function call":
        ex_list.append(ex)
        return(ex_list)
    else:
        ex_list.append(ex["A"])
        if ex["B"]["type"] in op:
            main_ex(ex["B"])
        else:
            ex_list.append(ex["B"])
        return(ex_list)
def mains():
    jsn=opn()
    ht=jsn["height"]
    wi=jsn["width"]
    img=Image.new("RGB",(wi,ht),(200,200,200))
    pillow.img=img
    pillow.ht=ht
    pillow.wi=wi
    funcs=jsn["functions"]
    for i in funcs:
        if i["function name"]=="main":
            main=i
            funcs.remove(i)
    ex=main["expression"]
    ex_list=main_ex(ex,[])
    for i in ex_list:
        name=i['function name']
        main_args=i['args']
        for j in funcs:
            if j["function name"]==name:
                if j["type"]=="function definition":
                    args=j["args"]
                    ex=j["expression"]
                    r=func(main_args,args,ex,funcs)
                else:
                    args=j["args"]
                    args.append(j["recursive arg"])
                    bex=j["base expression"]
                    rex=j["recursive expression"]
                    recfunc(args,main_args,bex,rex,funcs)
    pillow.img.save("image.jpg")

if __name__=='__main__':
    mains()
    pillow.img.save("image.jpg")
