import SimpleITK
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as tk

cid = None

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print 'x = %d, y = %d' % (
        ix, iy)

    global coords
    coords.append((ix, iy))

    if len(coords) == 2:
        canvas.mpl_disconnect(cid)

    return coords

def markSeeds(canvas):
    print('gggg')
    cid = canvas.mpl_connect('button_press_event', onclick)



