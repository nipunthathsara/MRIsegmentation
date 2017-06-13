import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt
import helpers.viewHelper as help
from Tkinter import *
import patientRegister as patientReg


#******************try-1
class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.button = Button(frame, text="Browse Directory", command=self.getPatient, width=15, padx=20).pack()
        self.label = Label(frame, text='Select modality').pack(side=BOTTOM)
        self.selection = IntVar()

        self.T1 = Radiobutton(frame,
                              text="T1 weighted",
                              padx=20,
                              variable=self.selection,
                              value=1).pack(anchor=W)
        self.T2 = Radiobutton(frame,
                              text="T2 weighted",
                              padx=20,
                              variable=self.selection,
                              value=2).pack(anchor=W)

    def getPatient(self):
        patientDirectory = patientReg.Register().getPatient()
        print(patientDirectory)

root = Tk()
root.geometry("1000x1000")
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



