import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt
import helpers.viewHelper as help

filenameT1 = "./dataset/mr_T1/patient_109_mr_T1.mhd"
filenameT2 = "./dataset/mr_T2/patient_109_mr_T2.mhd"

idxSlice = 26
labelGrayMatter = 1

imgT1Original = SimpleITK.ReadImage(filenameT1)
imgT2Original = SimpleITK.ReadImage(filenameT2)

help.sitk_show(SimpleITK.Tile(imgT1Original[:, :, idxSlice],
                         imgT2Original[:, :, idxSlice],
                         (2, 1, 0)))

imgT1Smooth = SimpleITK.CurvatureFlow(image1=imgT1Original,
                                      timeStep=0.125,
                                      numberOfIterations=5)

imgT2Smooth = SimpleITK.CurvatureFlow(image1=imgT2Original,
                                      timeStep=0.125,
                                      numberOfIterations=5)

help.sitk_show(SimpleITK.Tile(imgT1Smooth[:, :, idxSlice],
                         imgT2Smooth[:, :, idxSlice],
                         (2, 1, 0)))