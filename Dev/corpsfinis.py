#!/usr/bin/python
# coding: utf-8

from __future__ import division, print_function
#from sys import exit,argv,stderr

class zn:
  def __init__(self,n,modulo=0):
    if isinstance(n,zn):
      self.val=n.val%n.modulo
      self.modulo=n.modulo
    elif not isinstance(modulo,int) or modulo<=0 or not isinstance(n,int):
      raise TypeError
    else:
      self.val=n%modulo
      self.modulo=modulo
  def __str__(self):
    ch=""
    for c in str(self.val):
      ch=ch+str(c)+chr(204)+chr(133)
    return ch
  def __repr__(self):
    return str(self)
#  def __cmp__(self,n):
#    n=zn(n,self.modulo)
#    if self.val==n.val:
#      return 0
#    return 1
  def __ne__(self,n):
    n=zn(n,self.modulo)
    if self.val==n.val:
      return 0
    return 1
  def __abs__(self):
    return self
  def __add__(self,n):
    n=zn(n,self.modulo)
    s=self.val+n.val
    s%=self.modulo
    return zn(s,self.modulo)
  def __radd__(self,n):
    return self+n
  def __neg__(self):
    op=-self.val%self.modulo
    return zn(op%self.modulo,self.modulo)
  def __sub__(self,n):
    return self+(-n)
  def __rsub__(self,n):
    return n-self
  def __mul__(self,n):
    n=zn(n,self.modulo)
    p=self.val*n.val%self.modulo
    return zn(p,self.modulo)
  def __rmul__(self,n):
    return self*n
  def __truediv__(self,d):
    d=zn(d,self.modulo)
    if d.val==0:
      raise ZeroDivisionError
    def bezout(n,a): # a<n au=1 [n]
      r,u,v,rr,uu,vv=a,1,0,n,0,1
      while rr!=0:
        q=r//rr
        r,u,v,rr,uu,vv=rr,uu,vv,r-q*rr,u-q*uu,v-q*vv
      return u%n
    q=bezout(self.modulo,d.val)
    if (q*d.val)%self.modulo==1:
      return zn(q,self.modulo)*self
    else:
      raise ZeroDivisionError
  def __rtruediv__(self,n):
    return n/self
  def __pow__(self,e):
    if isinstance(e,int):
      if e>=0:
        p=zn(1,self.modulo)
        x=zn(self)
        while e>1:
          if e%2:
            p*=x
          x*=x
          e//=2
        return p*x
      else:
        return zn(1,self.modulo)/self**-e
    raise TypeError

class polynome:
  """
  [1,-32,0,5] est X³-32X²+5
  """

  def __init__(self,coef=[]):#,modulo=0):
    if isinstance(coef,(list,tuple,fpn,zn)):
      if coef:
        self.coef=coef
      else:
        self.coef=[0]
    elif isinstance(coef,(int,float)):
      self.coef=[coef]
    elif isinstance(coef,polynome):
      self.coef=[c for c in coef.coef]
#      self.modulo=coef.modulo
    else:
      raise TypeError
#    self.modulo=modulo

  def __str__(self):
    expo={"0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹"}
    ch=""
    for i in range(len(self)):
      c=self.coef[i]
      if c!=0:
        try:
          if c>0:
            ch=ch+"+"
          else:
            ch=ch+"-"
        except TypeError:
          ch=ch+"+"
        e=str(len(self)-i-1)
        if c!=1 and not (c+1==0 and isinstance(c,(int,float))) or e=="0":
          ch=ch+str(abs(c))
        ch=ch+"X"
        if e=="0":
          ch=ch[:-1]
        elif e=="1":
          pass
        else:
          for c in str(len(self)-i-1):
            ch=ch+expo[c]
    if ch:
      return ch[1:]
    return "0"

  def __repr__(self):
    return str(self)

  def __call__(self,val):
    res=0
    for c in self.coef:
      res*=val
      res+=c
