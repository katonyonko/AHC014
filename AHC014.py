import io
import re
import sys

_INPUT = """\
6
33 58
13 24
14 24
15 24
16 24
17 24
12 23
18 23
11 22
19 22
10 21
20 21
9 20
21 20
8 19
15 19
18 19
22 19
8 18
12 18
15 18
18 18
22 18
8 17
12 17
15 17
18 17
22 17
8 16
12 16
15 16
18 16
22 16
8 15
12 15
15 15
18 15
22 15
9 14
12 14
15 14
18 14
21 14
10 13
12 13
15 13
18 13
20 13
22 13
11 12
12 12
15 12
18 12
19 12
23 12
12 11
15 11
18 11
24 11
"""
sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  from random import randint,randrange
  from heapq import heappop, heappush
  import time
  class RectJoin():
    def __init__(self, N):
      self.N = N
      self.ans=[]
      self.best_score=0

    def Set(self,Weight):
      #縦に置いてある石から四角形を探す
      for i in range(self.N):
        now=0
        while now<self.N and self.banmen[i*self.N+now]>=0: now+=1
        next=now+1
        while next<self.N:
          while next<N and self.banmen[i*self.N+next]>=0: next+=1
          if next<self.N:
            self.FindRect(i,now,i,next,Weight)
          now,next=next,next+1
      #左上から右下に向けて置いてある石から四角形を探す
      for i in range(1,2*self.N-2):
        now=0
        while max(0,i-self.N+1)<=now<=min(self.N-1,i) and self.banmen[(i-now)*self.N+now]>=0: now+=1
        next=now+1
        while max(0,i-self.N+1)<=next<=min(self.N-1,i):
          while max(0,i-self.N+1)<=next<=min(self.N-1,i) and self.banmen[(i-next)*self.N+next]>=0: next+=1
          if next<=i:
            self.FindRect(i-now,now,i-next,next,Weight)
          now,next=next,next+1

    def bi(self,i,j,k):
      if k==0: return i*(self.N-1)+j
      elif k==1: return self.N**2-self.N-1+self.N*i+j
      elif k==2: return self.N*(self.N-1)*2+(self.N-1)*i+j
      else: return self.N*(self.N-1)*2+(self.N-1)**2+(self.N-1)*i+j

    def FindRect(self,i,j,k,l,Weight):
      """
      与えた点(i,j)と(k,l)を通る四角形を作れるかを判定し、作れる場合はそれをkouhoに追加し、banmenを更新する関数
      """
      d=max(abs(i-k),abs(j-l))
      #縦
      if i==k: dir=[(1,0),(-1,0)]; y=0; z=1
      #横
      elif j==l: dir=[(0,1),(0,-1)]; y=1; z=0
      #左下から右上
      elif i-j==k-l: dir=[(-1,1),(1,-1)]; y=2; z=3
      #左上から右下
      elif i+j==k+l: dir=[(1,1),(-1,-1)]; y=3; z=2
      for _ in range(2):
        q,r=dir[_]
        m,n,o,p=i+q,j+r,k+q,l+r
        OK=True
        while 0<=m<self.N and 0<=n<self.N and 0<=o<self.N and 0<=p<self.N:
          if self.banmen[m*N+n]<0 and self.banmen[o*self.N+p]<0: OK=False; break
          elif self.banmen2[self.bi(min(i,m),min(j,n),z)]==1 or self.banmen2[self.bi(min(k,o),min(l,p),z)]==1: OK=False; break
          elif self.banmen[m*self.N+n]>=0 and self.banmen[o*self.N+p]>=0: m,n,o,p=m+q,n+r,o+q,p+r
          else: break
        if 0<=m<self.N and 0<=n<self.N and 0<=o<self.N and 0<=p<self.N:
          for s in range(d):
            if self.banmen2[self.bi(min(i+s*(k-i)//d,i+(s+1)*(k-i)//d),min(j+s*(l-j)//d,j+(s+1)*(l-j)//d),y)]==1 or self.banmen2[self.bi(min(m+s*(k-i)//d,m+(s+1)*(k-i)//d),min(n+s*(l-j)//d,n+(s+1)*(l-j)//d),y)]==1: OK=False; break
          if OK==False: continue
          flg=True
          for s in range(d-1):
            if self.banmen[(m+(s+1)*(k-i)//d)*self.N+n+(s+1)*(l-j)//d]<0: flg=False
          if flg==True:
            e=max(abs(i-m),abs(j-n))
            if self.banmen[m*self.N+n]<0:
              heappush(self.kouho,(self.banmen[o*self.N+p],Weight(o,p,k,l,m,n),o,p,k,l,i,j,m,n))
            else:
              heappush(self.kouho,(self.banmen[m*self.N+n],Weight(m,n,o,p,i,j),m,n,o,p,k,l,i,j))
            for s in range(d-1):
              if self.banmen[(i+(s+1)*(k-i)//d)*self.N+j+(s+1)*(l-j)//d]>=0: self.banmen[(i+(s+1)*(k-i)//d)*self.N+j+(s+1)*(l-j)//d]+=1
              if self.banmen[(m+(s+1)*(k-i)//d)*self.N+n+(s+1)*(l-j)//d]>=0: self.banmen[(m+(s+1)*(k-i)//d)*self.N+n+(s+1)*(l-j)//d]+=1
            for t in range(e-1):
              if self.banmen[(i+(t+1)*(m-i)//e)*self.N+j+(t+1)*(n-j)//e]>=0: self.banmen[(i+(t+1)*(m-i)//e)*self.N+j+(t+1)*(n-j)//e]+=1
              if self.banmen[(k+(t+1)*(m-i)//e)*self.N+l+(t+1)*(n-j)//e]>=0: self.banmen[(k+(t+1)*(m-i)//e)*self.N+l+(t+1)*(n-j)//e]+=1

    #四角形を作れる４点になっているかを確認する関数（間に石の置かれた点がないかを確認する）
    def MakeRect(self,i,j,k,l,m,n):
      res=True
      d,e=max(abs(i-k),abs(j-l)),max(abs(i-m),abs(j-n))
      for s in range(d-1):
        if self.banmen[(i+(s+1)*(k-i)//d)*self.N+j+(s+1)*(l-j)//d]==-1: res=False
        if self.banmen[(m+(s+1)*(k-i)//d)*self.N+n+(s+1)*(l-j)//d]==-1: res=False
      for t in range(e-1):
        if self.banmen[(i+(t+1)*(m-i)//e)*self.N+j+(t+1)*(n-j)//e]==-1: res=False
        if self.banmen[(k+(t+1)*(m-i)//e)*self.N+l+(t+1)*(n-j)//e]==-1: res=False
      p=0 if i==k else 1 if j==l else 2 if i-j==k-l else 3
      q=0 if i==m else 1 if j==n else 2 if i-j==m-n else 3
      for s in range(d):
        if self.banmen2[self.bi(min(i+s*(k-i)//d,i+(s+1)*(k-i)//d),min(j+s*(l-j)//d,j+(s+1)*(l-j)//d),p)]==1: res=False
        if self.banmen2[self.bi(min(m+s*(k-i)//d,m+(s+1)*(k-i)//d),min(n+s*(l-j)//d,n+(s+1)*(l-j)//d),p)]==1: res=False
      for t in range(e):
        if self.banmen2[self.bi(min(i+t*(m-i)//e,i+(t+1)*(m-i)//e),min(j+t*(n-j)//e,j+(t+1)*(n-j)//e),q)]==1: res=False
        if self.banmen2[self.bi(min(k+t*(m-i)//e,k+(t+1)*(m-i)//e),min(l+t*(n-j)//e,l+(t+1)*(n-j)//e),q)]==1: res=False
      return res

    #四角形を作れる４点について盤面を更新する関数
    def MakeRect2(self,i,j,k,l,m,n):
      d,e=max(abs(i-k),abs(j-l)),max(abs(i-m),abs(j-n))
      p=0 if i==k else 1 if j==l else 2 if i-j==k-l else 3
      q=0 if i==m else 1 if j==n else 2 if i-j==m-n else 3
      for s in range(d):
        self.banmen2[self.bi(min(i+s*(k-i)//d,i+(s+1)*(k-i)//d),min(j+s*(l-j)//d,j+(s+1)*(l-j)//d),p)]=1
        self.banmen2[self.bi(min(m+s*(k-i)//d,m+(s+1)*(k-i)//d),min(n+s*(l-j)//d,n+(s+1)*(l-j)//d),p)]=1
      for t in range(e):
        self.banmen2[self.bi(min(i+t*(m-i)//e,i+(t+1)*(m-i)//e),min(j+t*(n-j)//e,j+(t+1)*(n-j)//e),q)]=1
        self.banmen2[self.bi(min(k+t*(m-i)//e,k+(t+1)*(m-i)//e),min(l+t*(n-j)//e,l+(t+1)*(n-j)//e),q)]=1

    #与えられたweightに基づいてRectJoinを解く関数
    def Solve(self,Weight,banmen,banmen2):
      self.banmen = banmen.copy()
      self.banmen2=banmen2.copy()
      self.kouho=[]
      self.output=[]
      self.Set(Weight)
      #候補から別のパスの途上にない点で中心から一番遠くにあるものを取り出し、答えに追加していく
      while self.kouho:
        b,w,i,j,k,l,m,n,o,p=heappop(self.kouho)
        if self.banmen[i*self.N+j]==b:
          #まず四角形を作れるか確認し、作れるならoutputに追加してkouhoと盤面を更新
          if self.MakeRect(i,j,k,l,o,p)==True and self.banmen[i*self.N+j]>=0:
            self.output.append((i,j,k,l,m,n,o,p))
            for ii,jj in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]:
              ti,tj=i+ii,j+jj
              while 0<=ti<self.N and 0<=tj<self.N and self.banmen[ti*self.N+tj]>=0: ti,tj=ti+ii,tj+jj
              if 0<=ti<self.N and 0<=tj<self.N: self.FindRect(i,j,ti,tj,Weight)
            self.banmen[i*self.N+j]=-1
            self.MakeRect2(i,j,k,l,o,p)
            self.Dec(i,j,k,l,o,p)
        else:
          if self.MakeRect(i,j,k,l,o,p)==True and self.banmen[i*self.N+j]>=0:
            heappush(self.kouho,(self.banmen[i*self.N+j],w,i,j,k,l,m,n,o,p))
          else:
            self.Dec(i,j,k,l,o,p)
      if self.score(self.output)>self.best_score:
        self.ans=self.output
        self.best_score=self.score(self.output)
        self.Weight=Weight

    #４点の間の石の置いていないところについてbanmenの数字を１減らす関数
    def Dec(self,i,j,k,l,m,n):
      d,e=max(abs(i-k),abs(j-l)),max(abs(i-m),abs(j-n))
      for s in range(d-1):
        if self.banmen[(i+(s+1)*(k-i)//d)*self.N+j+(s+1)*(l-j)//d]>=0: self.banmen[(i+(s+1)*(k-i)//d)*self.N+j+(s+1)*(l-j)//d]-=1
        if self.banmen[(m+(s+1)*(k-i)//d)*self.N+n+(s+1)*(l-j)//d]>=0: self.banmen[(m+(s+1)*(k-i)//d)*self.N+n+(s+1)*(l-j)//d]-=1
      for t in range(e-1):
        if self.banmen[(i+(t+1)*(m-i)//e)*self.N+j+(t+1)*(n-j)//e]>=0: self.banmen[(i+(t+1)*(m-i)//e)*self.N+j+(t+1)*(n-j)//e]-=1
        if self.banmen[(k+(t+1)*(m-i)//e)*self.N+l+(t+1)*(n-j)//e]>=0: self.banmen[(k+(t+1)*(m-i)//e)*self.N+l+(t+1)*(n-j)//e]-=1

    #スコアの算出
    def score(self,L):
      return sum([(L[i][0]-(N-1)//2)**2+(L[i][1]-(N-1)//2)**2+1 for i in range(len(L))])

  #変数の用意
  N,M=map(int,input().split())
  points=[list(map(int,input().split())) for i in range(M)]
  banmen=[0]*(N**2)
  for i in range(M):
    x,y=points[i]
    banmen[x*N+y]=-1
  banmen2=[0]*(N*(N-1)*2+(N-1)**2*2)

  def Weight(i,j,k,l,m,n):
    return max(abs(i-k),abs(j-l))+max(abs(i-m),abs(j-n))
  def Weight2(i,j,k,l,m,n):
    return (-1)*(max(abs(i-k),abs(j-l))+max(abs(i-m),abs(j-n)))
  def Weight3(i,j,k,l,m,n):
    return (i-(N-1)//2)**2+(j-(N-1)//2)**2+1
  def Weight4(i,j,k,l,m,n):
    return (-1)*((i-(N-1)//2)**2+(j-(N-1)//2)**2+1)
  def Weight5(i,j,k,l,m,n):
    return i
  def Weight6(i,j,k,l,m,n):
    return j
  def Weight7(i,j,k,l,m,n):
    return -i
  def Weight8(i,j,k,l,m,n):
    return -j
  def Weight9(i,j,k,l,m,n):
    return i+j
  def Weight10(i,j,k,l,m,n):
    return -i-j
  def Weight11(i,j,k,l,m,n):
    return i-j
  def Weight12(i,j,k,l,m,n):
    return -i+j
  def Weight13(i,j,k,l,m,n):
    return i*j
  def Weight14(i,j,k,l,m,n):
    return -i*j
  def Weight15(i,j,k,l,m,n):
    return max(abs(i-k),abs(j-l))*max(abs(i-m),abs(j-n))
  def Weight16(i,j,k,l,m,n):
    return (-1)*max(abs(i-k),abs(j-l))*max(abs(i-m),abs(j-n))

  def bi(i,j,k):
      if k==0: return i*(N-1)+j
      elif k==1: return N**2-N-1+N*i+j
      elif k==2: return N*(N-1)*2+(N-1)*i+j
      else: return N*(N-1)*2+(N-1)**2+(N-1)*i+j

  def f(output):
    banmen=[0]*(N**2)
    banmen2=[0]*(N*(N-1)*2+(N-1)**2*2)
    for ii in range(len(output)):
      i,j,k,l,___,____,m,n=output[ii]
      banmen[i*N+j]=-1
      d,e=max(abs(i-k),abs(j-l)),max(abs(i-m),abs(j-n))
      p=0 if i==k else 1 if j==l else 2 if i-j==k-l else 3
      q=0 if i==m else 1 if j==n else 2 if i-j==m-n else 3
      for s in range(d):
        banmen2[bi(min(i+s*(k-i)//d,i+(s+1)*(k-i)//d),min(j+s*(l-j)//d,j+(s+1)*(l-j)//d),p)]=1
        banmen2[bi(min(m+s*(k-i)//d,m+(s+1)*(k-i)//d),min(n+s*(l-j)//d,n+(s+1)*(l-j)//d),p)]=1
      for t in range(e):
        banmen2[bi(min(i+t*(m-i)//e,i+(t+1)*(m-i)//e),min(j+t*(n-j)//e,j+(t+1)*(n-j)//e),q)]=1
        banmen2[bi(min(k+t*(m-i)//e,k+(t+1)*(m-i)//e),min(l+t*(n-j)//e,l+(t+1)*(n-j)//e),q)]=1
    return banmen, banmen2

  w=[Weight,Weight2,Weight3,Weight4,Weight5,Weight6,Weight7,Weight8,Weight9,Weight10,Weight11,Weight12,Weight13,Weight14,Weight15,Weight16]
  TL = 4.5
  start = time.perf_counter()
  rect=RectJoin(N)
  tmp=[]
  for i in range(len(w)):
    rect.Solve(w[i],banmen,banmen2)
  cnt=0
  W=rect.Weight
  k=1
  while True:
    if cnt % 10 == 0:
      now = time.perf_counter()
      elapsed =  now - start
      if elapsed//1 > k:
        banmen,banmen2=f(rect.ans[:k*15])
        k+=1
      if elapsed > TL:
        break
    def tmp(i,j,k,l,m,n):
      p=randint(0,5)
      if p==0: return 0
      return W(i,j,k,l,m,n)
    rect.Solve(tmp,banmen,banmen2)
    cnt+=1

  #結果の出力
  print(len(rect.ans))
  for i in range(len(rect.ans)):
    print(*rect.ans[i])