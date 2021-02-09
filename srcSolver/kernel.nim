import sequtils
import math
import test

proc `-`(x,y:seq[int]):seq[int]=
  return zip(x,y).map(proc (p:(int,int)):int=return p[0] - p[1])

proc by(x:seq[int],i:int):seq[int]=
  return x.map(proc (p:int) :int= p*i)

proc by_i(x:var seq[int],i:int)=
  x = x.map(proc (p:int) :int= p*i)


proc NZeros(ver:seq[int]):int=
  var res:int
  for i in items(ver):
    if 0 == i:
      inc(res)
  return res

proc FindIndexes(ver:seq[int]):seq[int]=
  result = @[]
  for p in 0..ver.high():
    if ver[p] != 0:
      result.add(p)
  return result

proc FindMissingIndex(vect, sol:seq[int]):int=
  for i in 0..vect.high():
    if vect[i] != 0 and sol[i] == 0:
      return i

proc OnlyZeros(ver:seq[int]):bool=
  for i in items(ver):
    if i != 0:
      return false
  return true

proc ExistInBoth(x,y:seq[int]):int=
  var res:int
  for i,j in items(zip(x,y)):
    if i>0 and j>0:
      inc(res)
  return res

proc ZeroLines(matr:seq[seq[int]]):int=
  var res:int
  for i in items(matr):
    if OnlyZeros(i):
      inc(res)
  return res

proc NSolutions(matr:seq[seq[int]]):int=
    return abs(matr.len()-matr[0].len()) + ZeroLines(matr)

proc optimise(x:var seq[int])=
  let reduce = x.gcd()
  if reduce > 1:
    x = x.map(proc (p:int):int= p div reduce)

proc optimise(x:seq[int]):seq[int]=
  let reduce = x.gcd()
  if reduce > 1:
    return x.map(proc (p:int):int= p div reduce)
  return x

#optimises matrcix to be solved by gauss method
proc GaussOptimise(matr:var seq[seq[int]],ind:int)=
  for i in ind..matr.high():
    if matr[i][ind] != 0:
      swap(matr[i],matr[ind])

proc GaussReduce(matr:var seq[seq[int]])=
  var MatrSquare:int=min([matr[0].len,matr.len])
  for i in 0..(MatrSquare-1):
    if matr[i][i] == 0:
      matr.GaussOptimise(i)
    for j in (i+1)..(MatrSquare-1):
      if matr[i][i] != 0 and matr[j][i] != 0:
        var devisor:int = lcm(matr[i][i],matr[j][i])
        let c1:int = devisor div matr[i][i]
        let c2:int = devisor div matr[j][i]
        matr[j] = optimise(matr[i].by(c1) - matr[j].by(c2))

    for i in countdown(MatrSquare-1,1):
      for j in countdown(i-1,0):
        if matr[i][i] != 0 and matr[j][i] != 0:
          let devisor = int(lcm(matr[i][i],matr[j][i]))
          let c1:int = devisor div matr[i][i]
          let c2:int = devisor div matr[j][i]
          matr[j] = optimise(matr[i].by(c1) - matr[j].by(c2))

proc GetKernel*(imatr:seq[seq[int]]):seq[int]=
  var matr = imatr
  GaussReduce(matr)
  if len(matr)==0:
      return @[]
  if len(matr[0])==0:
      return @[]
  var sol = repeat(0,matr[0].len())
  var comb = NSolutions(matr)
  if comb > 1:
    for p in (matr.len())..(matr[0].high()):
      sol[p] = 1

  var line_len:int = matr[0].len
  var rows:int = matr.len
  var line:int = 0
  var factors:int = 0
  var failsafe:int = 0
  var matches:int

  while(NZeros(sol)!=0):
    failsafe+=1
    assert(failsafe <= 100)
    factors = line_len - NZeros(matr[line])
    matches = ExistInBoth(matr[line],sol)
    if factors == 2 and matches == 0:
      let fact:seq[int] = FindIndexes(matr[line])
      ### we know that all of the indexes are coprime, because of the optimisation
      ### therefore we can just exchange their absolute values and be done with it
      sol[fact[0]] = abs (matr[line][fact[1]])
      sol[fact[1]] = abs (matr[line][fact[0]])
    elif factors - matches == 1 and matches != 0:
      ### general case of an equesion where all but one variables is known
      let missing = FindMissingIndex(matr[line],sol)
      let complement = zip(sol,matr[line]).map(proc (x:(int,int)):int= abs(x[0] * x[1])).sum()
      let common = abs(lcm(matr[line][missing],complement))
      sol.by_i(abs(common) div abs(complement))
      sol[missing] = abs(common) div abs(matr[line][missing])
    #otherwise we try each line in a round-robin fassion
    line+=1
    line=line mod rows
    optimise(sol)
  return (sol)

if isMainModule:
  # needed test only for this part because others are deterministic and 
  # algorithms are tested and only thing that can get wrong with them
  # is if comuter started doing weird things
  block GetKernelTest:
    let result = GetKernel(@[@[6, 0, 0, -2], @[0, -1, 0, 1], @[0, 0, 3, -2]])
    #"C2H5OH + O2 -> CO2 + H2O"
    let expected = @[1, 3, 2, 3]
    TestEqu(result,expected,"GetKernel")
