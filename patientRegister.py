import tkFileDialog
import tkMessageBox
import os


class Register:
    patientDirectory = ''

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