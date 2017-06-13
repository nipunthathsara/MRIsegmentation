import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt
import helpers.viewHelper as help
from Tkinter import *
import patientRegister as patientReg


#******************try-1
class App:
    modality = 0
    T1_modality = False
    T2_modality = False

    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        Label(frame, text='Select patient directory: ', padx = 50).grid(row=0, column=0)
        Button(frame, text="Browse Directory", command=self.getPatient, width=15, padx=50).grid(row=0, column=1)
        #self.label = Label(frame, text='Select modality').pack(side=BOTTOM)

        # App.modality = IntVar()
        App.T1_modality = BooleanVar()
        App.T2_modality = BooleanVar()
        Label(frame, text='Select modality: ', padx = 50).grid(row = 2, column = 0)
        # self.T1 = Radiobutton(frame,
        #                       text="T1 weighted",
        #                       padx=20,
        #                       variable=App.modality,
        #                       value=1).grid(row = 2, column = 0)
        # self.T2 = Radiobutton(frame,
        #                       text="T2 weighted",
        #                       padx=20,
        #                       variable=App.modality,
        #                       value=2).grid(row = 3, column = 0)
        Checkbutton(frame,
                    text="T1 weighted",
                    variable=App.T1_modality).grid(row = 3, column = 0)
        Checkbutton(frame,
                    text="T2 weighted",
                    variable=App.T2_modality).grid(row = 4, column = 0)
        Button(frame, text="Next", command=self.next, width=15, padx=20).grid(row = 5, column = 1)

    def getPatient(self):
        patientDirectory = patientReg.Register().getPatient()
        print(patientDirectory)

    def next(self):
        print(str(App.T1_modality.get()))
        print(str(App.T2_modality.get()))

root = Tk()
root.geometry("500x500")
app = App(root)
root.mainloop()

#**************end of try

filenameT1 = "./dataset/mr_T1/patient_109_mr_T1.mhd"
filenameT2 = "./dataset/mr_T2/patient_109_mr_T2.mhd"

idxSlice = 26
labelGrayMatter = 1

imgT1Original = SimpleITK.ReadImage(filenameT1)
imgT2Original = SimpleITK.ReadImage(filenameT2)

help.sitk_show(SimpleITK.Tile(imgT1Original[:, :, idxSlice],imgT2Original[:, :, idxSlice],(2,1,0))) #give input images in multiple args or as a list, then give display configurations as a tuple
#input slice number to other axis to get vertical cross sections



#**************************Smoothing*******************************

#Method 1 : CurvatureFlow
imgT1Smooth = SimpleITK.CurvatureFlow(image1=imgT1Original,timeStep=0.125,numberOfIterations=5)

imgT2Smooth = SimpleITK.CurvatureFlow(image1=imgT2Original,timeStep=0.125,numberOfIterations=5)

help.sitk_show(SimpleITK.Tile(imgT1Smooth[:, :, idxSlice],
                         imgT2Smooth[:, :, idxSlice],
                         (2, 1, 0)))



