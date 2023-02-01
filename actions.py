# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict


pizza_price={'small':5,'medium':7,'large':10}
side_dish_price=3
drink_price=2


class AddSideDishToOrder(Action):
	def name(self):
		return 'add_side_dish_to_order'

	def run(self, dispatcher, tracker, domain):
		side_dish = tracker.get_slot("side_dish_name")
		amount = tracker.get_slot("amount")
		old_price = tracker.get_slot("price")
		if amount is None: amount=1
		order_details =  str(amount) + " plates of "+  side_dish
		old_order = tracker.get_slot("total_order")
		price=old_price+side_dish_price*int(amount)
		if old_order==None: old_order=[]
		return[SlotSet("price", price),SlotSet("total_order", [order_details]) if old_order is None else SlotSet("total_order", old_order+[order_details])]






class ActionChangeOrder(Action):
	def name(self):
		return 'action_change_order'

	def run(self, dispatcher, tracker, domain):
		pizza_size = tracker.get_slot("pizza_size")
		pizza_type = tracker.get_slot("pizza_type")
		pizza_amount = tracker.get_slot("amount")
		inter_order= tracker.get_slot("inter_order")
		
		if pizza_size is None: pizza_size= inter_order['pizza_size']
		if pizza_amount is None: pizza_amount= inter_order['pizza_amount']
		if pizza_type is None: pizza_type= inter_order['pizza_type']
			
		
		return[SlotSet("pizza_type", pizza_type),SlotSet("pizza_size", pizza_size),SlotSet("amount", pizza_amount)]

class ActionPizzaOrderAdd(Action):
	def name(self):
		return 'action_pizza_order_add'

	def run(self, dispatcher, tracker, domain):
		old_order = tracker.get_slot("total_order")
		old_price = tracker.get_slot("price")
		if old_order is None:
			old_price=0
		pizza_size = tracker.get_slot("pizza_size")
		pizza_type = tracker.get_slot("pizza_type")
		pizza_amount = tracker.get_slot("amount")
		order_details = str(pizza_amount+" "+pizza_size+" "+pizza_type+ " Pizzas ")
		price=old_price+pizza_price[pizza_size]*int(pizza_amount)
		return[SlotSet("price", price),SlotSet("total_order", [order_details]) if old_order is None else SlotSet("total_order", old_order+[order_details])]



    	




class ActionResetPizzaForm(Action):
	def name(self):
		return 'action_reset_pizza_form'

	def run(self, dispatcher, tracker, domain):
		
		pizza_size = tracker.get_slot("pizza_size")
		pizza_type = tracker.get_slot("pizza_type")
		pizza_amount = tracker.get_slot("amount")
		
		
		return[SlotSet("pizza_type", None),SlotSet("pizza_size", None),SlotSet("amount", None)]

class ActionOrderNumber(Action):
	def name(self):
		return 'action_order_number'

	def run(self, dispatcher, tracker, domain):
		name_person = tracker.get_slot("client_name")
		number_person = tracker.get_slot("phone_number")
		order_number =  str(name_person + "_"+number_person)
		print(order_number)
		return[SlotSet("order_number", order_number)]




class ActionPizzaQuestions(Action):
	def name(self):
		return 'action_pizza_questions'

	def run(self, dispatcher, tracker, domain):
		topping = tracker.get_slot("toppings")
		if topping=="meat": pizzas='Margherita, Tuna, Vegetarian'
		if topping=="vegetables": pizzas='Margherita, Tuna, pepperoni, kebab'
		if topping=="pepper": pizzas='Margherita, Tuna, pepperoni, kebab'
		
		
		return[SlotSet("pizzas", pizzas)]

class ActionSideQuestions(Action):
	def name(self):
		return 'action_side_questions'

	def run(self, dispatcher, tracker, domain):
		topping = tracker.get_slot("toppings")
		if topping=="meat": side_dishes='onion rings, French Fries, mozzarella sticks'
		if topping=="cheese": side_dishes='onion rings, French Fries, chicken wings'
		if topping=="onion": side_dishes='French Fries, mozzarella stciks, onion rings'
		
		
		return[SlotSet("side_dishes", side_dishes)]

