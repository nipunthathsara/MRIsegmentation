import SimpleITK
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as tk

seeds = None

def show(image, frame, title = None, margin = 0.0, dpi = 100):
    toolbar = None
    canvas = None
    ax = None
    ndArray = None
    fig = None
    ndArray = SimpleITK.GetArrayFromImage(image)
    figsize = (5,5)#(1 + margin) * ndArray.shape[0] / dpi, (1 + margin) * ndArray.shape[1] / dpi
    # figsize = (1 + margin) * ndArray.shape[0] / dpi, (1 + margin) * ndArray.shape[1] / dpi
    # set fixed size to image
    extent = (0, ndArray.shape[1], ndArray.shape[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    plt.set_cmap("gray")
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])
    ax.imshow(ndArray)
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas, frame)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    return canvas

def callBack(event):
    print event.x, event.y
    seeds.append((event.xdata, event.ydata))
    if len(seeds) == 5:
        return seeds

def markSeeds(canvas):
    data = canvas.callbacks.connect('button_press_event', callBack)
    canvas.mpl_disconnect(data)
    return data

# def callback(event):
#     print event.xdata, event.ydata


