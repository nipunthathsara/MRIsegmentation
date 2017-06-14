import tkFileDialog
import tkMessageBox
import os


class Register:
    #patientDirectory = ''

    def getPatient(self):
        patientDirectory = tkFileDialog.askdirectory(title='Choose patient')
        subDirs = [dI for dI in os.listdir(patientDirectory) if os.path.isdir(os.path.join(patientDirectory, dI))]
        if patientDirectory:
            try:
                print(patientDirectory)
                for a in subDirs:
                    print a
                    # App.directoryPathVar.set(directoryPathVar)
                return patientDirectory

            except:
                tkMessageBox.showerror("Open Source File", "Failed to read file \n'%s'" % patientDirectory)


    def getModality(selfself, patientDir, modality):
        if(patientDir):
            try:
                subDirs = [dI for dI in os.listdir(patientDir) if os.path.isdir(os.path.join(patientDir, dI))]
                for mod in subDirs:
                    if(mod == modality):
                        return mod

                return tkMessageBox.showerror("Open Source File", "Modality not found in \n'%s'" % patientDir)
            except:
                tkMessageBox.showerror("Open Source File", "Failed to read patient directory \n'%s'" % patientDir)
