# Team_alpha

<!-- TABLE OF CONTENTS -->
## Table of Contents
<details open="open">
  <summary>Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href=#how-to-run>How to Run</a></li>
        <li><a href=#how-to-use-the-software>How to use the software</a></li>
        <li><a href="#copyright">Copyright</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href=#iteration-1>Iteration 1</a></li>
        <li><a href=#iteration-2>Iteration 2</a></li>
        <li><a href=#iteration-3>Iteration 3</a></li>
        <li><a href=#iteration-4>Iteration 4</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



## About The Project

We build this Weather Forcast Software to help you be able to know the weather around the world. An application of science and technology to predict the conditions of the atmosphere for a given location and time

### How to Run
Please install <a href="#built-with">packages list from here</a> and download our program from git clone git@github.com:utk-cs/Team_alpha.git

You shall obtain files: WeatherApp.py and image (directory)

Run with: py WeatherApp.py

### How to use the software
Iteration 1: 
At the top-left corner appeared a search box, enter a desired location. 

Then enter the type of unit for temperature. There are 3 choices for it:

  - anything: kelvin 
   
  - "metric": Celsius
  
  - "imperial": Fahrenheit.
It will appear weather condtion you need today and some basic information on the next 7 days
Maksure you click the box "Unit" by left-click mouse after entered "Search city" and "Unit"
### Copyright
#### Weather Icons and App Logo Copyrights
Iconset: (https://openweathermap.org/weather-conditions)

License: Free for commercial use ()

Download date: 2021-10-03

### Built With
* [PyQt5](https://pypi.org/project/PyQt5/#/)

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
A machine can run python3

### Installation

#### For Deverlopers:
   1. Get a free API Key at [OpenWeatherMap](https://openweathermap.org/api)

   2. Private API key included in the test.py

#### For TA:
  ##### Install 
  1. PyQt5 - pip install pyqt5
  2. BlurWindow - python -m pip install BlurWindow
  3. requests - python -m pip install requests
  4. pytz - pip install pytz
  
  <li><a href=#iteration-3>Iteration 3</a></li>

  5. pip install qt-material

## Usage

### Iteration 1
#### Features:
    1. Search box which can get longtitude and latitude from One Call api
  
    2. Background with image
    
    3. Today's temperature at desired location + country (states)
    
    4. Weather conditon's icon based on the result return from One Call api
    
    5. Today's variables (humidity, pressure, feel likes, wind speed) with no decimal number
    
    6. Daily section contain: next 7 dates with max. and min. for each day
    
    7. If the user entered an invalid location, it will prompt an error message
    

![image](https://user-images.githubusercontent.com/69742686/136226257-05348064-c12a-4f4f-bc6e-eba882a87968.png)

![image](https://user-images.githubusercontent.com/69742686/136229137-aa9eeed2-235d-4653-b748-2798643b72db.png)

### Iteration 2
#### Features:
    1. Icons for daily weather
    
    2. Background image based on today's weather conditon
    
    3. Display look better 
    
![image](https://user-images.githubusercontent.com/69742686/138382342-080cf33c-b1cb-4813-8f2e-74b214359694.png)

![image](https://user-images.githubusercontent.com/69742686/138382951-9fd464fe-e418-4793-9c66-402734052361.png)

![image](https://user-images.githubusercontent.com/69742686/138382965-d4749bde-a013-43f7-a850-5ddc3b0967d4.png)

### Iteration 3

<ul>
    <li><a href="#installation">New installation</a></li>
</ul>


#### Features:
    1. The labels that can stand at the same place in bigger or smaller screen size
    
    2. Hourly for today's date
    
    3. Alert messeage 
    
    4. Save a favorite location. Any time you open the application, it showned your saved location
    
![image](https://user-images.githubusercontent.com/69742686/140447882-eaf69c83-a2d7-4ef8-80e0-511141f7e6fd.png)


### Iteration 4

#### Features:
    1. Warning messages appear when the location has an alert
    
    2. Hourly information for the current data
    
    3. Reset to default settings button


https://user-images.githubusercontent.com/69742686/142523399-b84b2b93-edfc-4d28-9999-f0889a8f222e.mp4



## Contact
An Phan - phanthanhan2107@gmail.com (primary), aphan2@vols.utk.edu (school)

Seth Johnson - sjohn248@vols.utk.edu

Darius White

Taha Khan

Project Link: [Team_alpha](https://github.com/utk-cs/Team_alpha)
