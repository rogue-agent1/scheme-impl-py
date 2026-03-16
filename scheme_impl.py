#!/usr/bin/env python3
"""Scheme interpreter — s-expression parsing and evaluation."""
import operator as op
def tokenize(s):return s.replace("("," ( ").replace(")"," ) ").split()
def parse(tokens):
    if not tokens:raise SyntaxError("Unexpected EOF")
    t=tokens.pop(0)
    if t=="(":
        L=[]
        while tokens[0]!=")":L.append(parse(tokens))
        tokens.pop(0);return L
    elif t==")":raise SyntaxError("Unexpected )")
    else:
        try:return int(t)
        except:
            try:return float(t)
            except:return t
def standard_env():
    env={"+":(lambda *a:sum(a)),"-":(lambda a,b=None:(-a if b is None else a-b)),
         "*":(lambda *a:eval("*".join(str(x) for x in a)) if len(a)>1 else a[0]),
         "/":(lambda a,b:a//b),">":(lambda a,b:a>b),"<":(lambda a,b:a<b),
         ">=":(lambda a,b:a>=b),"<=":(lambda a,b:a<=b),"=":(lambda a,b:a==b),
         "abs":abs,"max":max,"min":min,"not":(lambda x:not x),
         "list":(lambda *x:list(x)),"car":(lambda x:x[0]),"cdr":(lambda x:x[1:]),
         "cons":(lambda x,y:[x]+list(y)),"null?":(lambda x:x==[]),
         "number?":(lambda x:isinstance(x,(int,float))),"#t":True,"#f":False}
    return env
class Env(dict):
    def __init__(self,params=(),args=(),outer=None):
        self.update(zip(params,args));self.outer=outer
    def find(self,var):
        if var in self:return self
        if self.outer:return self.outer.find(var)
        raise NameError(var)
def eval_scheme(x,env):
    if isinstance(x,str):return env.find(x)[x]
    if not isinstance(x,list):return x
    if x[0]=="quote":return x[1]
    if x[0]=="if":
        _,test,conseq,*alt=x
        return eval_scheme(conseq if eval_scheme(test,env) else (alt[0] if alt else None),env)
    if x[0]=="define":
        _,var,expr=x;env[var]=eval_scheme(expr,env);return None
    if x[0]=="lambda":
        _,params,body=x
        return lambda *args:eval_scheme(body,Env(params,args,env))
    if x[0]=="begin":
        for expr in x[1:]:val=eval_scheme(expr,env)
        return val
    # Function call
    proc=eval_scheme(x[0],env);args=[eval_scheme(a,env) for a in x[1:]]
    return proc(*args)
def run(program):
    env=Env(outer=None);env.update(standard_env())
    tokens=tokenize(program);result=None
    while tokens:result=eval_scheme(parse(tokens),env)
    return result
def main():
    print(run("(+ 1 2 3)"))
    print(run("(define square (lambda (x) (* x x))) (square 5)"))
if __name__=="__main__":main()
