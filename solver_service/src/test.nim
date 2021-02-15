import sequtils
import strformat
import tables

proc TestEqu*[T](expected,result:seq[T],block_module:string = "")= 
  var pos:int = 0
  var passed:int = 0
  for ex,res in items(zip(expected,result)):
    if ex == res:
      inc(passed)
    else:
      echo fmt"id {pos} failed {res} != {ex}"
    inc(pos)
  echo fmt"{block_module}Test {passed}/{pos} passed"

proc TestEquTables*[A,B](expected,result:Table[A,B],block_module:string = "")= 
  var pos:int = 0
  var passed:int = 0
  for i in expected.keys:
    if expected[i] != result[i]:
      echo fmt"key {i} value mismatch {expected[i]} != {result[i]}"
    else:
      inc passed
    inc pos
  echo fmt"{block_module}Test {passed}/{pos} passed"
  return

proc TestEquUnordered*[T](expected,result:seq[T],block_module:string = "")= 
  var pos:int = 0
  var passed:int = 0
  if result.len != expected.len:
    echo fmt"{block_module}Test argument length mismatch {result.len} != {expected.len}"
  for ex in items(expected):
    if ex in result:
      inc(passed)
    else:
      echo fmt"id {pos} {ex} not in {result}"
    inc(pos)
  echo fmt"{block_module}Test {passed}/{pos} passed"
