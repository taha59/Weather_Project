# importing the libraries

# import sys
# #from tkinter import *
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QMessageBox, QWidget 
# from PyQt5.QtGui import QPixmap
# from PyQt5 import QtWidgets, QtGui, QtCore

# importing the libraries
import sys, requests, json, pytz
from tkinter import *
from tkinter import messagebox
from BlurWindow.blurWindow import blur

from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, QFile, QTextStream
from PyQt5.QtWidgets import QMenu, QToolBar, QMenuBar, QAction, QComboBox, QApplication, QGridLayout, QMainWindow, QDialog, QLabel, QRadioButton, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QMessageBox, QWidget, QHBoxLayout, QDesktopWidget
from PyQt5.QtGui import QImage, QPalette, QBrush, QColor
from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import datetime, date
import calendar

from qt_material import apply_stylesheet


from requests import api
from requests.models import to_native_string
#from PyQt5.QtGui import QCursor

# Enter your API key here
api_key = "a999316560f7b42e09c0a94e042ec53d"
 
# base_url variable to store url
base_url_weather = "http://api.openweathermap.org/data/2.5/onecall?"
base_url_geocode = "http://api.openweathermap.org/geo/1.0/direct?q="
unitSetFlag = "default"
introFlag = 0
    
class Weather_Alert_Window(QWidget):
    
    def __init__(self, alerts):
        super().__init__()
    
            
        self.alert_description_label = QtWidgets.QLabel(self)
        self.alert_source_label = QtWidgets.QLabel(self)

        alert_description = alerts[0]['description']
        alert_source = alerts[0]['sender_name']

        self.alert_source_label.setText(f"Alerts source:\n {alert_source}")
        self.getStyle(self.alert_source_label, 10, 'Time', "color:red;", 200, 0)

        self.alert_description_label.setText(f"Weather Alerts:\n {alert_description}")
        self.getStyle(self.alert_description_label, 10, 'Time', "color:red;", 200, 100)
    
        
    def getStyle (self, label, font_size,font_type, styleString, move_x, move_y):
        label.setFont(QFont(font_type,font_size))
        label.setStyleSheet(styleString)
        label.adjustSize()

        label.move(move_x, move_y)
    
    

