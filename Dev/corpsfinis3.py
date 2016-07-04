#!/usr/bin/python3

from qrcodeoutils import *

class ElementAnneau(object):
  def __radd__(self,autre):
    return self+autre
  def __rsub__(self,autre):
    return -self+autre
  def __rmul__(self,autre):
    return self*autre

class ElementCorps(ElementAnneau):
  def __truediv__(self,autre):
    return self*autre._inverse()
  def __rtruediv__(self,other):
    return self._inverse()*autre
  def __div__(self,autre):
    return self.__truediv__(autre)
  def __rdiv__(self,autre):
    return self.__rtruediv__(autre)

@memorise
def defzn(p):
#  operatorPrecedence=3
  class Zn(ElementCorps):
    def __init__(self,n):
      if isinstance(n,Zn):
        self.n=n.n
      else:
        self.n=n%p
      self.corps=Zn
    def __add__(self,m):
      return Zn(self.n+m.n)
    def __sub__(self,m):
      return Zn(self.n-m.n)
    def __mul__(self,m):
      return Zn(self.n*m.n)
    def __truediv__(self,m):
      return self*m._inverse()
#    def __divmod__(self,m):
#      return self/m,Zn(0)
    def __neg__(self):
      return Zn(-self.n)
    def __eq__(self,m):
      return isinstance(m,Zn) and self.n==m.n
    def __pow__(self,exp):
      if exp>0:
        prod=1
        x=self.n
        while exp>1:
          if exp%2:
            prod*=x
          x*=x
          x%=p
          exp//=2
        return Zn(prod*x)
      elif exp==0:
        return Zn(1)
      else:
        return self._inverse()**-exp
#    def __abs__(self): return abs(self.n)
    def __str__(self):
#      return hex(self.n)[2:]
      return str(self.n)+"\u0305"#chr(773)
    def __repr__(self):
#      return str(self)
      return "%d [mod %d]"%(self.n,self.p)

    def _inverse(self):
      return Zn(bezout(p,self.n))

  Zn.p=p
  Zn.__name__="ℤ/%dℤ"%p
  return Zn

#def veriftype(f):
#  def nouvfonct(self,autre):
#    if (hasattr(autre.__class__,'priorite') and autre.__class__.operatorPrecedence>self.__class__.operatorPrecedence):
#      return NotImplemented

#    if type(self) is not type(autre):
#      try:
#        autre=self.__class__(autre)
#      except TypeError:
#        try:
#          autre=autre.__class__(self)
#        except TypeError:
#          message='Pas d’isomorphisme entre %s de type %s vers le type %s dans la fonction %s'
#          raise TypeError(message%(autre,type(autre).__name__,type(self).__name__,f.__name__))
#      except Exception as e:
#        message='Erreur de type dans les arguments %r et %r pour la fonction %s. Raison:%s'
#        raise TypeError(message%(self,autre,f.__name__,type(autre).__name__,type(self).__name__,e))

#    return f(self,autre)

#  return nouvfonct

@memorise
def defpolynome(corps):

  class Polynome(ElementAnneau):
    operatorPrecedence=2
    construction=lambda L: Polynome([corps(x) for x in L])

    def __init__(self,c):
      if type(c) is Polynome:
        self.coefficients=c.coefficients
      elif isinstance(c,corps):
        self.coefficients=[c]
      elif not hasattr(c,'__iter__') and not hasattr(c,'iter'):
        self.coefficients=[corps(c)]
      else:
        self.coefficients=c

      try:
        while self.coefficients[0]==corps(0):
          del self.coefficients[0]
      except IndexError:
        pass

    def estzero(self):
      return self.coefficients==[]

    def __str__(self):
      if self.estzero():
        return "0"
      expo={"0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹"}
      return "+".join([str(self[-1-i])+"X"+"".join(expo[j] for j in str(self.degre()-i)) for i in range(len(self)) if self[-1-i]!=self.corps(0)])

    def __repr__(self):
      try:
        return str(self)+" [mod %d]"%(corps.p)
      except TypeError:
        return str(self)

    def __call__(self,val):
      if type(val) is type(self):
        res=Polynome([])
      else:
        res=self.corps(0)
      for c in self:
        res*=val
        res+=c
      return res
    def __abs__(self):
      return len(self.coefficients)
    def __len__(self):
      return len(self.coefficients)
    def __sub__(self,autre):
      return self+(-autre)
    def __iter__(self):
      return iter(self.coefficients)
    def __neg__(self):
      return Polynome([-a for a in self])
    def __pow__(self,exp):
      if exp>0:
        prod=Polynome([self.corps(1)])
        x=Polynome(self)
        while exp>1:
          if exp%2:
            prod*=x
          x*=x
          exp//=2
        return prod*x
      elif exp==0:
        return Polynome([self.corps(1)])

    def iter(self):
      return self.__iter__()
    def coefficientdominant(self):
      return self.coefficients[0]
    def __getitem__(self,i):
      return self.coefficients[-i-1]
    def __setitem__(self,i,x):
      self.coefficients[-i-1]=x
    def degre(self):
      return abs(self)-1

    @veriftype
    def __eq__(self,autre):
      return self.degre()==autre.degre() and self.coefficients==autre.coefficients#all([x==y for (x,y) in zip(self,autre)])

    @veriftype
    def __add__(self,autre):
      somme=[self.corps(0)]*(max(len(self),len(autre))-len(self))+self.coefficients
      for i in range(len(autre)):
        somme[-i-1]+=autre[i]
      return Polynome(somme)
    @veriftype
    def __radd__(self,autre):
      return self+autre
    @veriftype
    def __mul__(self,autre):
      if self.estzero() or autre.estzero():
        return Polynome([])
      prod=[self.corps(0) for _ in range(len(self)+len(autre)-1)]
      for i in range(len(self)):
        for j in range(len(autre)):
          prod[-i-j-1]+=autre[j]*self[i]
      return Polynome(prod)
