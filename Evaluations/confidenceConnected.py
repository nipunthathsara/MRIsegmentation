import SimpleITK
import  matplotlib.pyplot as plt
import numpy


def disp(img, title=None, margin=0.0, dpi=40):
    nda = SimpleITK.GetArrayFromImage(img)
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    extent = (0, nda.shape[1], nda.shape[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])
    plt.set_cmap("gray")
    ax.imshow(nda, extent=extent, interpolation=None)
    if title:
        plt.title(title)
    plt.show()


fileT1 = ".././dataset/mr_T1/patient_109_mr_T1.mhd"
t1 = SimpleITK.ReadImage(fileT1)
fileT2 = ".././dataset/mr_T2/patient_109_mr_T2.mhd"
t2 = SimpleITK.ReadImage(fileT2)
# disp(t1[:, :, 26])

smoothedImg = SimpleITK.CurvatureFlow(t1, timeStep = 0.125, numberOfIterations = 5)

seeds = [(165, 178, 26),
            (98, 165, 26),
            (205, 125, 26),
            (173, 205, 26)]
gray = SimpleITK.ConfidenceConnected(image1=smoothedImg,
                                                seedList=seeds,
                                                numberOfIterations=1,
                                                multiplier= 1.0,
                                                replaceValue= 1)

disp(gray[:, :, 26])

# Results
# Iterations = 5 Fixed, X = multiplier
# x = 2.5 (Recommended)
# x = 3.0 less
# x = 2.0 getting better
# x = 1.5 getting better
# x = 1.0 Good
# x = 0.5 decreasing

#Multiplier 1.0 fixed, x = iterations
# x = 1 fair
# x = 3 fair
# x = 5 guessed value fair
# x = 7 fair
# x = 9 fair
# x = 11 fair
# x = 15 fair