import SimpleITK
import tkMessageBox
import os
import numpy
import matplotlib.pyplot
import string


class Feed:

    def readImage(self, subDir, fileName):
        filePath = subDir + '/' + fileName + '.mhd'
        try:
            image = SimpleITK.ReadImage(str(filePath))
            return image
        except:
            tkMessageBox.showerror("Load failed", "failed to read image \n'%s'" % filePath)