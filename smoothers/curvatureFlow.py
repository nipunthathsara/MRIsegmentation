import SimpleITK
import numpy

class CurvatureFlow:
    def applycFlow(self, original):
        return SimpleITK.CurvatureFlow(original, timeStep=0.125, numberOfIterations=5)
        print('Select modality')