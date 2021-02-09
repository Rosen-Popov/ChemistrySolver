# Mudule implements parcer for chemical expressions
# Reduces chemical expression into a suitable matrix representation

import re
import strutils
import strformat
import parseutils
import sequtils
import tables
import test

type
  ChemCompund* = object
    Mod*:int
    Chem*:string

let Numbers:set[char] = {'1','2','3','4','5','6','7','8','9','0'}
proc SplitEquasionSides*(reaction:string):seq[seq[ChemCompund]]=
  var tmp:string = reaction.replace(" ").replace(">")
  let spl:seq[string] = tmp.split('-')
  const left_side:int = 0
  const right_side:int = 1 
  result = @[ newSeq[ChemCompund](), newSeq[ChemCompund]()]
  for i in items(spl[left_side].split('+')):
    #                                       leading,trailing
    result[0].add(ChemCompund(Mod:1,Chem:(i.strip(true,false,Numbers + {'*'}))))
  for i in items(spl[right_side].split('+')):
    #                                          leading,trailing
    result[1].add(ChemCompund(Mod:(-1),Chem:(i.strip(true,false,Numbers + {'*'}))))
  return result

proc SplitEquasion(reaction:string):seq[ChemCompund]=
  var tmp:string = reaction.replace(" ").replace(">")
  let spl:seq[string] = tmp.split('-')
  const left_side:int = 0
  const right_side:int = 1 
  result = newSeq[ChemCompund]()
  for i in items(spl[left_side].split('+')):
    #                                       leading,trailing
    result.add(ChemCompund(Mod:1,Chem:(i.strip(true,false,Numbers + {'*'}))))
  for i in items(spl[right_side].split('+')):
    #                                          leading,trailing
    result.add(ChemCompund(Mod:(-1),Chem:(i.strip(true,false,Numbers + {'*'}))))
  return result

proc HasSurroundingBrackets(arg:string):bool=
  var bracket:int = 0
  #                        leading,trailing
  let tmp:string = arg.strip(false,true,Numbers)
  for i in 0..tmp.high():
    if arg[i] == '(':
      dec(bracket)
    if arg[i] == ')':
      inc(bracket)
    if i < tmp.high and bracket == 0:
      return false
  return true

proc StripBrackets(arg:string):string=
  if arg[0] == '(' and arg.HasSurroundingBrackets():
    #                      leading,trailing
    var p:string = arg.strip(false,true,Numbers)
    return p[1..p.high()-1]
  else:
    return arg

proc BracketSubgroupsSplit(arg:string):seq[string]=
  var lvl:int
  var subsequneces:seq[tuple[bg:int,en:int]]
  # find subsequneces
  for ind in 0..arg.high():
    if arg[ind] == '(':
      dec lvl
      if lvl == -1:
        subsequneces.add((bg:ind,en:0))
    if arg[ind] == ')':
      inc lvl
      if lvl == 0:
        subsequneces[subsequneces.high()].en = ind
  assert(lvl == 0,"Unbalanced number of brackets")
  # elongate subsequences to have the modifiers,
  # if it has brackets it has a modifier
  if subsequneces.len() > 0:
    for i in 0..subsequneces.high():
      for j in subsequneces[i].en+1..arg.high():
        if arg[j] in Numbers:
          inc subsequneces[i].en
        else:
          break
  # now break array into subsequences
    var begining:int=0
    var ending:int = subsequneces[0].bg
    var res:seq[string]
    if begining != ending:
      res.add(arg[begining..<ending])
    for i in 0..subsequneces.high():
      begining = subsequneces[i].bg
      ending = subsequneces[i].en
      res.add(arg[begining..ending])
      if i == subsequneces.high():
        if ending != arg.high():
          res.add(arg[ending..arg.high()])
      else:
        begining = ending
        ending = subsequneces[i+1].bg
        if ending - begining > 1:
          res.add(arg[begining..ending])
    return res
  else:
    return @[arg]

proc IsCompound(arg:string):bool=
  var n:int
  for i in items(arg):
    if 'A' <= i and i <= 'Z':
      inc n
      if n > 1:
        return true
  return false
proc IsCompound(arg:ChemCompund):bool=
  return IsCompound(arg.Chem)

proc IsElement(arg:string):bool=
  var n:int
  for i in items(arg):
    if 'A' <= i and i <= 'Z':
      inc n
      if n > 1:
        return false
    if i in Numbers:
      return false
  return true

proc Extract(arg:ChemCompund):seq[ChemCompund]=
  if IsElement(arg.Chem):
    return @[arg]
  var comp:string = arg.Chem
  var global_mod:int = arg.Mod
  var chem_regex:Regex = re(r"([A-Z][a-z]?[0-9]*)|([(].*[)][0-9]*)")
  var num_regex:Regex  = re(r"[0-9]*\Z")
  var Found:seq[string]= findAll(comp,chem_regex)
  var MoreSplit:seq[string]
  var res:seq[ChemCompund]
  for i in items(Found):
    if not IsCompound(i):
      MoreSplit.add(i)
    else:
      MoreSplit = MoreSplit & BracketSubgroupsSplit(i)
  res.setLen(MoreSplit.len())
  for i in 0..MoreSplit.high():
    var Mod:seq[string] = findAll(MoreSplit[i],num_regex).filter(proc (x:string):bool= x != "")
    res[i].Chem = MoreSplit[i].strip(false,true,Numbers).StripBrackets
    if Mod.len() == 0:
      res[i].Mod = global_mod
    else:
      res[i].Mod = global_mod * parseInt(Mod[0])
  return res