#    @veriftype
#    def __rmul__(self,autre):
#      return self*autre

    @veriftype
    def __divmod__(self,diviseur):
      quotient,reste=Polynome([]),self
      degdiviseur=diviseur.degre()
      coefdomdiv=diviseur.coefficientdominant()
      while reste.degre()>=degdiviseur:
        niveau=reste.degre()-degdiviseur
        zeros=[self.corps(0) for _ in range(niveau)]
        monomediviseur=Polynome([reste.coefficientdominant()/coefdomdiv]+zeros)
        quotient+=monomediviseur
        reste-=monomediviseur*diviseur
      return quotient,reste

    def __floordiv__(self,div):
      q,_=divmod(self,div)
      return q
    def __mod__(self,div):
      _,r=divmod(self,div)
      return r

  Polynome.corps=corps
  Polynome.__name__="(%s)[x]"%corps.__name__
  return Polynome

@memorise
def deffq(p,m,polyann=None):
  Zp=defzn(p)
  if m==1:
    return Zp

  Polynome=defpolynome(Zp)
  if polyann is None:
    raise NotImplementedError
  else:
    polyannulateur=Polynome.construction(polyann)
#    annulateur=creepolyirred(p,m)

  class Fq(ElementCorps):
    cardinal=int(p**m)
    corps=Zp
    operatorPrecedence=3
    annulateur=polyannulateur

    def __init__(self,polynome):
      if type(polynome) is Fq:
        self.polynome=polynome.polynome
      elif type(polynome) is int or type(polynome) is Zp:
        self.polynome=Polynome([Zp(polynome)])
      elif isinstance(polynome,Polynome):
        self.polynome=polynome%polyannulateur
      else:
        self.polynome=Polynome([Zp(x) for x in polynome])%polyannulateur

      self.corps=Fq

    @veriftype
    def __add__(self,autre):
      return Fq(self.polynome+autre.polynome)
    @veriftype
    def __sub__(self,autre):
      return Fq(self.polynome-autre.polynome)
    @veriftype
    def __mul__(self,autre):
      return Fq(self.polynome*autre.polynome)
#    @veriftype
    def __eq__(self,autre):
      return isinstance(autre,Fq) and self.polynome==autre.polynome

    def __pow__(self,n):
      return Fq(pow(self.polynome,n))
    def __neg__(self):
      return Fq(-self.polynome)
#    def __abs__(self):
#      return abs(self.polynome)
    def __str__(self):
      return "("+repr(self.polynome).replace("X","x")+")"
    def __repr__(self):
      return repr(self.polynome)+" \u2208 "+self.__class__.__name__

#    @veriftype
#    def __divmod__(self,diviseur):
#      q,r=divmod(self.polynome,diviseur.polynome)
#      return (Fq(q),Fq(r))

    def _inverse(self):
      if self==Fq(0):
        raise ZeroDivisionError

      x,_,d=algoeuclideetendu(self.polynome,polyannulateur)
      return Fq(x)*Fq(d.coefficients[0]._inverse())

    @veriftype
    def __truediv__(self,autre):
      return self*autre._inverse()

  Fq.__name__="𝔽_{%d^%d}"%(p,m)
  return Fq


if __name__=="__main__":
  #mod7=defzn(7)
  #print([mod7(i) for i in range(10)])
  #print(mod7(3)**-2)
  #poly=defpolynome(mod7).construction
  #p=poly([1,5,0,2])
  #q=poly([1,1])
  #print(p+q)
  #print(q)
  #print(p//q,p%q)
  #print(q(mod7(2)))
  #print(poly([4])*q)
  #print(mod7(2)*mod7(4)-mod7(5))
  #print(mod7(1).corps.__name__)
  #z7=defzn(7)
  #print(mod7.__name__)
  #print(z7==mod7)
  F256=deffq(2,8,(1,0,0,0,1,1,1,0,1))
  x=F256([1,1,1,1,0,0])
  y=F256([1,1])
  print(x**15)
  print(x/y)
  polF256=defpolynome(F256).construction
  z=polF256([x,y,F256([0]),F256([1,1])])
  print((z**2+z)//z)
  print(z[2],z.coefficients[2])
  message="40d2754776173206272696c6c69670ec"
  correction="bc2a90136bafeffd4be0"
  polynome=[]
  for i in range(len(message)//2):
    polynome=polynome+[[int(j) for j in bin(eval("0x"+message[2*i:2*i+2]))[2:]]]
  polynome=polF256(polynome+[0]*(len(correction)//2))
  print(polynome)
  modulo=polF256([1])
  c=1
  for i in range(len(correction)//2):
    modulo*=polF256([[1],[int(j) for j in bin(c)[2:]]])
#    print(c,bin(c)[2:])
    c*=2
    if c>255:
      c^=285
  print(modulo)
  reste=polynome%modulo
  print(reste)
#  print(reste[0])
#  for i in reste.coefficients[0].polynome.coefficients:
#    print(str(i)[0])
  ch=""
  for s in reste.coefficients:
    nb=[]
    for c in s.polynome.coefficients:
      nb.append(int(str(c)[0]))
    ch=ch+hex(bin2dec(nb))[2:]
#      print(c,end="")
#    print()
#    print(s)
  print(ch)
#  print(''.join(hex(bin2dec([int(j) for j in 
#  print(''.join(hex(bin2dec(i.polynome.coefficients))[2:] for i in reste.coefficients))
