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

smoothedImg = SimpleITK.CurvatureFlow(t1, timeStep = 0.125, numberOfIterations = 8)


#Results
#Fixed TimeStep = 1 Iterations = x
# x = 0 less smoothing
# x = 1 more smoothing => Decrease timeStep
# TimeStep = 0.5
# x = 0 less smoothing
# x = 1 more smoothing => Decrease timeStep
# TimeStep = 0.25
# x = 0 less smoothing
# x = 1 average smoothing
# x = 2 average smoothing++
# x = 3 average smoothing++
# x = 4 average smoothing++
# x = 5 average smoothing++
# x = 10 more smoothing
# TimeStep = 0.125
# x = 0 less
# x = 1 less
# x = 2 less
# x = 3 less
# x = 4 fair
# x = 5 fair
# x = 6 fair
# x = 7 starting to over smooth
# x = 8 starting to over smooth



disp(smoothedImg[:, :, 26])
