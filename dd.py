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