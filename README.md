## 1. Overview
 This is our final project for the course Scientific Programming in Python of the University Osnabrück. Our goal is to compare the range of restaurants in different german cities available on Lieferando (www.lieferando.de). To gather the data we use Selenium (https://selenium-python.readthedocs.io) and matplotlib (https://matplotlib.org) to visualise the results. 

 ## 2. Installation 
 ### General requirements
 <ul>
 <li>Working python enviroment with version >= python 3.7 (https://www.python.org) </li> <br>
 <li>Chromedriver (https://chromedriver.chromium.org/downloads)<br> Install the chromdriver which fits your brower version. You can see the chrome version under Settings>About Chrome. </li> <br>
 </ul>

 ### Installation process
 Open a terminal in the project folder and enter <br>

     $ pip -r install requirements.txt

  You need to change the PATH in scraper.py depending on your operating system. 

  #### For Mac
  Attention: You might need to give special permissions to your chromedriver to work. 
  In line 17 and 18 it should look like this:
  ```Python 
 PATH = "PATH TO YOUR DRIVER"  
 driver = webdriver.Chrome(PATH)  
  
  ```
  #### For Windows 
  In line 17 and 18 it should look like this:
  ```Python 
 PATH = "PATH TO YOUR DRIVER"  
 driver = webdriver.Chrome(executable_path=PATH)  
  
  ```
  #### For Ubuntu Linux 

  ## 3. How to use the program
  Run lets_scrape.py 

     $ python lets_scrape.py

  and then follow the dialoge. As a result there should appear up to two pdf files in the Project folder.

  ### Troubleshooting and Remarks


   #### Entering adresses <br>
   <ul><li>Lieferando might not find the city. You may use an actual adress or add " Hbf" to the city name.</li> <br>
   <li>For cities which might occur multiple times in germany, you may enter the zip code to the city name. </li></ul>
