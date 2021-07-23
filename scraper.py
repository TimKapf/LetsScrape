from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import os



def get_number(String):
	'''This function returns the numbers of type float which appear in the given String. Lieferando.de uses the german format to represent point numbers, therefore "," will be transformed to ".".
	 Only works for the german format.'''

	result = ''.join(x for x in String if x.isdigit() or x == ',')
	if result == "":
		return -999.0
	result = float(result.replace(',','.'))
	return result

def restaurants(Adress):
	'''This funtion will return a list of tuples. Each tuple represents one restaurant which can be found at the input variable (adress) on Lieferando.de.
	One tuple has the form (restaurant_name, [type_kitchen1, type_kitchen2, ...], time_of_delivery, delivery_costs, min_order_value, rating, number_of_rating).'''

	PATH = "" # Path where the chromedriver is stored in 
	driver = webdriver.Chrome(PATH) 
	driver.get("https://www.lieferando.de")
	search = driver.find_element_by_id("imysearchstring")
	search.send_keys(Adress)

	time.sleep(2) # seconds

	driver.find_element_by_id("submit_deliveryarea").click()

	time.sleep(2) # seconds

	restaurants = []

	for restaurant in driver.find_elements_by_class_name("restaurant.js-restaurant"):

		try:
			restaurant_name = restaurant.find_element_by_class_name("restaurantname").text
		except NoSuchElementException:
			restaurant_name = "###"

		try:
			kitchen =  restaurant.find_element_by_class_name("kitchens").text
			kitchen = kitchen.split(", ")
		except NoSuchElementException:
			kitchen = ["###"]

		try: 
			delivery_time = restaurant.find_element_by_class_name("avgdeliverytime.avgdeliverytimefull.open").text
			if delivery_time.startswith("Ab"):
				delivery_time = -999
			else:
				delivery_time = int(get_number(delivery_time))

		except NoSuchElementException:
			delivery_time = -999

		try: 
			delivery_cost = get_number(restaurant.find_element_by_class_name("delivery-cost.js-delivery-cost.notranslate").text)
		except NoSuchElementException:
			delivery_cost = -999.0

		try: 
			min_order = get_number(restaurant.find_element_by_class_name("min-order.notranslate").text)
		except NoSuchElementException:
			min_order = -999.0

		try:
			rating = get_number(restaurant.find_element_by_class_name("review-stars-range").get_attribute("style")) / 20
		except NoSuchElementException:
			rating = -999.0

		try:
			num_of_rating = int(get_number(restaurant.find_element_by_class_name("rating-total").text))
		except NoSuchElementException:
			num_of_rating = -999

		restaurant_tuple = (restaurant_name, kitchen, delivery_time, delivery_cost, min_order, rating, num_of_rating)
		restaurants.append(restaurant_tuple)

	driver.quit()
	restaurants = restaurants[:-1]

	return restaurants


	



	












