import sys
import os
import subprocess
import ctypes
import json

from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from ui_py import maingui
from ui_py import settings

COMPANY_NAME = "goonteam"
APP_NAME = "goonsrb2launcher"

ui_folder = "ui"
image_folder = "img"
profiles_folder = "profiles"
default_profile = os.path.join(profiles_folder, "default.json")


# create profiles folder
try:
    os.mkdir(profiles_folder)
except FileExistsError:
    print("Already a profiles folder")

# then default profile

try:
    temp_prof_file = open(default_profile, "r")
    temp_prof_data = temp_prof_file.read()
    temp_prof_file.close()
    if temp_prof_data.strip() == "":
        os.remove(default_profile)
except FileNotFoundError:
    print("idk")

if not os.path.exists(default_profile):
    with open(default_profile, "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "srb2_executable": ""
            }, indent=4))

    

data_file = open(default_profile, "r+")
json_data = json.load(data_file)
srb2_file = json_data["srb2_executable"]
srb2_dir = os.path.join(srb2_file, "..")

def update_information():
    global srb2_dir
    global srb2_file
    data_file = open(default_profile, "r")
    real_data = json.loads(data_file.read())
    srb2_file = real_data["srb2_executable"]
    srb2_dir = os.path.join(real_data["srb2_executable"], "..")

def update_executable_file(new_executable):
    data_file = open(default_profile, "r+")
    json_data = json.loads(data_file.read())
    data_file.close()
    json_data["srb2_executable"] = new_executable
    data_file = open(default_profile, "w")
    data_file.write(json.dumps(json_data, indent=4))
    data_file.close()
    update_information()
    

# taken from stakcoverflow for the icon
myappid = u"veryrealgooncorp.goonlaunch.forsrb2.69420" # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class SettingsDialog(settings.Ui_Dialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)

        self.selectLocation.clicked.connect(self.select_file)
        self.srb2Location.setText(srb2_file)

    def select_file(self):
        self.srb2Location.setText(QFileDialog.getOpenFileName()[0])

class Launcher(maingui.Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.playButton.clicked.connect(self.play)
        self.actionSettings.triggered.connect(self.open_settings)

    def play(self):
        if srb2_file:
            os.chdir(srb2_dir)
            subprocess.Popen(srb2_file)

    def open_settings(self):
        dialog = QDialog()
        dialog_ui = SettingsDialog()
        dialog_ui.setupUi(dialog)
        dialog.setWindowTitle("goonsrb2launcher | settings")
        dialog.setWindowIcon(QtGui.QIcon(os.path.join(image_folder, "goonapplogo.png")))
        if dialog.exec():
            global srb2_file
            global srb2_dir
            print("user said ok")
            update_executable_file(dialog.srb2Location.text())


def main(): # c ahh programming
    app = QApplication(sys.argv)
    window = QMainWindow()
    app_ui = Launcher()
    app_ui.setupUi(window)
    window.setWindowTitle("goonsrb2launcher")
    window.setWindowIcon(QtGui.QIcon(os.path.join(image_folder, "goonapplogo.png")))
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()