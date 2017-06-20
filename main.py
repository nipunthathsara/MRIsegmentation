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
import tkMessageBox

import smoothers.curvatureFlow as cFlow
# import regions.segmentator as sgmnttr


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

        for F in (StartingPage, Denoiser, Segmentor):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        return frame


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
        #print(StartingPage.patientDirectory)

    def next(self):
        # print(str(App..0T1_modality.get()))
        # print(str(App.T2_modality.get()))
        print (StartingPage.patientDirectory)
        StartingPage.pubController.show_frame(Denoiser)



class Denoiser(tk.Frame):
    sliceNumber = ''
    smoothingMethod = ''
    t1_check = True
    t2_check = False

    t1_original = None
    t2_original = None
    t1_smoothned = None
    t2_smoothned = None
    tvFrame = None
    helpObj = None
    pubController = None

    def __init__(self, parent, controller):
        Denoiser.sliceNumber = tk.StringVar()
        Denoiser.sliceNumber.set('25')
        tk.Frame.__init__(self, parent)
        Denoiser.pubController = controller

        Denoiser.tvFrame = tk.Frame(self)  # creating new frame for matplotlib, since grid and pack cannot be used in same frame
        Denoiser.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)

        tk.Button(self, text="Next", command=self.onClickNext, width=15, padx=20).grid(row=0, column=6)
        self.number = tk.Entry(self, textvariable = Denoiser.sliceNumber, width=15).grid(row=0, column=5)
        tk.Button(self, text="Previous", command=self.onClickPrev, width=15, padx=20).grid(row=0, column=4)

        Denoiser.t1_check = tk.BooleanVar()
        Denoiser.t2_check = tk.BooleanVar()

        tk.Label(self, text='Select modality: ', padx=50).grid(row=1, column=4)
        tk.Checkbutton(self,
                       text="T1 weighted",
                       variable=Denoiser.t1_check).grid(row=2, column=4)
        tk.Checkbutton(self,
                       text="T2 weighted",
                       variable=Denoiser.t2_check).grid(row=2, column=5)
        tk.Button(self, text="Load Modality", command=self.onClickLoad, width=15, padx=20).grid(row=2, column=6)

        Denoiser.smoothingMethod = tk.StringVar()
        tk.Label(self, text = 'Select Smoothing Method').grid(row = 3, column = 4, sticky = 'ew')
        tk.OptionMenu(self, Denoiser.smoothingMethod, 'N4Bias Field Corrention', 'Curvature Flow').grid(row = 3, column = 5, sticky= 'ew')
        tk.Button(self, text="Apply filter", command=self.onClickApplyFilter, width=15, padx=20).grid(row=3, column=6)
        tk.Button(self, text="Proceed", command=self.onClickProceed, width=15, padx=20).grid(row=4, column=6)

        filenameT1 = "./dataset/mr_T1/patient_109_mr_T1.mhd" #add default jpg url here
        Denoiser.t1_original = SimpleITK.ReadImage(filenameT1)
        filenameT2 = "./dataset/mr_T2/patient_109_mr_T2.mhd"  # add default jpg url here
        Denoiser.t2_original = SimpleITK.ReadImage(filenameT2)
        help.show(Denoiser.t1_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)



    def onClickNext(self):
        current = int(str(Denoiser.sliceNumber.get())) + 1
        Denoiser.sliceNumber.set(current)
        Denoiser.tvFrame = None
        Denoiser.tvFrame = tk.Frame(self)  # creating new frame for matplotlib, since grid and pack cannot be used in same frame
        Denoiser.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
        if (Denoiser.t1_check.get()):
            help.show(Denoiser.t1_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
        if (Denoiser.t2_check.get()):
            help.show(Denoiser.t2_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
        if ((Denoiser.t2_check.get()) and (Denoiser.t1_check.get())):
            help.show(SimpleITK.Tile(Denoiser.t2_original[:, :, int(Denoiser.sliceNumber.get())],Denoiser.t1_original[:, :, int(Denoiser.sliceNumber.get())]), Denoiser.tvFrame)

    def onClickPrev(self):
        current = int(str(Denoiser.sliceNumber.get())) - 1
        Denoiser.sliceNumber.set(current)
        Denoiser.tvFrame = None
        Denoiser.tvFrame = tk.Frame(self)
        Denoiser.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
        if (Denoiser.t1_check.get()):
            help.show(Denoiser.t1_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
        if (Denoiser.t2_check.get()):
            help.show(Denoiser.t2_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
        if ((Denoiser.t2_check.get()) and (Denoiser.t1_check.get())):
            help.show(SimpleITK.Tile(Denoiser.t2_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.t1_original[:, :, int(Denoiser.sliceNumber.get())]), Denoiser.tvFrame)

    def onClickLoad(self):
        Denoiser.tvFrame = None
        Denoiser.tvFrame = tk.Frame(self)
        Denoiser.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
        if(Denoiser.t1_check.get() and not Denoiser.t2_check.get()):
            Denoiser.t1_original = patientReg.Register().getModality(StartingPage.patientDirectory, '_T1.')
            help.show(Denoiser.t1_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
        if(Denoiser.t2_check.get() and not Denoiser.t1_check.get()):
            Denoiser.t2_original = patientReg.Register().getModality(StartingPage.patientDirectory, '_T2.')
            help.show(Denoiser.t2_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
        if((Denoiser.t2_check.get()) and (Denoiser.t1_check.get())):
            Denoiser.t1_original = patientReg.Register().getModality(StartingPage.patientDirectory, '_T1.')
            Denoiser.t2_original = patientReg.Register().getModality(StartingPage.patientDirectory, '_T2.')
            help.show(SimpleITK.Tile(Denoiser.t2_original[:, :, int(Denoiser.sliceNumber.get())], Denoiser.t1_original[:, :, int(Denoiser.sliceNumber.get())]), Denoiser.tvFrame)



    def populateDefaults(self):
        Denoiser.t1_original = patientReg.Register().getModality(StartingPage.patientDirectory, '_T1.')

    def onClickApplyFilter(self):
        if(Denoiser.smoothingMethod):
            method = 0 if (str(Denoiser.smoothingMethod.get()) == 'Curvature Flow') else 1 #curvature flow is 0
            if(method == 0): #Curvature flow
                Denoiser.tvFrame = None
                Denoiser.tvFrame = tk.Frame(self)
                Denoiser.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
                if(Denoiser.t1_check.get() and not Denoiser.t2_check.get()):#if T1 selected
                    Denoiser.t1_smoothned = cFlow.CurvatureFlow().applycFlow(Denoiser.t1_original)
                    help.show(Denoiser.t1_smoothned[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
                elif (Denoiser.t2_check.get() and not Denoiser.t1_check.get()):#if T2
                    Denoiser.t2_smoothned = cFlow.CurvatureFlow().applycFlow(Denoiser.t2_original)
                    help.show(Denoiser.t2_smoothned[:, :, int(Denoiser.sliceNumber.get())], Denoiser.tvFrame)
                elif (Denoiser.t2_check.get() and Denoiser.t1_check.get()):#if Both T1 and T2
                    Denoiser.t1_smoothned = cFlow.CurvatureFlow().applycFlow(Denoiser.t1_original)
                    Denoiser.t2_smoothned = cFlow.CurvatureFlow().applycFlow(Denoiser.t2_original)
                    help.show(SimpleITK.Tile(Denoiser.t1_smoothned[:, :, int(Denoiser.sliceNumber.get())], Denoiser.t2_smoothned[:, :, int(Denoiser.sliceNumber.get())]), Denoiser.tvFrame)

            elif (method == 1):#N4BFCorrection
                if (Denoiser.t1_check.get() and not Denoiser.t2_check.get()): #if T1 selected
                    Denoiser.t1_smoothned = cFlow.CurvatureFlow().applycFlow()
                elif (Denoiser.t2_check.get() and not Denoiser.t1_check.get()):
                    Denoiser.t2_smoothned = cFlow.CurvatureFlow().applycFlow()
                elif (Denoiser.t2_check.get() and Denoiser.t1_check.get()):
                    Denoiser.t1_smoothned = cFlow.CurvatureFlow().applycFlow()
                    Denoiser.t2_smoothned = cFlow.CurvatureFlow().applycFlow()

    def onClickProceed(self):
        frame = Denoiser.pubController.show_frame(Segmentor)
        frame.t1_smoothned = Denoiser.t1_smoothned
        frame.t2_smoothned = Denoiser.t2_smoothned
        frame.sliceNumber = int(Denoiser.sliceNumber.get())
        frame.t1_checked = Denoiser.t1_check.get()
        frame.t2_checked = Denoiser.t2_check.get()




class Segmentor (tk.Frame):
    tvFrame = None

    def __init__(self, parent, controller):
        self.canvas = None
        self.t1_smoothned = None
        self.t2_smoothned = None
        self.sliceNumber = 0
        self.t1_checked = False
        self.t2_checked = False
        self.modToSegment = ''
        self.selectedMatter = ''
        self.image = None
        self.seeds = []

        self.grayLabel = 1
        self.whiteLabel = 2

        tk.Frame.__init__(self, parent)

        Segmentor.tvFrame = tk.Frame(self)
        Segmentor.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)

        self.modToSegment = tk.StringVar()
        tk.Label(self, text='Select modality to continue: ', padx=50).grid(row=1, column=4)
        tk.OptionMenu(self, self.modToSegment, 'T1 weighted', 'T2 weighted', 'T1 and T2').grid(row=1, column=5, sticky='ew')
        tk.Button(self, text="Load", command=self.onClickLoad, width=15, padx=20).grid(row=2, column=5)
        tk.Button(self, text="Mark Seeds", command=self.onClickMarkSeeds, width=15, padx=20).grid(row=3, column=5)

        self.selectedMatter = tk.StringVar()
        tk.Label(self, text='Select criteria: ', padx=50).grid(row=4, column=4)
        tk.OptionMenu(self, self.selectedMatter, 'Gray Matter', 'White matter', 'All').grid(row=4, column=5, sticky='ew')
        tk.Button(self, text="Segment", command=lambda: self.onClickSegement(str(self.modToSegment.get()), str(self.selectedMatter.get())), width=15, padx=20).grid(row=4, column=6)


    def onClickLoad(self):
        try:
            if (str(self.modToSegment.get()) == 'T1 weighted'):
                self.canvas = help.show(self.t1_smoothned[:, :, self.sliceNumber], Segmentor.tvFrame)
                self.image = self.t1_smoothned
            elif (str(self.modToSegment.get()) == 'T2 weighted'):
                self.canvas = help.show(self.t2_smoothned[:, :, self.sliceNumber], Segmentor.tvFrame)
                self.image = self.t2_smoothned
            elif (str(self.modToSegment.get()) == 'T1 and T2'):
                # self.canvas = help.show(SimpleITK.Tile(self.t1_smoothned[:, :, self.sliceNumber], self.t2_smoothned[:, :, self.sliceNumber]), Segmentor.tvFrame)
                self.canvas = help.show(self.t1_smoothned[:, :, self.sliceNumber], Segmentor.tvFrame)#display only one, otherwise frame resizes
                self.image = SimpleITK.Compose(self.t1_smoothned, self.t2_smoothned)#create multi component image, multi values per pixel

        except:
            tkMessageBox.showerror("Files not available", "Make sure you've loaded only the pre-processed modalities")

    def onClickMarkSeeds(self):
        print('marking seeds')
        self.graySeeds = [(165, 178, self.sliceNumber),
                    (98, 165, self.sliceNumber),
                    (205, 125, self.sliceNumber),
                    (173, 205, self.sliceNumber)]

        # self.whiteSeeds = [(118, 77, self.sliceNumber),
        #                   (162, 78, self.sliceNumber),
        #                   (98, 151, self.sliceNumber),
        #                   (151, 146, self.sliceNumber)]
        self.whiteSeeds = [(80, 184, self.sliceNumber),
                           (186, 201, self.sliceNumber),
                           (118, 77, self.sliceNumber),
                           (160, 79, self.sliceNumber)]

        if(str(self.modToSegment.get()) == 'T1 and T2'):
            seedMarkedImg = SimpleITK.Image(self.t2_smoothned)# can't mark on composite image therefore use T1 or T2
        else:
            seedMarkedImg = SimpleITK.Image(self.image)# creates a copy


        for seed in self.graySeeds:
            seedMarkedImg[seed] = 10000
        for seed in self.whiteSeeds:
            seedMarkedImg[seed] = 20000
        Segmentor.tvFrame = tk.Frame(self)
        Segmentor.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
        help.show(seedMarkedImg[:, :, self.sliceNumber], Segmentor.tvFrame)

    def onClickSegement(self, mod, matter):
        if (matter == 'Gray Matter'):
            if (mod == 'T1 and T2'):
                grayMatter = SimpleITK.VectorConfidenceConnected(image1=self.image,
                                               seedList=self.graySeeds,
                                               numberOfIterations=1,
                                               multiplier=0.1,
                                               replaceValue=self.grayLabel)
                # smoothnedScaled = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.image), grayMatter.GetPixelID()) #cast T1 or T2 to display along with gray matter
                smoothnedScaled = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.t2_smoothned), grayMatter.GetPixelID())#can't cast a composite image, instead use t1 or t2
                Segmentor.tvFrame = tk.Frame(self)
                Segmentor.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
                help.show(SimpleITK.LabelOverlay(smoothnedScaled[:, :, self.sliceNumber], grayMatter[:, :, self.sliceNumber]),Segmentor.tvFrame)

            else:
                # print('segmenting' + mod + ' ' + matter)
                grayMatter = SimpleITK.ConfidenceConnected(image1=self.image,
                                                           seedList=self.graySeeds,
                                                           numberOfIterations=3,
                                                           multiplier=1,
                                                           # width of confidence interval,  confidence interval is the mean plus or minus the "Multiplier" times the standard deviation
                                                           replaceValue=self.grayLabel)
                smoothnedScaled = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.image), grayMatter.GetPixelID())
                Segmentor.tvFrame = tk.Frame(self)
                Segmentor.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
                help.show(SimpleITK.LabelOverlay(smoothnedScaled[:, :, self.sliceNumber], grayMatter[:, :, self.sliceNumber]), Segmentor.tvFrame)

        elif (matter == 'White matter'):
            if (mod == 'T1 and T2'):
                whiteMatter = SimpleITK.VectorConfidenceConnected(image1=self.image,
                                                                 seedList=self.whiteSeeds,
                                                                 numberOfIterations=1,
                                                                 multiplier=0.1,
                                                                 replaceValue=self.whiteLabel)
                # smoothnedScaled = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.image), grayMatter.GetPixelID()) #cast T1 or T2 to display along with gray matter
                smoothnedScaled = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.t2_smoothned),
                                                 whiteMatter.GetPixelID())  # can't cast a composite image, instead use t1 or t2
                Segmentor.tvFrame = tk.Frame(self)
                Segmentor.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
                help.show(
                    SimpleITK.LabelOverlay(smoothnedScaled[:, :, self.sliceNumber], whiteMatter[:, :, self.sliceNumber]),
                    Segmentor.tvFrame)
            else:
                whiteMatter = SimpleITK.ConfidenceConnected(image1=self.image,
                                                           seedList=self.whiteSeeds,
                                                           numberOfIterations=3,
                                                           multiplier=1,
                                                           # width of confidence interval,  confidence interval is the mean plus or minus the "Multiplier" times the standard deviation
                                                           replaceValue=self.whiteLabel)
                smoothnedScaled = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.image), whiteMatter.GetPixelID())
                Segmentor.tvFrame = tk.Frame(self)
                Segmentor.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
                help.show(SimpleITK.LabelOverlay(smoothnedScaled[:, :, self.sliceNumber], whiteMatter[:, :, self.sliceNumber]), Segmentor.tvFrame)

        elif (matter == 'White matter'):
            if (mod == 'T1 and T2'):
                print('gg')








app = App()
app.geometry("1000x530")
app.mainloop()

#**************end of try