#    if self.modulo:
#      res%=self.modulo
    return res

  def __len__(self):
    return len(self.coef)

  def __ne__(self,q):
    q=polynome(q)
    return self.coef==q.coef
#    if self.coef==q.coef:# and self.modulo==q.modulo:
#      return True
#    return False

  def __add__(self,q):
    somme=polynome(self)#,self.modulo)
    if isinstance(q,int):
      somme.coef[-1]+=q
      return somme
    elif isinstance(q,polynome):
#      if self.modulo!=q.modulo:
#        raise ValueError("Les modulos doivent être égaux.")
      somme.coef=[0]*(max(len(self),len(q))-len(self))+somme.coef
      for i in range(len(q)):
        somme.coef[-i-1]+=q.coef[-1-i]
    else:
      raise TypeError
#    if self.modulo:
#      for i in range(len(self)):
#        somme.coef[i]%=self.modulo
    somme.simp()
    return somme

  def __radd__(self,q):
    return self+q

  def __neg__(self):
    oppose=polynome(self)
    for i in range(len(self)):
      oppose.coef[i]*=-1
#    if self.modulo:
#      for i in range(len(self)):
#        oppose.coef[i]%=self.modulo
    return oppose

  def __sub__(self,q):
    return self+(-q)

  def __rsub__(self,q):
    return q-self

  def __mul__(self,q):
#    if isinstance(q,polynome) and self.modulo!=q.modulo:
#      raise TypeError
    q=polynome(q)
    p=polynome([0]*(len(self)+len(q)-1))
#    p.modulo=self.modulo
    for i in range(len(self)):
      for j in range(len(q)):
        p.coef[-i-j-1]+=q.coef[-j-1]*self.coef[-i-1]
#    if self.modulo:
#      for i in range(len(self)):
#        p.coef[i]%=self.modulo
    p.simp()
    return p

  def __rmul__(self,q):
    return self*q

  def __pow__(self,e):
    if isinstance(e,int) and e>=0:
      p=polynome(1)
      x=polynome(self)
      while e>1:
        if e%2:
          p*=x
        x*=x
        e//=2
      return p*x
    raise TypeError

  def __divmod__(self,d):
#    def bezout(n,a): # a<n au=1 [n]
#      r,u,v,rr,uu,vv=a,1,0,n,0,1
#      while rr!=0:
#        q=r//rr
#        r,u,v,rr,uu,vv=rr,uu,vv,r-q*rr,u-q*uu,v-q*vv
#      return u%n
    if isinstance(d,zn):
      q=polynome([0]*len(self))
      r=polynome([0]*len(self))
      for i in range(len(self)):
        q.coef[i],r.coef[i]=self.coef[i]/d
      q.simp()
      r.simp()
      return q,r
#    if isinstance(d,int):
#      q=polynome([0]*len(self),self.modulo)
#      r=polynome([0]*len(self),self.modulo)
#      for i in range(len(self)):
#        q.coef[i],r.coef[i]=divmod(self.coef[i],d)
#      q.simp()
#      r.simp()
#      return q,r
    d=polynome(d)#,self.modulo)
    q=polynome([])#,self.modulo)
    pp=polynome(self)#,self.modulo)
    if d.coef==[0]:
      raise ZeroDivisionError
#    if self.modulo:
#      div=bezout(self.modulo,d.coef[0])
#    else:
#    div=d.coef[0]**-1
    while len(pp)>=len(d):
#      try:
#        q.coef.append(pp.coef[0]*div%self.modulo)
#      except ZeroDivisionError:
      q.coef.append(pp.coef[0]/d.coef[0])#*div)
      for i in range(len(d)):
        pp.coef[i]-=d.coef[i]*q.coef[-1]
