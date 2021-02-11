# A solver for chemical equations
A solver for chemical equations with a microservice architecture (NYI)\
Whole thing could have been a python script, but it is different 

## Solver Part - [Nim]
Solver and parcer of equations implemented in nim-lang 
 - Currently only solver + parcer with tests for each
 - Currenntly does not support valencies checking
 - Currently does not support ion equasions
 - Yield percentages/mass not supported as well, but might be in future
 - Could be used just as a include, currently only for C/C++ target\
 (depends on PCRE and javascript target uses a diffrent library) 
 - Doesnt have input validation
 - service part will be implemented later (with [jester])

## Opencv + Ocr - Python
 - As a added bonus, (attempt to) use a image as input, for ease of use.
 - Whole project would have remained in Nim, if it wasnt for this part\
 as I don't know of opencv/ocr bindings for nim, and have experience with it inly on python
 - I wanted something like phtomath? or similar type of program
## Server (Not yet known, but deffinetly not java)
 - Server that provideshandling of connections and request processing
 - Implementation language not decided on yet (maybe go-lang)

## Ui
 - Web based ui, either in javascript/typescript/[NIm]
 - A nim implementation would ether use [jester] or be in javascript
 - Input of expressions as text(maybe Latex parcer for expressions)
 - Allows for importing images form a link
 - Uploading images
 - Text files with expressions for bulk processing


## More on Solver - inner workings
 - Split in two parts, parcer and solver
 - Parcer - creates a system of linear equasions, represented with a matrix
 - Coeficients are quantities of each element in each compound
 - Solver module then takes said matrix and returns a vector with positive coeficients for each compound in formula
 - This vector happens to also be the kernel of said matrix and is only one (only one solution SHOULD exist)
 - To reach that solutin, matrix is diagonalized as much as possible using the gauss method \
    and then solved as one would a system of quasions
 - A possible derivative of the project would be a generic linear algebra library for nim, if there is one, i havent met it yet
 
 
 [jester]: https://github.com/dom96/jester
 [Nim]: https://nim-lang.org/
