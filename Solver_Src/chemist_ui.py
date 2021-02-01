#!/usr/bin/python3.8

from tkinter import *
import chem_parcer

def Solve_Press(input_target,output_target):
    text = input_target.get()
    output_target.delete(0,END)
    try:
        _loc = chem_parcer.chemical_reaction(text)
        _loc.solve_eq()
        res=_loc.get_res()
    except:
        res="ERROR"
    output_target.insert(0,res)
    print("pass 1")

def Run_With_Window():
    window = Tk()
    window.title("Chemist")
    window.geometry('800x100+400+400')

    f_input = Entry(window,width = 80)
    f_input.grid(column=1, row=1)

    f_output = Entry(window,width = 80)
    f_output.grid(column=1, row=2)

    solve=Button(window,text='Solve',command = lambda : Solve_Press (f_input,f_output))
    solve.grid(column=2, row=1)

    window.mainloop()

if __name__ == "__main__":
    Run_With_Window()
