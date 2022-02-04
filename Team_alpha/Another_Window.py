class AnotherWindow(QWidget):
    def __init__(self, cityname, h_time):
        super().__init__()
        self.cityname = cityname
        self.time = h_time
        self.initUI_another()
        
        
    def getStyle (self, label, font_size,font_type, styleString, move_x, move_y):
        label.setFont(QFont(font_type,font_size))
        label.setStyleSheet(styleString)
        label.move(move_x, move_y)
        label.adjustSize()

    def brusing_backgroundImage(self, backgroundImage):
        oImage = QImage(backgroundImage)
        screen = app.primaryScreen()
        sImage = oImage.scaled(screen.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette) 

    def initUI_another(self):
        object_a = MyWindow()
        self.setGeometry(50, 50, object_a.w, object_a.h)

        layout = QGridLayout()

        # if the text box is empty => favorite city = city 
        if self.cityname == "":
            self.cityname = object_a.user_city_temp
        #hourly label for pop up window
        self.hourly_label = QtWidgets.QLabel(self)
        self.hourly_label.setText(f"HOURLY FORECAST - {self.cityname.upper()}")
        self.getStyle(self.hourly_label, 24, 'Times', 'color:white;', 400 , 200)
        
        

        print("another: ", self.cityname)

        #return variables from showCity in class MyWindow()
        home_backgroundImage, home_time = object_a.showCity(self.cityname) 
        self.brusing_backgroundImage(home_backgroundImage)
        
        print("time: ", home_time)

        '''
        self.hourly_time = [0] * 20
        for i in range (20):
            self.hourly_time[i] = QtWidgets.QLabel(self)
            self.hourly_time[i].setStyleSheet('color:white;')
            self.hourly_time[i] = time[i]
            #layout.addWidget(self.hourly_time[i], i, 0)
        '''
        
        



        layout.addWidget(QLabel('1'),0,0)
        layout.addWidget(QLabel('2'),0,1)
        layout.addWidget(QLabel('3'),0,2)
        self.setLayout(layout)
