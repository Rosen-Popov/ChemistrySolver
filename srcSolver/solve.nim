import ./kernel.nim
import ./parcer.nim
import ./test.nim


proc ParceAndSolve(reaction:string):string=
  let chem_eq:seq[seq[ChemCompund]] = SplitEquasionSides(reaction)
  let modiff:seq[int] = GetKernel(CreateMatrix(reaction))
  var res=""
  var in_sol = 0

  for i in 0..chem_eq[0].high():
    if modiff[in_sol] > 1:
      res = res & $modiff[in_sol] & "*" & chem_eq[0][i].Chem
    else:
      res = res & chem_eq[0][i].Chem
    if i < chem_eq[0].high():
      res = res & " + "
    inc in_sol
  res = res & " -> "
    
  for i in 0..chem_eq[1].high():
    if modiff[in_sol] > 1:
      res = res & $modiff[in_sol] & "*" & chem_eq[1][i].Chem
    else:
      res = res & chem_eq[1][i].Chem
    if i < chem_eq[1].high():
      res = res & " + "
    inc in_sol
  return res


if isMainModule:
  block ParceAndSolveTest:
    let result = @[ParceAndSolve("C2H5OH + O2 -> CO2 + H2O")]
    let expected = @["C2H5OH + 3*O2 -> 2*CO2 + 3*H2O"]
    TestEqu(expected,result,"ParceAndSolve ")