#        try:
#          pp.coef[i]%=self.modulo
#        except ZeroDivisionError:
#          pass
      del(pp.coef[0])
    q.simp()
    pp.simp()
    return q,pp

  def __rdivmod__(self,p):
    q,r=divmod(p,self)
    return q,r

  def __floordiv__(self,d):
    q,_=divmod(self,d)
    return q

  def __rfloordiv__(self,p):
    q,_=divmod(p,self)
    return q

  def __mod__(self,d):
    _,r=divmod(self,d)
    return r

  def __rmod__(self,q):
    _,r=divmod(q,self)
    return r

  def simp(self):
    try:
      while self.coef[0]==0:
        del(self.coef[0])
    except IndexError:
      self.coef=[0]

class fpn():
  def __init__(self,poly,car,polgen):
    self.poly=polynome(poly)
    self.car=car
    self.polgen=polgen
  def __str__(self):
    return "("+str(self.poly).replace("X","x")+")"
  def __repr__(self):
    return str(self)
  def __len__(self):
    return len(self.poly)
  def __ne__(self,n):
    return n.poly.coef==self.poly.coef
#      print("Faux")
#      return False
#    print("Vrai")
#    return True
  def __add__(self,n):
    somme=fpn(self.poly,self.car,self.polgen)
    somme.poly+=n.poly
    somme.poly%=self.polgen
    return somme
  def __radd__(self,n):
    return n+self
  def __neg__(self):
    opp=fpn(self.poly,self.car,self.polgen)
    for i in range(len(self)):
      opp.poly.coef[i]*=-1
    return opp
  def __sub__(self,n):
    return self+(-n)
  def __rsub__(self,n):
    return n-self
  def __mul__(self,n):
    prod=fpn(self.poly,self.car,self.polgen)
    prod.poly*=n.poly
    prod.poly%=self.polgen
    return prod
  def __rmul__(self,n):
    return n*self
  def __pow__(self,e):
    puis=fpn(self.poly,self.car,self.polgen)
    if e>=0:
      puis.poly=puis.poly**e
    else:
      puis=fpn(polynome([zn(1,self.car)]),self.car,self.polgen)
      puis.poly=puis.poly**-e
    puis.poly%=self.polgen
    return puis
  def __truediv__(self,d):
#    if d==fpn(polynome([zn(0,self.car)]),self.car,self.polgen):
#      raise ZeroDivisionError
#    print(d)
    quot=fpn(self.poly,self.car,self.polgen)
    mul=d.poly**(self.car**len(self)-2)
    mul%=self.polgen
    quot.poly*=mul
    quot.poly%=self.polgen
#    print(d*quot,self)
    if d*quot!=self:
      raise ZeroDivisionError
    return quot
  def __rtruediv__(self,n):
    return n/self

#p=polynome([1,1,-1,1,1])
#print(p==p)
#q=polynome([1,0,0])
#print(p%5)
#print(p(2))
#print(p*polynome([1,2]))
#print(q(p))
#print(polynome([1,-1])**12)
#print(p==polynome([1,0]))
#s,r=divmod(p,q)
#print(p)
#print(p//q,s,r)
#print(s*q+r)
#p=polynome([1,7,-1])
#print(p**3)
mod=11
z=[zn(i,mod) for i in range(mod)]
#print(z)
#a=zn(5,11)
#b=zn(7,11)
#print(a**2)
#p=polynome([a,b,z[1],z[0]])
#print(p**2,p)
#q=polynome([z[1]]+[z[0]]*9+[z[10],z[0]])
#print([q(z[i]) for i in range(mod)],q)
#print(q,q.coef)
#c=zn(0,11)
#print(0==c)
polgen=polynome([1,1,1])
#print([polgen(i) for i in z])
nb1=fpn(polynome([z[2],z[3]]),mod,polgen)
nb2=fpn(polynome([z[3],z[1]]),mod,polgen)
nb3=nb1+nb2
print(nb1,nb2)
print((nb2*nb1)==(nb1*nb2))
q=nb1/nb2
print(q,q*nb2)
zero=fpn(polynome([z[0]]),mod,polgen)
#print(zero)
#print(nb1/zero)