class MyWindow(QMainWindow, QScrollArea):
    def __init__(self):
        super().__init__()

        #weather alert window flag intialized to 0 because it doesnt exist yet
        self.weather_alert_window_flag = 0

        # Force the style to be the same on all OSs:
        app.setStyle("Fusion")
        self._createMenuBar()

        screen = app.primaryScreen()

        rect = screen.availableGeometry()

        # perform math for the window change based on screen resolution
        self.x = rect.width() - 1855 # = 65
        self.y = rect.height() - 924 # = 96
        self.w = rect.width() - 440
        self.h = rect.height() - 120  

        self.x1 = rect.width()
        self.y1 = rect.height()
        self.seperate = rect.width() / 7 
        self.adjust_center = rect.width() / 2

        self.user_city_temp = ""
        self.setWindowTitle("Weather")

        self.setWindowIcon(QtGui.QIcon('image/appLogo.jpg'))

        self.settings = QSettings('teamAlpha', 'weather')
        if (self.settings.value('Theme') == "dark"):
            background = "./backgroundimage/darkThemeBackground.jpg"
        else:
            background = "./backgroundimage/DefaultBackground.jpg"
        oImage = QImage(background)
        screen = app.primaryScreen()
        sImage = oImage.scaled(screen.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        
        keys = self.settings.allKeys()
        if not keys:
            global introFlag
            introFlag = 1
            self.runIntro()
        else:
            self.loadMainWeatherWindow()
            

            #this buttons when selected will call the select function to run each if statement to determine light or dark mode
    def _createMenuBar(state):
        state.statusbar = state.statusBar()
        state.statusbar.showMessage('Ready')

        menubar = state.menuBar()
        viewMenu = menubar.addMenu('Options')

        viewStatAct = QAction('Options statusbar', state, checkable=True)
        viewStatAct.setStatusTip('Options statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(state.toggleMenu)

        viewMenu.addAction(viewStatAct)

        state.setGeometry(300, 300, 300, 200)
        state.setWindowTitle('Check menu')
        #state.statusbar.show()

    def toggleMenu(self, states):

        if states:
            self.statusbar.show()
        else:
            self.statusbar.hide()

        # Creating menus using a title
        # editMenu = menuBar.addMenu("&Edit")
        # helpMenu = menuBar.addMenu("&Help")
        
    # def _createToolBars(self):
    #     # Using a title
    #     fileToolBar = self.addToolBar("File")
    #     # Using a QToolBar object
    #     editToolBar = QToolBar("Edit", self)
    #     self.addToolBar(editToolBar)
    #     # Using a QToolBar object and a toolbar area
    #     helpToolBar = QToolBar("Help", self)
    #     self.addToolBar(Qt.LeftToolBarArea, helpToolBar)

    def setWindowSize(self):
        self.setGeometry(self.x, self.y, self.w, self.h) 
        self.setMinimumSize(700, 860)

        self.scroll = QScrollArea()           
        self.widget = QWidget()              
        self.layout = QVBoxLayout(self.widget)
        self.layout.setAlignment(Qt.AlignTop)
        

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        self.center()

    def initUI(self):
        # set the size of the app -> win.setGeometry(xpos, ypos, width, height)
       
        self.setWindowSize()
        self.radiobutton = QtWidgets.QRadioButton(self)
        self.radiobutton.setText("LightTheme")
        self.radiobutton.move(5, 50) # x pos y pos
        self.radiobutton.show()
        self.radiobutton2 = QtWidgets.QRadioButton(self)
        self.radiobutton2.setText("DarkTheme")
        self.radiobutton2.move(5, 70) # x pos y pos
        self.radiobutton2.show()

        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setText("Set as Home")
        self.saveButton.move(380, 20) # x pos y pos
        self.saveButton.setStyleSheet("border: 1px solid black;border-radius: 50%;color: black;background: white;")
        self.saveButton.show()

        self.homeButton = QtWidgets.QPushButton(self)
        self.homeButton.setText("Go Back Home")
        self.homeButton.move(479, 20) # x pos y pos
        self.homeButton.setStyleSheet("border: 1px solid black;border-radius: 50%;color: black;background: white;")
        self.homeButton.show()
        
        # Create label
        self.label = QtWidgets.QLabel(self)
        self.label.show()
        self.city_name = QtWidgets.QLabel(self)
        self.city_name.show()
        self.id = QtWidgets.QLabel(self)
        self.id.show()
        self.temp = QtWidgets.QLabel(self)
        self.temp.show()
        self.feel_like = QtWidgets.QLabel(self)
        self.feel_like.show()
        self.humidity = QtWidgets.QLabel(self)
        self.humidity.show()
        self.pressure = QtWidgets.QLabel(self)
        self.pressure.show()
        self.weather_report = QtWidgets.QLabel(self)
        self.weather_report.show()
        self.weather_report_icon = QtWidgets.QLabel(self)
        self.weather_report_icon.show()
        self.wind_speed = QtWidgets.QLabel(self)
        self.wind_speed.show()
        self.time_zone = QtWidgets.QLabel(self)
        self.time_zone.show()
        self.visibility_t = QtWidgets.QLabel(self)
        self.visibility_t.show()
        self.dew_point = QtWidgets.QLabel(self)
        self.dew_point.show()
        self.daily_label = QtWidgets.QLabel(self)
        self.daily_label.show()
        self.dt = QtWidgets.QLabel(self)
        self.dt.show()
        self.favoriteLabel = QtWidgets.QLabel(self)
        self.favoriteLabel.show()
        self.hourly_label = QtWidgets.QPushButton(self)
        self.hourly_label.show()
        self.check_hourly = QtWidgets.QLabel(self)
        self.check_hourly.show()

        self.dt_num = [0] * 7
        self.daily_temp_min = [0] * 7
        self.daily_temp_max = [0] * 7
        self.daily_report_icon = [0] * 7
        self.hourly_temp = [0] * 20
        self.hourly_report_icon = [0] * 20
        self.hourly_weather_report = [0] * 20
        self.hourly_time = [0] * 20
        for i in range(7):
            self.dt_num[i] = QtWidgets.QLabel(self)
            self.daily_temp_min[i] = QtWidgets.QLabel(self)
            self.daily_temp_max[i] = QtWidgets.QLabel(self)
            self.daily_report_icon[i] = QtWidgets.QLabel(self)
            self.dt_num[i].show()
            self.daily_temp_min[i].show()
            self.daily_temp_max[i].show()
            self.daily_report_icon[i].show()
        for i in range(20):
            self.hourly_temp[i] = QtWidgets.QLabel(self)
            self.hourly_report_icon[i] = QtWidgets.QLabel(self)
            self.hourly_weather_report[i] = QtWidgets.QLabel(self)
            self.hourly_time[i] = QtWidgets.QLabel(self)
            self.hourly_temp[i].show()
            self.hourly_report_icon[i].show()
            self.hourly_weather_report[i].show()
            self.hourly_time[i].show()
        self.daily_weather = QtWidgets.QLabel(self)
        self.daily_weather.show()
        self.hourly_weather = QtWidgets.QLabel(self)
        self.daily_weather.show()
        self.error = QtWidgets.QLabel(self)
        self.error.show()

       # self.update()
        self.label.move(600,40) # x pos y pos

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(100, 20) # x pos y pos
        self.textbox.resize(280,30)
        self.textbox.show()

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QRect(100, 50, 280, 40))
        self.comboBox.setObjectName("Unit Selection")
        
        global unitSetFlag
        if (self.settings.value('defaultUnits') == "Celsius"):
            self.comboBox.addItem("Celsius")   
            self.comboBox.addItem("Fahrenheit")
            self.comboBox.addItem("Kelvin")
        elif (self.settings.value('defaultUnits') == "Kelvin"):
            self.comboBox.addItem("Kelvin") 
            self.comboBox.addItem("Fahrenheit")
            self.comboBox.addItem("Celsius")
        else:
            self.comboBox.addItem("Fahrenheit")
            self.comboBox.addItem("Celsius")
            self.comboBox.addItem("Kelvin") 
        self.comboBox.show()
        #Create button
        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setText("Search City")
        self.searchButton.move(0, 20) # x pos y pos

        #Binds button shortcut to enter key
        self.searchButton.setShortcut("Return")
        self.searchButton.setStyleSheet("border: 1px solid black;border-radius: 50%;color: black;background: white;")
        self.center()
        self.searchButton.show()

        self.clearSettingsButton = QtWidgets.QPushButton(self)
        self.clearSettingsButton.setText("Reset Defaults")
        self.clearSettingsButton.move(578, 20)
        self.clearSettingsButton.setToolTip('Resets all app settings. Changes will take effect after reboot')
        self.clearSettingsButton.show()
        self.show()

    def getLightPalette(self):
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        return palette

    def getDarkPalette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        return palette
    
    def select(self):
        if self.radiobutton.isChecked():
            palette = QPalette()    
            palette = self.getLightPalette()
            app.setPalette(palette)
            self.setButtonsLight()
            if not self.city_name.text():
                self.changeToDefaultBackground()
        if self.radiobutton2.isChecked():
            palette = QPalette()
            palette = self.getDarkPalette()
            app.setPalette(palette)
            self.setButtonsDark()
            if not self.city_name.text():
                self.changeToDarkBackground()

    def setButtonsLight(self):
        self.switch_mode(self.searchButton, self.saveButton, self.homeButton, self.hourly_label, ":background-color: #FFFFFF")

    def setButtonsDark(self):
        self.switch_mode(self.searchButton, self.saveButton, self.homeButton, self.hourly_label, ":background-color: #3A4055")

    def switch_mode(self, searchButton, saveButton, homeButton, hourly_label, c_color):
        searchButton.setStyleSheet(c_color)
        saveButton.setStyleSheet(c_color)
        homeButton.setStyleSheet(c_color)
        hourly_label.setStyleSheet(c_color)

    def themeDefault(self):
        if self.launchThemeDark.isChecked():
            palette = QPalette()
            palette = self.getDarkPalette()
            app.setPalette(palette)
            self.confirmButton.setStyleSheet(":background-color: #3A4055")
            self.settings.setValue('Theme', "dark")
            self.changeToDarkBackground()

        if self.launchThemeLight.isChecked():
            palette = QPalette()
            palette = self.getLightPalette()
            app.setPalette(palette)

            self.settings.setValue('Theme', "light")
            self.confirmButton.setStyleSheet(":background-color: #FFFFFF")
            self.changeToDefaultBackground()
            
    def changeToDarkBackground(self):
            background = "./backgroundimage/darkThemeBackground.jpg"
            self.change_background(background)
    def changeToDefaultBackground(self):
            background = "./backgroundimage/DefaultBackground.jpg"
            self.change_background(background)

    def change_background(self, background_URL):
        background = background_URL
        oImage = QImage(background)
        screen = app.primaryScreen()
        sImage = oImage.scaled(screen.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def loadMainWeatherWindow(self):
        self.initUI()
        self.checkSettings()
        self.comboBox.activated[str].connect(self.comboClicked) 
        self.searchButton.clicked.connect(self.clicked)
        self.hourly_label.clicked.connect(self.hourly_clicked)
        self.saveButton.clicked.connect(self.saveEvent)
        self.homeButton.clicked.connect(self.homeEvent)
        self.clearSettingsButton.clicked.connect(self.clearSettings)

        self.radiobutton.toggled.connect(self.select)
        self.radiobutton2.toggled.connect(self.select)

    def clearSettings(self):
        self.settings.clear()

    def checkSettings(self):
        global unitSetFlag
        if (self.settings.value('defaultUnits') == "Kelvin"):
            unitSetFlag = "Kelvin"
        if (self.settings.value('defaultUnits') == "Celsius"):
            unitSetFlag = "Celsius"
        if (self.settings.value('defaultUnits') == "fahrenheit"):
            unitSetFlag = "fahrenheit"
        if (self.settings.value('UserCity') != None):
                self.runSavedCity()
        if (self.settings.value('Theme') != None):
            if (self.settings.value('Theme') == "dark"):
                palette = QPalette()
                palette = self.getDarkPalette()
                app.setPalette(palette)
                self.setButtonsDark()
            else:
                palette = QPalette()
                palette = self.getLightPalette()
                app.setPalette(palette)
                self.setButtonsLight()
        
    def testAndShow(self):
        complete_geo_url = base_url_geocode + (self.launchCityTextbox.text()) + "&limit=1&appid=" + api_key

        response = requests.get(complete_geo_url)
        geo_data = response.json()
        if response.status_code == 200:
            if len(geo_data) != 0:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']
                name = geo_data[0]['name']
                if unitSetFlag == ("Kelvin"):
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Kelvin" + "&exclude=minutely" + "&appid=" + api_key)
                elif unitSetFlag == ("Celsius"):
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Metric" + "&exclude=minutely" + "&appid=" + api_key)
                else:
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Imperial" + "&exclude=minutely" + "&appid=" + api_key)
                
                response = requests.get(complete_url)
                if response.status_code == 200:
                    if (geo_data[0]['country'] == "US"):
                        self.launchCityTextbox.setText(f"{name}, {geo_data[0]['state']}")
                    else:
                        self.launchCityTextbox.setText(f"{name}, {geo_data[0]['country']}")
                self.settings.setValue('userCity', name)
                self.setCheckIconLabel()
            else:
                self.setXiconLabel()
                self.settings.remove("userCity")  
        else:
            self.setXiconLabel()
            self.settings.remove("userCity")

    def setXiconLabel(self):
            self.im = QPixmap("./image/xIcon.png")
            self.cityNotFoundLabel.setPixmap(self.im)
            self.cityNotFoundLabel.setScaledContents( True )
            self.cityNotFoundLabel.setGeometry(40,40,40,40)
            self.cityNotFoundLabel.move(375,-4)

    def setCheckIconLabel(self):
            self.im = QPixmap("./image/checkIcon.png")
            self.cityNotFoundLabel.setPixmap(self.im)
            self.cityNotFoundLabel.setScaledContents( True )
            self.cityNotFoundLabel.setGeometry(30,30,30,30)
            self.cityNotFoundLabel.move(379,0)

    def runIntro(self):
        self.setWindowSize()
        self.initIntro()
        
        
        self.testValidCityButton.clicked.connect(self.testAndShow)
        self.defaultUnits.activated[str].connect(self.setLaunchUnits)
        self.confirmButton.clicked.connect(self.confirmSettings)
        self.launchThemeLight.toggled.connect(self.themeDefault)
        self.launchThemeDark.toggled.connect(self.themeDefault)

    def initIntro(self):
        self.cityNotFoundLabel = QtWidgets.QLabel(self)
        self.confirmButton = QtWidgets.QPushButton(self)
        self.confirmButton.setText("Confirm Settings")
        self.confirmButton.move(0,120)

        self.launchThemeLight = QtWidgets.QRadioButton(self)
        self.launchThemeLight.setText("LightTheme Default")
        self.launchThemeLight.move(5, 65) # x pos y pos
        self.launchThemeLight.adjustSize()
        self.launchThemeLight.show()
        self.launchThemeDark = QtWidgets.QRadioButton(self)
        self.launchThemeDark.setText("DarkTheme Default")
        self.launchThemeDark.move(5, 90) # x pos y pos
        self.launchThemeDark.adjustSize()
        self.launchThemeDark.show()

        self.defaultUnits = QComboBox(self)
        self.defaultUnits.setGeometry(QRect(0, 30, 100, 30))
        self.defaultUnits.setObjectName("Unit SelectdefaultUnits")
        self.defaultUnits.addItem("Fahrenheit")
        self.defaultUnits.addItem("Celsius")
        self.defaultUnits.addItem("Kelvin")
        self.defaultUnits.show()

        self.launchCityTextbox = QLineEdit(self)
        self.launchCityTextbox.move(100, 0) # x pos y pos
        self.launchCityTextbox.resize(280,30)
        self.launchCityTextbox.show()
        

        self.testValidCityButton = QtWidgets.QPushButton(self)
        self.testValidCityButton.setText("Set as Launch City")
        self.testValidCityButton.move(0,0)
        self.testValidCityButton.setShortcut("Return")
        self.testValidCityButton.setToolTip('App will show this location on launch')
        
        self.show()

    def clearIntro(self):
        self.confirmButton.deleteLater()
        self.testValidCityButton.deleteLater()
        self.launchThemeDark.deleteLater()
        self.launchThemeLight.deleteLater()
        self.defaultUnits.deleteLater()
        self.cityNotFoundLabel.clear()

    def confirmSettings(self):
        self.clearIntro()
        self.loadMainWeatherWindow()
        global introFlag
        introFlag = 0
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def getWeather_Alert(self, data):
        
        #check if the alerts dict block exists in data. if it does then proceed to display the weather alerts
        if 'alerts' in data:
            alerts = data['alerts']

        else:
            return

        self.weather_alert_window = Weather_Alert_Window(alerts)

        #a flag that indicates if window has been initialized 
        # set flag = 1 after intializing
        self.weather_alert_window_flag = 1
    
        self.weather_alert_window.show()

    def resizeEvent(self, event):
        global introFlag
        if (introFlag == 0):
            self.city_name.move(self.rect().center().x()-139, self.city_name.y())
            self.temp.move(self.rect().center().x()-80, self.temp.y()) 
            self.weather_report.move(self.rect().center().x()-79, self.weather_report.y())
            self.humidity.move(self.rect().center().x()- 270, self.humidity.y())
            self.pressure.move(self.rect().center().x()-79, self.pressure.y())
            self.weather_report_icon.move(self.rect().center().x()- 250, self.weather_report_icon.y())
            self.feel_like.move(self.rect().center().x()-(-170), self.feel_like.y())
            self.wind_speed.move(self.rect().center().x()- 330, self.wind_speed.y())  
            self.visibility_t.move(self.rect().center().x() - 79, self.visibility_t.y())
            self.dew_point.move(self.rect().center().x() - (-170), self.dew_point.y())
            width = (self.city_name.fontMetrics().boundingRect(self.city_name.text()).width())
            self.favoriteLabel.move((self.rect().center().x() - 139+width+15), self.favoriteLabel.y())
        QMainWindow.resizeEvent(self, event)

    def saveEvent(self):
        if self.city_name.text():
            newText = self.city_name.text()[0:-4] 
            self.settings.setValue('userCity', newText)
            self.createFavoriteLabel()

    def homeEvent(self):
        if (self.settings.value('userCity') != None):
            self.showCity(self.settings.value('userCity'))

    def createFavoriteLabel(self):
        self.im = QPixmap("./image/favorite.png")
        self.favoriteLabel.setPixmap(self.im)
        self.favoriteLabel.setScaledContents( True )
        self.favoriteLabel.setGeometry(40,40,40,40)
        width = (self.city_name.fontMetrics().boundingRect(self.city_name.text()).width())
        self.favoriteLabel.move(self.city_name.x() + width + 15, 240)

    def setLaunchUnits(self, unit):
        global unitSetFlag
        if unit == ("Kelvin"):
            unitSetFlag = "Kelvin"
            self.settings.setValue('defaultUnits', "Kelvin")
        elif unit == ("Celsius"):
            unitSetFlag = "Celsius"
            self.settings.setValue('defaultUnits', "Celsius")
        else:
            unitSetFlag = "fahrenheit"
            self.settings.setValue('defaultUnits', "fahrenheit")

    def comboClicked(self, unit):
         global unitSetFlag
         location = self.city_name.text()[0:-4]
         if unit == ("Kelvin"):
            unitSetFlag = "Kelvin"
            self.showCity(location)
         elif unit == ("Celsius"):
            unitSetFlag = "Celsius"
            self.showCity(location)
         else:
            unitSetFlag = "fahrenheit"
            self.showCity(location)

    def hourly_clicked(self):
        self.magician = AnotherWindow(self.user_city_temp)
        self.magician.show()

    def clicked(self):
        #if a flag = 1 or if the window is initialized
        if self.weather_alert_window_flag == 1:

            #if window already exists close it and set its flag to 0 because it doesnt exist anymore
            if self.weather_alert_window != None:
                self.weather_alert_window.close()
                self.weather_alert_window_flag = 0
                
        self.showCity(self.textbox.text())

    def getStyle (self, label, font_size,font_type, styleString, move_x, move_y):
        label.setFont(QFont(font_type,font_size))
        label.setStyleSheet(styleString)
        label.adjustSize()

        label.move(move_x, move_y)

    def getDaily_report(self, label, daily_report_icon,x, y, w, h, move_x, move_y):
        daily_report_icon.setPixmap(label)
        daily_report_icon.setScaledContents( True )
        daily_report_icon.setGeometry(x,y,w,h)
        daily_report_icon.move(move_x, move_y)

    def runSavedCity(self):
        
        self.showCity(self.settings.value('userCity'))

    def showCity(self, userCityName = ""):
        
        self.update() # Update to get the full text
        
        # complete_geo_url variable to get coordinates for location
        complete_geo_url = base_url_geocode + userCityName + "&limit=1&appid=" + api_key

        response = requests.get(complete_geo_url)
        geo_data = response.json()

        if response.status_code == 200:
            #access coordinates and name from Geocoding API, this is stored in a dictionary variable
            if len(geo_data) != 0:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']
                name = geo_data[0]['name']
                #Use coordinates above to search for information from Onecall API
                if unitSetFlag == "Kelvin":
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Kelvin" + "&exclude=minutely" + "&appid=" + api_key)
                elif unitSetFlag == "Celsius":
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Metric" + "&exclude=minutely" + "&appid=" + api_key)
                else:
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Imperial" + "&exclude=minutely" + "&appid=" + api_key)
                # Sending HTTP request
                response = requests.get(complete_url)
                # checking the status code of the request
                if response.status_code == 200:
                    # retrieving data in the json format
                    data = response.json()
                    
                    # take the 'current' dict block in api code
                    current = data['current']
                    daily = data['daily']
                    hourly = data['hourly']

                    #call weather alerts
                    self.getWeather_Alert(data)

                    self.user_city_temp = userCityName


                    # getting temperature
                    temperature = current['temp']
                    # getting feel like
                    temp_feel_like = current['feels_like']  
                    # getting the humidity
                    humidity = current['humidity']
                    # getting the pressure
                    pressure = current['pressure']
                    # weather report
                    weather_report = current['weather'][0]['main']
                    # wind report
                    wind_report = current['wind_speed']
                    #visibility
                    visibility_t = current['visibility']
                    #dew_point
                    dew_point = current['dew_point']
                    #

                    #get all of element in daily struct (for loop)
                    dt = [element['dt'] for element in daily]
                    daily_temp_min = [element['temp']['min'] for element in daily]
                    daily_temp_max = [element['temp']['max'] for element in daily]
                    daily_weather = [element['weather'][0]['icon'] for element in daily]   

                    hourly_temp = [element['temp'] for element in hourly]
                    hourly_FL = [element['feels_like'] for element in hourly]
                    hourly_weather = [element['weather'][0]['icon'] for element in hourly]
                    hourly_weather_condition = [element['weather'][0]['description'] for element in hourly]
                    hourly_time = [element['dt'] for element in hourly]
                    hourly_pressue = [element['feels_like'] for element in hourly]
                    hourly_humidity = [element['humidity'] for element in hourly]
                    hourly_visibility = [element['visibility'] for element in hourly]
                    hourly_wind_speed = [element['wind_speed'] for element in hourly]

                    c_time = [0] * 20
                    # 7-days forcast
                    for i in range(7):
                        dt[i] = datetime.fromtimestamp(dt[i]).strftime('%a %d')
                    for i in range(20):
                        hourly_time[i] = datetime.fromtimestamp(hourly_time[i]).strftime('%I %p')
                        c_time[i] = hourly_time[i]
                    self.error.clear()

                    self.city_name.setGeometry(600,55,300,24)
                    if (geo_data[0]['country'] == "US"):
                        self.city_name.setText(f"{name}, {geo_data[0]['state']}")
                        self.textbox.setText(f"{name}, {geo_data[0]['state']}")
                    else:
                        self.city_name.setText(f"{name}, {geo_data[0]['country']}")
                        self.textbox.setText(f"{name}, {geo_data[0]['country']}")

                    newLocation = (self.rect().center() - QPoint(139,400))
                    self.getStyle(self.city_name, 30, 'Times',"color: white;", newLocation.x(), 239)


                    newLocation = (self.rect().center()-QPoint(80,350))
                    self.temp.setText(f"{round(temperature)}\N{DEGREE SIGN}")
                    self.getStyle(self.temp, 60,'Times', "color:white;", newLocation.x(), 289)

                    self.weather_report.setText(f" {weather_report}")
                    newLocation = (self.rect().center()-QPoint(79,200))
                    self.getStyle(self.weather_report,17, 'Time', "color:white;", newLocation.x(), 439)

                    self.humidity.setText(f"Humidity {humidity}%")
                    newLocation = (self.rect().center()-QPoint(270,155))
                    self.getStyle(self.humidity, 11, 'Times',"color:white;", newLocation.x(), 484)

                    self.pressure.setText(f"Pressure {pressure} mbar")
                    newLocation = (self.rect().center()-QPoint(79,155))
                    self.getStyle(self.pressure, 11,'Times', "color:white;", newLocation.x(), 484)

                    self.feel_like.setText(f"Feels Like {round(temp_feel_like)} \N{DEGREE SIGN}")
                    newLocation = (self.rect().center()-QPoint(-170,155)) 
                    self.getStyle(self.feel_like, 11,'Times', "color:white;", newLocation.x(), 484)

                    self.wind_speed.setText(f"Wind Speed {round(wind_report)} mph")
                    newLocation = (self.rect().center()-QPoint(330,100))
                    self.getStyle(self.wind_speed, 11,'Times', "color:white;", newLocation.x(), 539)

                    calculate_visibility = visibility_t / 1000
                    convert_to_miles = calculate_visibility / 0.621371
                    self.visibility_t.setText(f"Visibility {round(convert_to_miles)} mi")
                    newLocation = (self.rect().center() -QPoint (79, 100))
                    self.getStyle(self.visibility_t, 11,'Times', "color:white;", newLocation.x(), 539)

                    self.dew_point.setText(f"Dew Point {round(dew_point)} \N{DEGREE SIGN}")
                    newLocation = (self.rect().center() - QPoint(-170, 100))
                    self.getStyle(self.dew_point, 11, 'Times', "color:white;", newLocation.x(), 539)

                    #display weather icon based on api weather report code
                    weatherCode = current['weather'][0]['icon']
                    icon = "./image/" + weatherCode + ".png"
                    backgroundImage = "./backgroundimage/" + weatherCode + ".jpg"
                    oImage = QImage(backgroundImage)
                    screen = app.primaryScreen()
                    sImage = oImage.scaled(screen.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
                    palette = QPalette()
                    palette.setBrush(QPalette.Window, QBrush(sImage))
                    self.setPalette(palette)

                    self.im = QPixmap(icon)
                    self.weather_report_icon.setPixmap(self.im)
                    self.weather_report_icon.setScaledContents( True )
                    self.weather_report_icon.setGeometry(150,150,150,150)
                    newLocation = (self.rect().center()-QPoint(250,350))
                    self.weather_report_icon.move(newLocation.x(), 289) 
                    
                    #hourly icon
                    hourly_label_icon = "./image/hourly.png"
                    #display weather icon based on daily api weather report code
                    daily_icon = [0] * 7
                    for i in range(7):
                        daily_icon[i] = "./image/" + daily_weather[i] + ".png"
                    
                    hourly_icon = [0] * 20
                    for i in range(20):
                        hourly_icon[i] = "./image/" + hourly_weather[i] + ".png"

                    # Minimum and Maximum temperature number
                    temp_min = [0] * 7
                    temp_max = [0] * 7
                    for i in range(7):
                        temp_min[i] = round(daily_temp_min[i])
                        temp_max[i] = round(daily_temp_max[i])
                    



                    self.dw = [0] * 7
                    move_daily = 0
                    temp = self.x1 - 50

                    self.daily_label.setText("Daily")
                    self.getStyle(self.daily_label, 17,'Times', "color:white;", self.x1 - temp, self.h - 230)
                    
                    for i in range(7):

                        move_dt_num_x = round((self.x1 - temp) + move_daily)
                        self.dt_num[i].setText(f"{dt[i]}")
                        self.getStyle(self.dt_num[i], 14,'Times', "color: white;", move_dt_num_x , self.h - 180)

                        move_icon_temp_x = move_dt_num_x - 5
                        self.dw[i] = QPixmap(daily_icon[i])
                        self.getDaily_report(self.dw[i],self.daily_report_icon[i],100, 100, 100, 100, move_icon_temp_x, self.h - 160)
                       
                        shift_temp_x = move_icon_temp_x
                       
                        self.daily_temp_max[i].setText(f"{temp_max[i]}\N{DEGREE SIGN}")
                        self.getStyle(self.daily_temp_max[i], 13,'Times', "color: white;", shift_temp_x, self.h - 80)
                        
                        self.daily_temp_min[i].setText(f"{temp_min[i]}\N{DEGREE SIGN}")
                        self.getStyle(self.daily_temp_min[i], 11,'Times', "color: white;", shift_temp_x + 50, self.h - 75)

                        move_daily += self.seperate
    
                    self.hourly_label.setText(f"Hourly")
                    self.getStyle(self.hourly_label, 13, 'Times', "color:black;", self.x1 - temp, self.h - 500 )


                    newText = self.city_name.text()[0:-4]
                    if (newText == self.settings.value('userCity')):
                        self.createFavoriteLabel()
                    else:
                        self.favoriteLabel.clear()
                    self.update() 
                    return backgroundImage, c_time, hourly_icon, hourly_weather_condition, hourly_temp, hourly_FL, hourly_pressue,hourly_humidity, hourly_visibility, hourly_wind_speed


            else:
                self.city_name.clear()
                self.id.clear() 
                self.temp.clear() 
                self.feel_like.clear() 
                self.humidity.clear() 
                self.pressure.clear()
                self.weather_report.clear() 
                self.weather_report_icon.clear()
                self.wind_speed.clear() 
                self.time_zone.clear()
                self.daily_label.clear() 
                self.dt.clear()
                self.visibility_t.clear()
                self.dew_point.clear()
                self.hourly_label.hide()
                #self.alert_description_label.clear()
                #self.alert_source_label.clear() 
                self.favoriteLabel.clear()
                for i in range(7):
                    self.dt_num[i].clear()
                    self.daily_report_icon[i].clear()
                    self.daily_temp_max[i].clear()
                    self.daily_temp_min[i].clear()
                for i in range(20):
                    self.hourly_temp[i].clear()
                    self.hourly_report_icon[i].clear()
                    self.hourly_weather_report[i].clear()
                    self.hourly_time[i].clear()
            # showing the error message if not real city name
                self.error.setText(f"The city you entered does not exist. Please enter a city name.")
                self.error.setFont(QFont('Times', 13))
                self.error.setStyleSheet("color: white;")
                self.error.adjustSize()
                self.error.move(600,55)

                background = "./backgroundimage/DefaultBackground.jpg"
                oImage = QImage(background)
                screen = app.primaryScreen()
                sImage = oImage.scaled(screen.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
                palette = QPalette()
                palette.setBrush(QPalette.Window, QBrush(sImage))
                self.setPalette(palette)
                self.update()

    def update(self):
        self.label.adjustSize()
        
class AnotherWindow(QWidget):
    def __init__(self, cityname):
        super().__init__()
        self.cityname = cityname
        self.setWindowTitle("Hourly")
        self.initUI_another()

    def brusing_backgroundImage(self, backgroundImage):
        oImage = QImage(backgroundImage)
        screen = app.primaryScreen()
        sImage = oImage.scaled(screen.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette) 

    def draw_a_H_bar(self, label, constant_x, change_this):
        label.setText(f"|")
        label.setStyleSheet('color:white')
        label.move(constant_x, change_this)

    def draw_a_V_bar(self, label, change_this, constant_y):
        label.setText(f"-")
        label.setStyleSheet('color:white')
        label.move(change_this, constant_y)


    def initUI_another(self):
        object_a = MyWindow()
        self.setGeometry(50, 50, object_a.w, object_a.h)

        background, c_time, icon, wc, h_temp, feels_, pressure, hum, vis, wind = object_a.showCity(self.cityname)
        self.brusing_backgroundImage(background)

        
        #hourly label for pop up window
        self.hourly_label = QtWidgets.QLabel(self)
        self.hourly_label.setText(f"HOURLY FORECAST - {self.cityname.upper()}")
        object_a.getStyle(self.hourly_label, 24, 'Times', 'color:white;', 400 , 100)

        self.temp_label = QtWidgets.QLabel(self)
        self.temp_label.setText(f"Temperature")
        object_a.getStyle(self.temp_label, 11, 'Times', 'color:white;', 10, 300)

        self.condition_label = QtWidgets.QLabel(self)
        self.condition_label.setText(f"Condition")
        object_a.getStyle(self.condition_label, 11, 'Times', 'color:white;', 10, 380 )

        self.feels_like_label = QtWidgets.QLabel(self)
        self.feels_like_label.setText(f"Feels Like")
        object_a.getStyle(self.feels_like_label, 11, 'Times', 'color:white;', 10 ,460)

        self.pressure_label = QtWidgets.QLabel(self)
        self.pressure_label.setText(f"Pressure")
        object_a.getStyle(self.pressure_label, 11, 'Times', 'color:white;', 10 ,540)

        self.humidity_label = QtWidgets.QLabel(self)
        self.humidity_label.setText(f"Humidity")
        object_a.getStyle(self.humidity_label, 11, 'Times', 'color:white;', 10 ,620)

        self.visibility_label = QtWidgets.QLabel(self)
        self.visibility_label.setText(f"Visibility")
        object_a.getStyle(self.visibility_label, 11, 'Times', 'color:white;', 10 ,700)

        self.wind_label = QtWidgets.QLabel(self)
        self.wind_label.setText(f'Wind Speed')
        object_a.getStyle(self.wind_label, 11, 'Times', 'color:white;', 10 ,780)

        self.hourly_time = [0] * 20
        self.hw = [0] * 20

        a = 220
        i = 0
        split = round(object_a.x1 / 10)
        array_num = 9
        temp = [0] * array_num
        self.hourly_report_icon = [0] * array_num
        self.hourly_condition = [0] * array_num
        self.hourly_temp = [0] * array_num
        self.hourly_feels_like = [0] * array_num
        self.hourly_pressure = [0] * array_num
        self.hourly_humidity = [0] * array_num
        self.hourly_visibility = [0] * array_num
        self.hourly_wind_speed = [0] * array_num

        for i in range (9):
            temp[i] = QtWidgets.QLabel(self)
            temp[i].setText(f" {c_time[i]}")
            object_a.getStyle(temp[i], 11, 'Times', 'color:white;', a, 180)
            
            self.hourly_report_icon[i] = QtWidgets.QLabel(self)
            self.hw[i] = QPixmap(icon[i])
            object_a.getDaily_report(self.hw[i], self.hourly_report_icon[i], 100, 100, 100, 100, a , 210)

            self.hourly_temp[i] = QtWidgets.QLabel(self)
            self.hourly_temp[i].setText(f"{round(h_temp[i])} \N{DEGREE SIGN}")
            object_a.getStyle(self.hourly_temp[i], 11, 'Times', 'color:white;', a + 20, 300)

            self.hourly_condition[i] = QtWidgets.QLabel(self)
            self.hourly_condition[i].setText(f"{wc[i]}")
            object_a.getStyle(self.hourly_condition[i], 11, 'Times', 'color:white;', a, 380)

            self.hourly_feels_like[i] = QtWidgets.QLabel(self)
            self.hourly_feels_like[i].setText(f"{round(feels_[i])} \N{DEGREE SIGN}")
            object_a.getStyle(self.hourly_feels_like[i], 11, 'Times', 'color:white;', a + 20, 460)

            self.hourly_pressure[i] = QtWidgets.QLabel(self)
            self.hourly_pressure[i].setText(f"{round(pressure[i])} mbar")
            object_a.getStyle(self.hourly_pressure[i], 11, 'Times', 'color:white;', a + 20, 540)

            self.hourly_humidity[i] = QtWidgets.QLabel(self)
            self.hourly_humidity[i].setText(f"{hum[i]}%")
            object_a.getStyle(self.hourly_humidity[i], 11, 'Times', 'color:white;', a + 20, 620)

            self.hourly_visibility[i] = QtWidgets.QLabel(self)
            self.hourly_visibility[i].setText(f"{round(vis[i] / 1000)} mi")
            object_a.getStyle(self.hourly_visibility[i], 11, 'Times', 'color:white;', a + 20, 700)

            self.hourly_wind_speed[i] = QtWidgets.QLabel(self)
            self.hourly_wind_speed[i].setText(f"{round(wind[i])} mph")
            object_a.getStyle(self.hourly_wind_speed[i], 11, 'Times', 'color:white;', a + 20, 780)

            a += split

        H_single_bar = [0] * 220
        num = 180
        for i in range (220):
            H_single_bar[i] = QtWidgets.QLabel(self)
            self.draw_a_H_bar(H_single_bar[i], 210, num)
            num += 3
        V_single_bar = [0] * 700
        num = 20
        for i in range (600):
            V_single_bar[i] = QtWidgets.QLabel(self)
            self.draw_a_V_bar(V_single_bar[i], num, 210)
            num += 4

    
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv) 
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())


window()

  
