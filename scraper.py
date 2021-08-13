from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from data_helper import get_number, explicit_wait


def restaurants(adress: str) -> list:
	"""This funtion will return a list of tuples.
	Each tuple represents one restaurant which can be found at the input variable (adress) on Lieferando.de.
	One tuple has the form: (restaurant_name: str, [type_kitchen1: str, type_kitchen2: str, ...]: list,
							time_of_delivery: int, delivery_costs: float, min_order_value: float,
							rating: float, number_of_ratings: int): tuple.
	"""

	# Copy the path of the chromedriver in here
	PATH = "chromedriver_91.exe"#"/Users/tkapferer/Uni/LetsScrape/chromedriver_91"  
	driver = webdriver.Chrome(executable_path=PATH) 
	# Enter adress on Lieferando and search for it
	driver.get("https://www.lieferando.de")
	search = driver.find_element_by_id("imysearchstring")
	search.click()
	search.send_keys(adress)

	explicit_wait(driver,'lp__place.notranslate.selected', 8)

	search.send_keys(Keys.ENTER)
	
	explicit_wait(driver,'restaurant_amount',15)

	restaurants = []

	# create entrys for every restaurant found
	for restaurant in driver.find_elements_by_class_name("restaurant.js-restaurant"):

		try:
			restaurant_name = restaurant.find_element_by_class_name("restaurantname").text
		except NoSuchElementException:
			restaurant_name = None

		try:

			kitchen =  restaurant.find_element_by_class_name("kitchens").text
			kitchen = kitchen.split(", ")

		except NoSuchElementException:
			kitchen = None

		try: 

			delivery_time = restaurant.find_element_by_class_name("avgdeliverytime.avgdeliverytimefull.open").text
			
			if delivery_time.startswith("Ab") or delivery_time.startswith("From"):
				delivery_time = -1
			else:
				delivery_time = int(get_number(delivery_time))

		except NoSuchElementException:
			delivery_time = -1

		try: 
			delivery_cost = get_number(restaurant.find_element_by_class_name("delivery-cost.js-delivery-cost.notranslate").text)
		except NoSuchElementException:
			delivery_cost = -1

		try: 
			min_order = get_number(restaurant.find_element_by_class_name("min-order.notranslate").text)
		except NoSuchElementException:
			min_order = -1

		try:
			rating = get_number(restaurant.find_element_by_class_name("review-stars-range").get_attribute("style")) / 20
		except NoSuchElementException:
			rating = -1

		try:
			num_of_rating = int(get_number(restaurant.find_element_by_class_name("rating-total").text))
		except NoSuchElementException:
			num_of_rating = -1

		restaurant_tuple = (restaurant_name, kitchen, delivery_time, delivery_cost, min_order, rating, num_of_rating)
		restaurants.append(restaurant_tuple)

	driver.quit()
	restaurants = restaurants[:-1]

	return restaurants


	


if __name__ == '__main__':
	print(restaurants("Frankfurt am Main hbf"))
	












