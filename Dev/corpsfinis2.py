#!/usr/bin/python
# coding: utf-8

from __future__ import division, print_function

def defzn(modulo):
  class zn:
    def __init__(self,n):
      if isinstance(n,zn):
        self.val=n.val%modulo
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
    def __ne__(self,n):
      n=zn(n)
      if self.val==n.val:
        return 0
      return 1
    def __add__(self,n):
      n=zn(n)
      s=self.val+n.val
      s%=modulo
      return zn(s)
    def __radd__(self,n):
      return self+n
    def __neg__(self):
      op=(-self.val)%modulo
      return zn(op%modulo)
    def __sub__(self,n):
      return self+(-n)
    def __rsub__(self,n):
      return n-self
    def __mul__(self,n):
      if isinstance(n,int):
        if n>=0:
          somme=zn(0)
          for _ in range(n):
            somme+=self
          return somme
        else:
          return -self*(-n)
      n=zn(n)
      p=self.val*n.val%modulo
      return zn(p)
    def __rmul__(self,n):
      return self*n
    def __truediv__(self,d):
      d=zn(d)
      if d.val==0:
        raise ZeroDivisionError
      def bezout(n,a): # a<n au=1 [n]
        r,u,v,rr,uu,vv=a,1,0,n,0,1
        while rr!=0:
          q=r//rr
          r,u,v,rr,uu,vv=rr,uu,vv,r-q*rr,u-q*uu,v-q*vv
        return u%n
      q=bezout(modulo,d.val)
      if (q*d.val)%modulo==1:
        return zn(q)*self
      else:
        raise ZeroDivisionError
    def __rtruediv__(self,n):
      return n/self
    def __pow__(self,e):
      if isinstance(e,int):
        if e>=0:
          p=zn(1)
          x=zn(self)
          while e>1:
            if e%2:
              p*=x
            x*=x
            e//=2
          return p*x
        else:
          return zn(1)/self**-e
      raise TypeError
  return zn

def defpoly(classe):
  class polynome:
    def __init__(self,coef=[]):
#      print(classe)
      if isinstance(coef,(list,tuple)):
        if coef:
          self.coef=[classe(c) for c in coef]
        else:
          self.coef=[classe(0)]
      elif isinstance(coef,classe):
        self.coef=[coef]
      elif isinstance(coef,(int,float)):
        self.coef=[classe(coef)]
      elif isinstance(coef,polynome):
#        print(coef.coef)
#        print(isinstance(coef,polynome))
        self.coef=[classe(c) for c in coef.coef]
      else:
#        self.coef=[coef]
        raise TypeError
    def __str__(self):
      expo={"0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹"}
      def affcoef(e):
        co="X"
        if e=="0":
          co=""
        elif e=="1":
          pass
        else:
          for ec in str(e):
            co=co+expo[ec]
        return co
      ch=""
      for i in range(len(self)):
        c=self.coef[i]
        if isinstance(c,(int,float)):
          if c!=0:
            if c>0:
              ch=ch+"+"
            else:
              ch=ch+"-"
            e=str(len(self)-i-1)
            if c!=1 and c!=-1 or e=="0":
              ch=ch+str(abs(c))
            ch=ch+affcoef(e)
          elif c==0:
            pass
        elif "x" in str(c):
          ch=ch+"+("+str(c)+")"
          ch=ch+affcoef(str(len(self)-i-1))
        else:
          ch=ch+"+"+str(c)
          ch=ch+affcoef(str(len(self)-i-1))
      if ch:
        return ch[1:]
      return str(c)
    def __repr__(self):
      return str(self)
    def __call__(self,val):
      res=classe(0)
      for c in self.coef:
        res*=val
        res+=c
      return res
    def __len__(self):
      return len(self.coef)
    def __ne__(self,q):
      q=polynome(q.coef)
      return self.coef==q.coef
    def __add__(self,q):
      somme=polynome(self)
      if isinstance(q,classe):
        somme.coef[-1]+=q
        return somme
      elif isinstance(q,polynome):
        somme.coef=[classe(0)]*(max(len(self),len(q))-len(self))+somme.coef
        for i in range(len(q)):
          somme.coef[-i-1]+=q.coef[-1-i]
      else:
        raise TypeError
      somme.simp()
      return somme
    def __radd__(self,q):
      return self+q
    def __neg__(self):
      oppose=polynome(self)
      for i in range(len(self)):
        oppose.coef[i]*=classe(-1)
      return oppose
    def __sub__(self,q):
      return self+(-q)
    def __rsub__(self,q):
      return q-self
    def __mul__(self,q):
      if isinstance(q,int):
        if q>=0:
          somme=classe(0)
          for _ in range(q):
            somme+=self
          return somme
        else:
          return -self*(-q)
      q=polynome(q)
      p=polynome([classe(0) for _ in range(len(self)+len(q)-1)])
      for i in range(len(self)):
        for j in range(len(q)):
          p.coef[-i-j-1]+=q.coef[-j-1]*self.coef[-i-1]
      p.simp()
      return p
    def __rmul__(self,q):
      return self*q
    def __pow__(self,e):
      if isinstance(e,int) and e>=0:
        p=polynome(classe(1))
        x=polynome(self)
        while e>1:
          if e%2:
            p*=x
          x*=x
          e//=2
        return p*x
      raise TypeError
    def __divmod__(self,d):
      if isinstance(d,classe):
        q=polynome([classe(0)]*len(self))
        r=polynome([classe(0)]*len(self))
        for i in range(len(self)):
          q.coef[i],r.coef[i]=self.coef[i]/d
        q.simp()
        r.simp()
        return q,r
      d=polynome(d)
      q=polynome([])
      r=polynome(self)
      if d.coef==[classe(0)]:
        raise ZeroDivisionError
      while len(r)>=len(d):
        q.coef.append(r.coef[0]/d.coef[0])
        for i in range(len(d)):
          r.coef[i]-=d.coef[i]*q.coef[-1]
        del(r.coef[0])
      q.simp()
      r.simp()
      return q,r
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
        while self.coef[0]==classe(0):
          del(self.coef[0])
      except IndexError:
        self.coef=[0]
  return polynome

