import random

#Customer makes random order, checks list of all possible orders, attempts to make order based on the amount of money they have
#If not try to order again. If an order completes, prompts user to order again. They can keep doing this until they have less money than the
#cheapest item on the menu

class Menu:

    def __init__(self, sizes, base_prices):
        self.sizes = sizes #size of item as in small, medium, large
        self.base_prices = base_prices #price of an item
        self.full_menu = self.get_full_menu() # returns dictionary of prices per item/size. ex {"coffee - small": 6, "coffee - medium": 7}
        self.price_list = self.get_price_list() #gets a list of the prices of the items on the menu
        self.min_price = self.get_min_price() #gets the lowest price on the menu

    def get_full_menu(self):
        full_menu = {}
        for size in self.sizes:
            for item in self.base_prices:
                size_item_combo = size + ' - ' + item
                if size == 'small':
                    full_menu[size_item_combo] = self.base_prices.get(item)
                elif size == 'medium':
                    full_menu[size_item_combo] = self.base_prices.get(item) + 1
                else:
                    full_menu[size_item_combo] = self.base_prices.get(item) + 2

        return full_menu

    def get_price_list(self):
        price_list = list(self.base_prices.values())
        return price_list

    def get_min_price(self):
        min_price = min(self.price_list)
        return min_price


class Drink:

    def __init__(self, menu, drink, size):
        self.menu = menu  # Reference to the Menu instance
        self.drink = drink #Drink type like latte, mocha, etc
        self.size = size #size of drink item
        self.drink_price = self.get_drink_price(drink, size) #takes in menu dictionary and a drink/size combo, and returns the price

    def get_drink_price(self, drink, size):  # size = "small", "medium", "large"
        size_item_combo = size + ' - ' + drink
        price = self.menu.full_menu.get(size_item_combo)
        return price

class EconomicClass:

    def __init__(self):
        self.EconomicClasses = {'Rich': 50, 'Middle': 25, 'Poor': 5} #The economic classes in this world and money associated with it


class Customer:

    def __init__(self, customers_class=None):
        self.customers_class = customers_class #The economic class of a given customer
        self.wealth = self.get_customers_money() #Given someone's economic class, returns the amount of money they have

    def get_customers_money(self):
        economic_class_instance = EconomicClass().EconomicClasses
        if self.customers_class == None: #If customer's class is not provided, chooses a random class to use
            random_economic_class = random.choice(list(economic_class_instance))
            customers_money = economic_class_instance[random_economic_class]
            return customers_money
        else:
            customers_money = economic_class_instance.get(self.customers_class)
            return customers_money

    def update_customer_wealth(self, wealth_delta): #After an order completes, updates the customer's wealth
        self.wealth = self.wealth + wealth_delta
        return self.wealth

class Order:

    def __init__(self, menu, customer):
        self.menu = menu #menu of drink/size combos and their respecrive prices
        self.customer = customer #Customer who is making order
        self.drink = None #drink that is ordered
        self.order_validity = False #takes in a drink ordered and their economic class. Returns boolean if the order can be made (if customer's money is more than the order)
        self.order_result() #If order is invalid tries to order a different drink

    def get_drink_order(self):
        random_menu_item = random.choice(list(self.menu.full_menu))
        random_order_price = self.menu.full_menu[random_menu_item]
        return random_order_price

    def validate_order(self):
        print(f'Price: {self.drink}, money: {self.customer.wealth}')
        net_money = self.customer.wealth - self.drink
        if net_money >= 0:
            print('Transcation Valid')
            return True
        else:
            print('Customer does not have enough money')
            return False

    def order_result(self):
        while self.order_validity is False and self.customer.wealth >= self.menu.min_price:
        #Try to order drink. If customer has more money than drink, return bool of true and break loop. Else keep going until they order drink they have the money for
            self.drink = self.get_drink_order()
            self.order_validity = self.validate_order()

        if self.customer.wealth >= self.menu.min_price: #If loop breaks because transaction is valid, update customer's wealth and prompt to order again
            customers_new_wealth = self.customer.update_customer_wealth(-self.drink)
            print(r"Customer's new wealth:", customers_new_wealth)
            self.order_again()

        else: #If loop breaks because customer doesn't have enough money to order anything, end program
            print('You do not have enough money to order again')
            exit()

    def order_again(self): #Method for allowing customer to decide if they want to order again
        choice = ""
        while choice not in ("Yes","No"):
            choice = input("Do you want to order again: ")

        if choice == "Yes":
            self.drink = None
            self.order_validity = False
            self.order_result()
        else:
            print('Order Completed')
            exit()

if __name__ == '__main__':
    sizes = ['small','medium','large']

    base_price = {'latte': 6,
                  'coffee': 3,
                  'mocha': 4}

    menu = Menu(sizes, base_price)
    customer = Customer()
    Order(menu, customer)