proc Decompose(compound:string):Table[string,int]=
  var Gone:seq[ChemCompund] = Extract(ChemCompund(Mod:1,Chem:compound)) #reduced to atoms :)
  var res:Table[string,int]
  while (Gone.map(IsCompound).foldl(a or b,false)):
    Gone = Gone.map(Extract).foldl(a & b)
  for i in items(Gone):
    if res.hasKey(i.Chem):
      res[i.Chem] = res[i.Chem] + i.Mod
    else:
      res[i.Chem] = i.Mod
  return res

proc CreateMatrix*(equation:string):seq[seq[int]]=
  var res:Table[string,seq[int]]
  var real_res:seq[seq[int]]
  var splt:seq[ChemCompund]=SplitEquasion(equation)
  var Gone:seq[Table[string,int]]
  Gone.setLen(splt.len())
  for i in 0..splt.high():
    Gone[i] = Decompose(splt[i].Chem)
  for i in items(Gone):
    for k in keys(i):
      if not res.hasKey(k):
        res[k]= repeat(0,splt.len())
  for col in 0..splt.high():
    for row in keys(Gone[col]):
      res[row][col] = Gone[col][row] * splt[col].Mod
  for i in keys(res):
    real_res.add(res[i])
  return real_res

if isMainModule:
  block SplitEquasionTest:
    let name:string = "SplitEquasion "
    let res:seq[ChemCompund] = SplitEquasion("1*C3H8O + O2 -> CO2 + H2O")
    let expected:seq[ChemCompund] = @[
      ChemCompund(Mod:1,Chem:"C3H8O"),
      ChemCompund(Mod:1,Chem:"O2"),
      ChemCompund(Mod:(-1),Chem:"CO2"),
      ChemCompund(Mod:(-1),Chem:"H2O")]
    TestEqu(expected,res,name)

  block StripBracketsTest:
    let name:string = "StripBrackets "
    let res:seq[string]= @[
      StripBrackets("(OH)2"),
      StripBrackets("(OH)"),
      StripBrackets("OH2"),
      StripBrackets("(OH)2(OH)2")]
    let expected:seq[string]  = @["OH","OH","OH2","(OH)2(OH)2"]
    TestEqu(expected,res,name)

  block BracketSubgroupsSplitTest:
    let name:string = "BracketSubgroupsSplit "

    let result0:seq[string] = BracketSubgroupsSplit("C3(H8)2(O3(O5))")
    let expected0:seq[string] = @["C3", "(H8)2", "(O3(O5))"]
    TestEqu(expected0,result0,name & " Nested Brackets ")

    let result1:seq[string] = BracketSubgroupsSplit("Ca(OH)12(OH)23")
    let expected1:seq[string] = @["Ca", "(OH)12", "(OH)23"]
    TestEqu(expected1,result1,name & " Planar Brackets ")

    let result2:seq[string] = BracketSubgroupsSplit("Ca")
    let expected2:seq[string] = @["Ca"]
    TestEqu(expected2,result2,name & " No Brackets ")

    let result3:seq[string] = BracketSubgroupsSplit("((OH)2(OH)2)")
    let expected3:seq[string] = @["((OH)2(OH)2)"]
    TestEqu(expected3,result3,name & " Inside Brackets ")

  block ExtractTest:
    let name:string = "Extract"

    let result0:seq[ChemCompund] = Extract(ChemCompund(Mod:1,Chem:"(OH)2(OH)2"))
    let expected0:seq[ChemCompund]= @[ChemCompund(Mod: 2, Chem: "OH"),
                                      ChemCompund(Mod: 2, Chem: "OH")] 
    TestEqu(expected0,result0,name & " Brackets Formula ")

    let result1:seq[ChemCompund] = Extract(ChemCompund(Mod:1,Chem:"C2H5OH"))
    let expected1:seq[ChemCompund]= @[ChemCompund(Mod: 2, Chem: "C"),
                                      ChemCompund(Mod: 5, Chem: "H"), 
                                      ChemCompund(Mod: 1, Chem: "O"),
                                      ChemCompund(Mod: 1, Chem: "H")]
    TestEqu(expected1,result1,name & " Normal Formula ")

    let result2:seq[ChemCompund] = Extract(ChemCompund(Mod:2,Chem:"C2"))
    let expected2:seq[ChemCompund]= @[ChemCompund(Mod: 4, Chem: "C")] 
    TestEqu(expected2,result2,name & " Single Element ")

    let result3:seq[ChemCompund] = Extract(ChemCompund(Mod:1,Chem:"C"))
    let expected3:seq[ChemCompund]= @[ChemCompund(Mod: 1, Chem: "C")] 
    TestEqu(expected3,result3,name & " Element")

  block DecomposeTest:
    let name:string = "Decompose"

    let result0:Table[string,int] = Decompose("C2H5OH")
    let expected0:Table[string,int] = {"H": 6, "C": 2, "O": 1}.toTable
    TestEquTables(expected0,result0,name & " Basic Reaction")

    let result1:Table[string,int] = Decompose("Ca(OH)2")
    let expected1:Table[string,int] = {"H": 2, "Ca": 1, "O": 2}.toTable
    TestEquTables(expected1,result1,name & " Nested Reaction")

    let result2:Table[string,int] = Decompose("C2H5(OH)2")
    let expected2:Table[string,int] = {"H": 7, "C": 2, "O": 2}.toTable
    TestEquTables(expected2,result2,name & " Nested A little complex Reaction")

  block CreateMatrixTest:
    let expected:seq[seq[int]] = @[ @[6, 0, 0, -2], @[2, 0, -1, 0], @[1, 2, -2, -1]]
    let result:seq[seq[int]] = CreateMatrix("C2H5OH + O2 -> CO2 + H2O")
    TestEquUnordered(expected,result,"CreateMatrix")