def defquotient(classe,polgen):
  class quotient(classe):
#    print(classe)
    def __init__(self,n):
      if isinstance(n,int):
        self.coef=[classe(n)]
      else:
        classe.__init__(self,n)
        temp=n%polgen
        self.coef=temp.coef
    def __str__(self):
      return classe.__str__(self).replace("X","x")
    def __add__(self,n):
#      som=quotient(classe.__add__(self,n)%polgen)
      return self.appl2(classe.__add__,n)
    def __radd__(self,n):
      return self.appl2(classe.__radd__,n)
    def __neg__(self):
      return self.appl1(classe.__neg__)
    def __sub__(self,n):
      return self.appl2(classe.__sub__,n)
    def __rsub__(self,n):
      return self.appl2(classe.__rsub__,n)
    def __mul__(self,n):
      if isinstance(n,int):
        if n>=0:
          somme=classe(0)
          for _ in range(n):
            somme+=self
          return somme
        else:
          return -self*(-n)
      else:
        return self.appl2(classe.__mul__,n)
    def __rmul__(self,n):
      return self.appl2(classe.__rmul__,n)
    def __pow__(self,n):
      return self.appl2(classe.__pow__,n)
    def __truediv__(self,d):
      zero=classe(0)
      if d==zero:
        raise ZeroDivisionError
      return self*d**(self.coef[0].modulo**(len(polgen)-1)-2)
    def __rtruediv__(self,q):
      return q/self
#    def simp(self):
#      self%=polgen
#      classe.simp(self)
#      poly=defpoly(defzn(car))
#      self%=poly(polgen)
    def appl2(self,methode,n):
      return quotient(methode(self,n)%polgen)
    def appl1(self,methode):
      return quotient(methode(self)%polgen)
  return quotient

z5=defzn(5)
#z=[z5(i) for i in range(5)]
#print(z,z[1]/z[2])
#z7=defzn(7)
#zz=[z7(i) for i in range(7)]
#print(zz,z)
#print(z7(0))
#print(z7(11)+zz[5])

#print(z5(1)==z5(1))
#poly=defpoly(z5)
#p=poly([z5(1),z5(1),z5(2)])
#q=poly([z5(-1),z5(3),z5(4)])
#print(p,q)
#s,r=divmod(p,q)
#print(s*q+r)

poly5=defpoly(z5)
polgen=poly5([z5(1),z5(1),z5(1)])
#print(polgen-polgen)
zp25=defquotient(poly5,polgen)
#print(zp25)
pol=poly5([z5(3),z5(2)])
n=zp25(pol)
qol=poly5([z5(1),z5(2)])
m=zp25(qol)
n2=m/n
print(n2,n,m,-m,n*m,m.coef[0].modulo)
polzp25=defpoly(zp25)
poll=polzp25([m,n,n2])
#print(2*poll)
#qoll=poll*poll
#print(qoll.coef)
