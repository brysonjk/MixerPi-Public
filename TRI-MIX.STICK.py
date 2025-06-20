#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from O2SENSOR_old import *

class App:

        def __init__(self, master):
                self.master = master
                frame = Frame(master)
                frame.pack()
                label = Label(frame, text='TRI-MIX Stick', font=("Helvetica", 32))
                label.grid(row=0, columnspan=2)

                label = Label(frame, text='', font=("Helvetica", 32))
                label.grid(row=1, columnspan=2)

                self.S0_reading_label = Label(frame, text='12.34', font=("Helvetica", 20))
                self.S0_reading_label.grid(row=2,column=0, sticky=W)

                self.S1_reading_label = Label(frame, text='12.34', font=("Helvetica", 20))
                self.S1_reading_label.grid(row=2,column=1, sticky=E)

                label = Label(frame, text='', font=("Helvetica", 32))
                label.grid(row=3, columnspan=2)

                self.mix_c1_label = Label(frame, text='123', font=("Helvetica", 45))
                self.mix_c1_label.grid(row=4, column=0, sticky=E)

                self.mix_c2_label = Label(frame, text='123', font=("Helvetica", 45))
                self.mix_c2_label.grid(row=4, column=1, sticky=W)
		
                self.update_S0_reading()
                self.update_S1_reading()
                self.update_mix_c1()
                self.update_mix_c2()


        def update_S0_reading(self):
                O2_S0 = get_O2_S0()
                reading_str = "S0: {:.2f}% O²".format(O2_S0)
                self.S0_reading_label.configure(text=reading_str)
                self.master.after(500, self.update_S0_reading)

        def update_S1_reading(self):
                O2_S1 = get_O2_S1()
                reading_str = "S1: {:.2f}% O²".format(O2_S1)
                self.S1_reading_label.configure(text=reading_str)
                self.master.after(500, self.update_S1_reading)

        def update_mix_c1(self):
                MIX_C1 = get_O2_S1()
                mix_c1_str = "{:.2f}% O² /".format(MIX_C1)
                self.mix_c1_label.configure(text=mix_c1_str)
                self.master.after(500, self.update_mix_c1)

        def update_mix_c2(self):
                O2_S0 = get_O2_S0()
                O2_S1 = get_O2_S1()
                MIX_CALC = (100-O2_S1)/(100-O2_S0)+O2_S0*(O2_S1-100)/(20.8*(100-O2_S0))
                MIX_C2 = MIX_CALC*100 
                mix_c2_str = " {:.2f}% He".format(MIX_C2)
                self.mix_c2_label.configure(text=mix_c2_str)
                self.master.after(500, self.update_mix_c2)


root = Tk()
root.wm_title('Dive Tools --- Tri-Mix Stick')
app = App(root)
root.geometry("800x450+0+0")
root.mainloop()
