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
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QComboBox, QApplication, QGridLayout, QMainWindow, QDialog, QLabel, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QMessageBox, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5 import QtWidgets, QtGui
from datetime import datetime, date
import calendar

from requests import api
#from PyQt5.QtGui import QCursor

# Enter your API key here
api_key = "a999316560f7b42e09c0a94e042ec53d"
 
# base_url variable to store url
base_url_weather = "http://api.openweathermap.org/data/2.5/onecall?"
base_url_geocode = "http://api.openweathermap.org/geo/1.0/direct?q="
unitSetFlag = "default"
   
class MyWindow(QMainWindow, QScrollArea):
    def __init__(self):
        super().__init__()
        self.x = 65
        self.y = 96
        self.w = 1480
        self.h = 900       
        self.setWindowTitle("Weather")

        self.setWindowIcon(QtGui.QIcon('image/appLogo.jpg'))        
        background = "./backgroundimage/DefaultBackground.jpg"
        oImage = QImage(background)
        sImage = oImage.scaled(QSize(1480,900))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        
        self.initUI()
        self.comboBox.activated[str].connect(self.comboClicked) 
        self.button1.clicked.connect(self.clicked)
        
    def initUI(self):
        # set the size of the app -> win.setGeometry(xpos, ypos, width, height)
        self.setGeometry(self.x, self.y, self.w, self.h) 

        self.scroll = QScrollArea()           
        self.widget = QWidget()              
        
        self.setMinimumSize(840, 750)


        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        # Create label
        self.label = QtWidgets.QLabel(self)
        self.city_name = QtWidgets.QLabel(self)
        self.id = QtWidgets.QLabel(self)
        self.temp = QtWidgets.QLabel(self)
        self.feel_like = QtWidgets.QLabel(self)
        self.humidity = QtWidgets.QLabel(self)
        self.pressure = QtWidgets.QLabel(self)
        self.weather_report = QtWidgets.QLabel(self)
        self.weather_report_icon = QtWidgets.QLabel(self)
        self.wind_speed = QtWidgets.QLabel(self)
        self.time_zone = QtWidgets.QLabel(self)

        self.daily_label = QtWidgets.QLabel(self)
        self.dt = QtWidgets.QLabel(self)
        self.dt_0 = QtWidgets.QLabel(self)
        self.dt_1 = QtWidgets.QLabel(self)
        self.dt_2 = QtWidgets.QLabel(self)
        self.dt_3 = QtWidgets.QLabel(self)
        self.dt_4 = QtWidgets.QLabel(self)
        self.dt_5 = QtWidgets.QLabel(self)
        self.dt_6 = QtWidgets.QLabel(self)

        self.daily_temp_min = QtWidgets.QLabel(self)
        self.daily_temp_min_0 = QtWidgets.QLabel(self)
        self.daily_temp_min_1 = QtWidgets.QLabel(self)
        self.daily_temp_min_2 = QtWidgets.QLabel(self)
        self.daily_temp_min_3 = QtWidgets.QLabel(self)
        self.daily_temp_min_4 = QtWidgets.QLabel(self)
        self.daily_temp_min_5 = QtWidgets.QLabel(self)
        self.daily_temp_min_6 = QtWidgets.QLabel(self)


        self.daily_temp_max = QtWidgets.QLabel(self)
        self.daily_temp_max_0 = QtWidgets.QLabel(self)
        self.daily_temp_max_1 = QtWidgets.QLabel(self)
        self.daily_temp_max_2 = QtWidgets.QLabel(self)
        self.daily_temp_max_3 = QtWidgets.QLabel(self)
        self.daily_temp_max_4 = QtWidgets.QLabel(self)
        self.daily_temp_max_5 = QtWidgets.QLabel(self)
        self.daily_temp_max_6 = QtWidgets.QLabel(self)

        self.daily_report_icon_0 = QtWidgets.QLabel(self)
        self.daily_report_icon_1 = QtWidgets.QLabel(self)
        self.daily_report_icon_2 = QtWidgets.QLabel(self)
        self.daily_report_icon_3 = QtWidgets.QLabel(self)
        self.daily_report_icon_4 = QtWidgets.QLabel(self)
        self.daily_report_icon_5 = QtWidgets.QLabel(self)
        self.daily_report_icon_6 = QtWidgets.QLabel(self)

        self.testing_label = QtWidgets.QLabel(self) 

        self.daily_weather = QtWidgets.QLabel(self)
        self.error = QtWidgets.QLabel(self)

       # self.update()
        self.label.move(600,40) # x pos y pos

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(100, 0) # x pos y pos
        self.textbox.resize(280,30)


        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QRect(100, 30, 280, 30))
        self.comboBox.setObjectName("Unit Selection")

        self.comboBox.addItem("Fahrenheit (default)")
        self.comboBox.addItem("Celsius")
        self.comboBox.addItem("Kelvin")
  
        #Create button
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Search City")
        self.button1.move(0, 0) # x pos y pos

        #Binds button shortcut to enter key
        self.button1.setShortcut("Return")
        self.button1.setStyleSheet("border: 1px solid black;")
        self.button1.setStyleSheet("border-radius: 50%;")
        self.button1.setStyleSheet("color: black;")
        self.button1.setStyleSheet("background: white;")

        self.show()

    def resizeEvent(self, event):
        self.city_name.move(self.rect().center()-QPoint(139,379))
        self.temp.move(self.rect().center()-QPoint(149,299)) 
        self.weather_report.move(self.rect().center()-QPoint(89,149))
        self.humidity.move(self.rect().center()-QPoint(359,79))
        self.pressure.move(self.rect().center()-QPoint(159,79))
        self.weather_report_icon.move(self.rect().center()-QPoint(239,269))
        self.feel_like.move(self.rect().center()-QPoint(-81,79))
        self.wind_speed.move(self.rect().center()-QPoint(159,29))  
        
        #daily
        

        QMainWindow.resizeEvent(self, event)

    def comboClicked(self, unit):
         global unitSetFlag 
         if unit == ("Kelvin"):
            unitSetFlag = "Kelvin"
         elif unit == ("Celsius"):
            unitSetFlag = "Celsius"
         else:
            unitSetFlag = "fahrenheit"
    # This, when clicked, will grab users input for a city name
    def clicked(self):
        userCityName = self.textbox.text() # variable for city name user input
        
        self.update()   # Update to get the full text

        
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
                if unitSetFlag == ("Kelvin"):
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Kelvin" + "&exclude=minutely" + "&appid=" + api_key)
                elif unitSetFlag == ("Celsius"):
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Metric" + "&exclude=minutely" + "&appid=" + api_key)
                else:
                    complete_url = (base_url_weather + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=Imperial" + "&exclude=minutely" + "&appid=" + api_key)
                # Sending HTTP request
                response = requests.get(complete_url)
                print(complete_url)
                # checking the status code of the request
                if response.status_code == 200:

                    # retrieving data in the json format
                    data = response.json()
                    data1 = response.json()
                    
                    # take the 'current' dict block in api code
                    current = data['current']
                    daily = data1['daily']



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

                    #print(len(daily))
                    #dt = daily[0]['dt']
                    #daily_temp = daily[6]['temp']

                    #get all of element in daily struct (for loop)
                    dt = [element['dt'] for element in daily]
                    daily_temp_min = [element['temp']['min'] for element in daily]
                    daily_temp_max = [element['temp']['max'] for element in daily]
                    daily_weather = [element['weather'][0]['icon'] for element in daily]                   

                    # 7-days forcast
                    dt[0] = datetime.fromtimestamp(dt[0]).strftime('%a %d')
                    dt[1] = datetime.fromtimestamp(dt[1]).strftime('%a %d')
                    dt[2] = datetime.fromtimestamp(dt[2]).strftime('%a %d')
                    dt[3] = datetime.fromtimestamp(dt[3]).strftime('%a %d')
                    dt[4] = datetime.fromtimestamp(dt[4]).strftime('%a %d')
                    dt[5] = datetime.fromtimestamp(dt[5]).strftime('%a %d')
                    dt[6] = datetime.fromtimestamp(dt[6]).strftime('%a %d')
                    dt[7] = datetime.fromtimestamp(dt[7]).strftime('%a %d')


                    self.error.clear()

                    self.city_name.setGeometry(600,55,300,24)
                    if (geo_data[0]['country'] == "US"):
                        self.city_name.setText(f"{name}, {geo_data[0]['state']}")
                    else:
                        self.city_name.setText(f"{name}, {geo_data[0]['country']}")
                        
                    self.city_name.setFont(QFont('Times', 30))
                    self.city_name.setStyleSheet("color: white;border: 1px solid black;")
                    self.city_name.adjustSize()
                    self.city_name.move(600,70)


                    self.temp.setText(f" {round(temperature)}\N{DEGREE SIGN}")
                    self.temp.setFont(QFont('Times', 60))
                    self.temp.setStyleSheet("color: white;")
                    self.temp.adjustSize()
                    self.temp.move(590,150)   

                    self.weather_report.setText(f" {weather_report}")
                    self.weather_report.setFont(QFont('Times', 17))
                    self.weather_report.setStyleSheet("color: white;")
                    self.weather_report.adjustSize()
                    self.weather_report.move(650,300) 

                    self.humidity.setText(f"Humidity {humidity}%")
                    self.humidity.setFont(QFont('Times', 11))
                    self.humidity.setStyleSheet("color: white;")
                    self.humidity.adjustSize()
                    self.humidity.move(380,370)

                    self.pressure.setText(f"Pressure {pressure} mbar")
                    self.pressure.setFont(QFont('Times', 11))
                    self.pressure.setStyleSheet("color: white;")
                    self.pressure.adjustSize()
                    self.pressure.move(580,370)

                    #display weather icon based on api weather report code
                    weatherCode = current['weather'][0]['icon']
                    icon = "./image/" + weatherCode + ".png"
                    backgroundImage = "./backgroundimage/" + weatherCode + ".jpg"
                    oImage = QImage(backgroundImage)
                    sImage = oImage.scaled(QSize(1480,900))
                    palette = QPalette()
                    palette.setBrush(QPalette.Window, QBrush(sImage))
                    self.setPalette(palette)

                    self.im = QPixmap(icon)
                    self.weather_report_icon.setPixmap(self.im)
                    self.weather_report_icon.setScaledContents( True )
                    self.weather_report_icon.setGeometry(100,100,100,100)
                    self.weather_report_icon.move(500,180)
                    
                    

                    #display weather icon based on daily api weather report code
                    daily_icon_0 = "./image/" + daily_weather[0] + ".png"
                    daily_icon_1 = "./image/" + daily_weather[1] + ".png"
                    daily_icon_2 = "./image/" + daily_weather[2] + ".png"
                    daily_icon_3 = "./image/" + daily_weather[3] + ".png"
                    daily_icon_4 = "./image/" + daily_weather[4] + ".png"
                    daily_icon_5 = "./image/" + daily_weather[5] + ".png"
                    daily_icon_6 = "./image/" + daily_weather[6] + ".png"



                   


                    self.feel_like.setText(f"Feel Like {round(temp_feel_like)} \N{DEGREE SIGN}")
                    self.feel_like.setFont(QFont('Times', 11))
                    self.feel_like.setStyleSheet("color: white;")
                    self.feel_like.adjustSize()
                    self.feel_like.move(820,370)  

                    self.wind_speed.setText(f"Wind Speed {round(wind_report)} mph")
                    self.wind_speed.setFont(QFont('Times', 11))
                    self.wind_speed.setStyleSheet("color: white;")
                    self.wind_speed.adjustSize()
                    self.wind_speed.move(580,420)

                    self.daily_label.setText("Daily")
                    self.daily_label.setFont(QFont('Times', 17))
                    self.daily_label.setStyleSheet("color: white;border: 2px solid green;")
                    self.daily_label.adjustSize()
                    self.daily_label.move(50, 500)
                 
                    


                    # Minimum temperature number -> string for rjust
                    min1 = str(round(daily_temp_min[0]))
                    min2 = str(round(daily_temp_min[1]))
                    min3 = str(round(daily_temp_min[2]))
                    min4 = str(round(daily_temp_min[3]))
                    min5 = str(round(daily_temp_min[4]))
                    min6 = str(round(daily_temp_min[5]))
                    min7 = str(round(daily_temp_min[6]))

                    # Maximum temperature number -> string for rjust
                    max1 = str(round(daily_temp_max[0]))
                    max2 = str(round(daily_temp_max[1]))
                    max3 = str(round(daily_temp_max[2]))
                    max4 = str(round(daily_temp_max[3]))
                    max5 = str(round(daily_temp_max[4]))
                    max6 = str(round(daily_temp_max[5]))
                    max7 = str(round(daily_temp_max[6]))


                    
                    self.dw_0 = QPixmap(daily_icon_0)
                    self.daily_report_icon_0.setPixmap(self.dw_0)
                    self.daily_report_icon_0.setScaledContents( True )
                    self.daily_report_icon_0.setGeometry(90,90,90,90)
                    self.daily_report_icon_0.move(50,570)

                    self.dt_0.setText(f" {dt[0]} \n\n\n{max1}\N{DEGREE SIGN}  {min1}\N{DEGREE SIGN}")
                    self.dt_0.setFont(QFont('Times', 13))
                    self.dt_0.setStyleSheet("color: white; border: 1px solid green;")
                    self.dt_0.adjustSize() #50,550
                    #m1 = (550/self.w) * 100
                    self.dt_0.move(50, 550)

                    self.dw_1 = QPixmap(daily_icon_1)
                    self.daily_report_icon_1.setPixmap(self.dw_1)
                    self.daily_report_icon_1.setScaledContents( True )
                    self.daily_report_icon_1.setGeometry(90,90,90,90)
                    self.daily_report_icon_1.move(320,570)

                    self.dt_1.setText(f" {dt[1]} \n\n\n{max2}\N{DEGREE SIGN}  {min2}\N{DEGREE SIGN}")
                    self.dt_1.setFont(QFont('Times', 13))
                    self.dt_1.setStyleSheet("color: white; border: 1px solid green;")
                    self.dt_1.adjustSize() 
                    self.dt_1.move(320, 550)

                    self.dw_2 = QPixmap(daily_icon_2)
                    self.daily_report_icon_2.setPixmap(self.dw_2)
                    self.daily_report_icon_2.setScaledContents( True )
                    self.daily_report_icon_2.setGeometry(90,90,90,90)
                    self.daily_report_icon_2.move(570,570)

                    self.dt_2.setText(f" {dt[2]} \n\n\n{max3}\N{DEGREE SIGN}  {min3}\N{DEGREE SIGN}")
                    self.dt_2.setFont(QFont('Times', 13))
                    self.dt_2.setStyleSheet("color: white; border: 1px solid green;")
                    self.dt_2.adjustSize() 
                    self.dt_2.move(570, 550)
                    self.update() 

                    self.dw_3 = QPixmap(daily_icon_3)
                    self.daily_report_icon_3.setPixmap(self.dw_3)
                    self.daily_report_icon_3.setScaledContents( True )
                    self.daily_report_icon_3.setGeometry(90,90,90,90)
                    self.daily_report_icon_3.move(820,570)

                    self.dt_3.setText(f" {dt[3]} \n\n\n{max4}\N{DEGREE SIGN}  {min4}\N{DEGREE SIGN}")
                    self.dt_3.setFont(QFont('Times', 13))
                    self.dt_3.setStyleSheet("color: white; border: 1px solid green;")
                    self.dt_3.adjustSize() 
                    self.dt_3.move(820, 550)
                    self.update() 

                    self.dw_4 = QPixmap(daily_icon_4)
                    self.daily_report_icon_4.setPixmap(self.dw_4)
                    self.daily_report_icon_4.setScaledContents( True )
                    self.daily_report_icon_4.setGeometry(90,90,90,90)
                    self.daily_report_icon_4.move(1070,570)

                    self.dt_4.setText(f" {dt[4]} \n\n\n{max5}\N{DEGREE SIGN}  {min5}\N{DEGREE SIGN}")
                    self.dt_4.setFont(QFont('Times', 13))
                    self.dt_4.setStyleSheet("color: white; border: 1px solid green;")
                    self.dt_4.adjustSize() 
                    self.dt_4.move(1070, 550)
                    self.update() 

                    self.dw_5 = QPixmap(daily_icon_5)
                    self.daily_report_icon_5.setPixmap(self.dw_5)
                    self.daily_report_icon_5.setScaledContents( True )
                    self.daily_report_icon_5.setGeometry(90,90,90,90)
                    self.daily_report_icon_5.move(1320,570)

                    self.dt_5.setText(f" {dt[5]} \n\n\n{max6}\N{DEGREE SIGN}  {min6}\N{DEGREE SIGN}")
                    self.dt_5.setFont(QFont('Times', 13))
                    self.dt_5.setStyleSheet("color: white; border: 1px solid green;")
                    self.dt_5.adjustSize() 
                    self.dt_5.move(1320, 550)
                    self.update() 

                    self.dw_6 = QPixmap(daily_icon_6)
                    self.daily_report_icon_6.setPixmap(self.dw_6)
                    self.daily_report_icon_6.setScaledContents( True )
                    self.daily_report_icon_6.setGeometry(90,90,90,90)
                    self.daily_report_icon_6.move(1570,570)

                    self.dt_6.setText(f" {dt[6]} \n\n\n{max7}\N{DEGREE SIGN}  {min7}\N{DEGREE SIGN}")
                    self.dt_6.setFont(QFont('Times', 13))
                    self.dt_6.setStyleSheet("color: white; border: 1px solid green;")
                    self.dt_6.adjustSize() 
                    self.dt_6.move(1570, 550)
                    self.update() 



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
                self.daily_temp_max.clear()
                self.daily_temp_min.clear()
            # showing the error message if not real city name
                self.error.setText(f"The city you entered does not exist. Please enter a city name.")
                self.error.setFont(QFont('Times', 13))
                self.error.setStyleSheet("color: white;")
                self.error.adjustSize()
                self.error.move(600,55)
                self.update() 

    def update(self):
        self.label.adjustSize()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv) 
    window = MyWindow()

    window.show()
    sys.exit(app.exec_())


window()

  
