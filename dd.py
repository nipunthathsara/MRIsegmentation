def onClickMarkSeeds(self):
    # print('ggggg')
    # self.seeds = help.markSeeds(self.canvas)
    # print('hhhhh')
    # print self.seeds
    self.seeds = [(165, 178, self.sliceNumber), (98, 165, self.sliceNumber), (205, 125, self.sliceNumber),
                  (173, 205, self.sliceNumber)]
    seedMarkedImg = SimpleITK.Image(self.t2_smoothned)
    for seed in self.seeds:
        seedMarkedImg[seed] = 10000

    Segmentor.tvFrame = None

    help.show(seedMarkedImg[:, :, self.sliceNumber], Segmentor.tvFrame)
    # Get seed array here


def sitk_tile_vec(self, lstImgs):
    lstImgToCompose = []
    for idxComp in range(lstImgs[0].GetNumberOfComponentsPerPixel()):
        lstImgToTile = []
        for img in lstImgs:
            lstImgToTile.append(SimpleITK.VectorIndexSelectionCast(img, idxComp))
        lstImgToCompose.append(SimpleITK.Tile(lstImgToTile, (len(lstImgs), 1, 0)))
    Segmentor.tvFrame = None
    Segmentor.tvFrame = tk.Frame(self)
    Segmentor.tvFrame = tk.Frame(self)
    help.show(SimpleITK.Compose(lstImgToCompose), Segmentor.tvFrame)


def onClickSegement(self, mod, matter):
    if (matter == 'Gray Matter'):
        if (mod == 'T1 and T2'):
            print('gg')
        else:
            print('hh')
            grayMatter = SimpleITK.ConfidenceConnected(image1=self.t1_smoothned,
                                                       seedList=self.seeds,
                                                       numberOfIterations=3,
                                                       multiplier=1,
                                                       replaceValue=self.grayLabel)
            # Segmentor.tvFrame = None
            # Segmentor.tvFrame = tk.Frame(self)
            t1SmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.t1_smoothned), grayMatter.GetPixelID())
            # help.show(SimpleITK.LabelOverlay(castedImg[:,:,self.sliceNumber], grayMatter), Segmentor.tvFrame)
            # help.show(grayMatter[:,:,self.sliceNumber],Segmentor.tvFrame)
            # help.show(grayMatter,Segmentor.tvFrame)
            # Segmentor.sitk_tile_vec([SimpleITK.LabelOverlay(t1SmoothInt[:,:,self.sliceNumber]),(grayMatter[:,:,self.sliceNumber])])

            """"This filter extracts a connected set of pixels whose pixel intensities are consistent
                    with the pixel statistics of a seed point. The mean and variance across a neighborhood (8-connected, 26-connected, etc.)
                    are calculated for a seed point. Then pixels connected to this seed point whose values are within the confidence interval
                    for the seed point are grouped. The width of the confidence interval is controlled by the "Multiplier" variable
                    (the confidence interval is the mean plus or minus the "Multiplier" times the standard deviation). If the intensity
                    variations across a segment were gaussian, a "Multiplier" setting of 2.5 would define a confidence interval wide enough
                    to capture 99% of samples in the segment.
                    After this initial segmentation is calculated, the mean and variance are re-calculated. All the pixels in the
                    previous segmentation are used to calculate the mean the standard deviation (as opposed to using the pixels in
                    the neighborhood of the seed point). The segmentation is then recalculated using these refined estimates for the
                    mean and variance of the pixel values. This process is repeated for the specified number of iterations.
                     Setting the "NumberOfIterations" to zero stops the algorithm after the initial segmentation from the seed point."""

            # creating rescaled t1_smoothed image. to overlap with graymatter.
            t1_smoothnedScaled = SimpleITK.Cast(SimpleITK.RescaleIntensity(self.t1_smoothned), grayMatter.GetPixelID())
            Segmentor.tvFrame = tk.Frame(self)
            Segmentor.tvFrame.grid(row=0, column=0, columnspan=4, rowspan=5)
            help.show(
                SimpleITK.LabelOverlay(t1_smoothnedScaled[:, :, self.sliceNumber], grayMatter[:, :, self.sliceNumber]),
                Segmentor.tvFrame)



            # elif(matter =='White matter'):
            #     if (mod == 'T1 and T2'):
            #         print('gg')
            #     else:
            #         print('hh')
            # elif (matter == 'All'):
            #     if (mod == 'T1 and T2'):
            #         print('gg')
            #     else:
            #         print('hh')