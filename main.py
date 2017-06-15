import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt
import helpers.viewHelper as help
import Tkinter as tk
import patientRegister as patientReg
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


#******************try-1

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Brain Tumor Detector')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartingPage, Denoiser):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartingPage (tk.Frame):
    patientDirectory = ''
    #modality = 0
    T1_modality = False
    T2_modality = False
    pubController = None#in order to make controoler available in other methods

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='Select patient directory: ', padx = 50).grid(row=0, column=0)
        tk.Button(self, text="Browse Directory", command=self.getPatient, width=15, padx=20).grid(row=0, column=1)
        #self.label = Label(frame, text='Select modality').pack(side=BOTTOM)

        StartingPage.T1_modality = tk.BooleanVar()
        StartingPage.T2_modality = tk.BooleanVar()
        tk.Label(self, text='Select modality: ', padx = 50).grid(row = 2, column = 0)
        tk.Checkbutton(self,
                    text="T1 weighted",
                    variable=StartingPage.T1_modality).grid(row = 3, column = 0)
        tk.Checkbutton(self,
                    text="T2 weighted",
                    variable=StartingPage.T2_modality).grid(row = 4, column = 0)
        tk.Button(self, text="Next", command=self.next, width=15, padx=20).grid(row = 5, column = 1)
        StartingPage.pubController = controller

    def getPatient(self):
        StartingPage.patientDirectory = patientReg.Register().getPatient()
        #print(App.patientDirectory)

    def next(self):
        # print(str(App.T1_modality.get()))
        # print(str(App.T2_modality.get()))
        #print (StartingPage.patientDirectory)
        StartingPage.pubController.show_frame(Denoiser)


class Denoiser(tk.Frame):
    sliceNumber = ''
    smoothingMethod = ''

    def __init__(self, parent, controller):
        Denoiser.sliceNumber = tk.StringVar()
        Denoiser.sliceNumber.set('25')
        tk.Frame.__init__(self, parent)

        tk.Button(self, text="Next", command=self.onClickNext, width=15, padx=20).grid(row=0, column=6)
        self.number = tk.Entry(self, textvariable = Denoiser.sliceNumber, width=15).grid(row=0, column=5)
        tk.Button(self, text="Previous", command=self.onClickPrev, width=15, padx=20).grid(row=0, column=4)

        t1_check = tk.BooleanVar()
        t2_check = tk.BooleanVar()
        tk.Label(self, text='Select modality: ', padx=50).grid(row=1, column=4)
        tk.Checkbutton(self,
                       text="T1 weighted",
                       variable=t1_check).grid(row=2, column=4)
        tk.Checkbutton(self,
                       text="T2 weighted",
                       variable=t2_check).grid(row=2, column=5)

        Denoiser.smoothingMethod = tk.StringVar()
        tk.Label(self, text = 'Select Smoothing Method').grid(row = 3, column = 4, sticky = 'ew')
        tk.OptionMenu(self, Denoiser.smoothingMethod, 'N4Bias Field Corrention', 'Curvature Flow').grid(row = 3, column = 5, sticky= 'ew')
        tk.Button(self, text="Apply filter", command=self.onClickApplyFilter, width=15, padx=20).grid(row=3, column=6)

        tvFrame = tk.Frame(self)#creating new frame for matplotlib, since grid and pack cannot be used in same frame
        tvFrame.grid(row = 0, column = 0, columnspan= 4, rowspan = 5)

        #ggg
        filenameT1 = "./dataset/mr_T1/patient_109_mr_T1.mhd"
        idxSlice = 26
        imgT1Original = SimpleITK.ReadImage(filenameT1)
        #help.sitk_show(SimpleITK.Tile(imgT1Original[:, :, idxSlice], imgT2Original[:, :, idxSlice], (2, 1, 0))
        ndArray = SimpleITK.GetArrayFromImage(imgT1Original[:, :, idxSlice])
        title = None
        margin = 0.0
        dpi = 40
        figsize = (1 + margin) * ndArray.shape[0] / dpi, (1 + margin) * ndArray.shape[1] / dpi
        extent = (0, ndArray.shape[1], ndArray.shape[0], 0)
        fig = matplotlib.pyplot.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])
        ax.imshow(ndArray)

        #ggg


        # f = Figure(figsize=(5, 5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(fig, tvFrame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, tvFrame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



    def onClickNext(self):
        current = int(str(Denoiser.sliceNumber.get())) + 1
        Denoiser.sliceNumber.set(current)

    def onClickPrev(self):
        current = int(str(Denoiser.sliceNumber.get())) - 1
        Denoiser.sliceNumber.set(current)

    def onClickApplyFilter(self):
        print('smoothning')














app = App()
app.geometry("1000x500")
app.mainloop()

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



