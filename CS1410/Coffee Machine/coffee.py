"""
I declare that the following source code was written solely by me. I understand that copying any source code, in whole
or in part, constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy.

Welcome to coffee.py the program that simulates a cofee machine. It has several classes that represent the machine itself,
the selector, the cash box, and the products that are dispensed. It will take several commands via an input in OneAction(), and
display their results (or errors). It only takes nickels up to half dollars, and there are 5 options that it vends.
"""

class Product:
    """Creates a generic product. It has a name (str), a price (int), and a recipe (list). Has a getter for price, and a function to
    make the product."""
    def __init__(self, name, price, recipe):
        """Initializes the generic product with a name, a price, and the recipe to dispense for it."""
        self.name = name
        self.price = price
        self.recipe = recipe
    
    def __str__(self):
        return f"{self.name} costs {self.price} cents."
    
    def getPrice(self):
        """Returns price of the Product."""
        return self.price
    
    def make(self):
        """Dispenses the product!"""
        print(f"Making {self.name}")
        for ingredient in self.recipe:
            print(f"\tDispensing {ingredient}")

class CashBox:
    """Creates a cash_box that tracks the credit (or amount that has been entered since last selection) and totalRecieved (or amount
    actually used to buy coffee. Has a deposit(amount) for coins inserted, a returnCoins() that returns coins leftover after making coffee or
    on quit, a haveYou(amount) to price check if it has the amount needed for coffee in credit, a deduct(amount) that moves amount to 
    totalRecieved then calls returnCoins(), and a total() that returns I guess how much is in totalRecieved."""

    def __init__(self):
        """Initializes the credit and totalRecieved variables."""
        self.credit = 0
        self.totalRecieved = 0

    def deposit(self, amount):
        """Recieves an amount (int) and deposits it into self.credit"""
        self.credit += amount
        print(f"Depositing {amount} cents. You have {self.credit} cents credit.")
        

    def returnCoins(self):
        """Returns any coins in credit by printing the return then setting self.credit to 0."""
        print(f"Returning {self.credit} cents.")
        self.credit = 0

    def haveYou(self, amount):
        """Price check to see if the CashBox's credit has enough to make a product."""
        if self.credit >= amount:
            return True
        print("Sorry, not enough money deposited.")
    
    def deduct(self, amount):
        """Moves coins from credit to totalRecieved, then returns whatever coins are left."""
        self.credit -= amount
        self.totalRecieved += amount

        if self.credit > 0:
            self.returnCoins()

    def total(self):
        return self.totalRecieved


class Selector:
    """Creates a selector that handles the selections. It needs a cash_box and products. It'll handle the selection of products and
    check the amount that a product costs after it is selected, then verify with the cash box that the money has been recieved, then
    if it has, will dispense the products and tell the cash_box to deduct the price."""

    def __init__(self, cash_box):
        """Initializes the selector with it's cash_box (that's made in coffee_machine and passed in during the creation of the 
        selector) and it's products."""
        self.cash_box = cash_box
        self.products = [Product("black", 35, ["cup", "coffee", "water"]), Product("white", 35, ["cup", "coffee", "creamer", "water"]),\
                         Product("sweet", 35, ["cup", "coffee", "sugar", "water"]), Product("white & sweet", 35, ["cup", "coffee", "sugar", "creamer" "water"]), \
                         Product("bouillon", 25, ["cup", "buillon powder", "water"])]
        
    def select(self, index):
        """Selects a product, first checking the price of the product, then checking the cash box if it has the credit required,
        then if it does makes the product and tells the cash box to deduct the price."""

        price = self.products[index - 1].getPrice()

        if self.cash_box.haveYou(price):
            self.products[index - 1].make()
            self.cash_box.deduct(price)


class CoffeeMachine:
    """Creates a coffee_machine that is the front to all this business. Verifies that all commands are done correctly through oneAction()
    and has totalCash() to reflect how much the machine has made. Needs a cash_box and a selector."""

    def __init__(self):
        """Initializes the coffee_machine with a cash_box and a selector."""
        
        self.cash_box = CashBox()
        self.selector = Selector(self.cash_box)
    
    def oneAction(self):
        """The big mama. Does pretty much everthing including verifying that commands are correct and then gets the ball rolling."""

        print(f"\n\n_______________________________\n\tPRODUCT LIST: all 35 cents, except buillon (25 cents)\n\t1=black, 2=white, 3=sweet, 4=white & sweet, 5=buillon")
        print(f"\tSample commands: insert 25, select 1")

        command = input("Your command: ").split()

        if command[0].lower() == "insert":
            
            if int(command[1]) in [5, 10, 25, 50]:
                self.cash_box.deposit(int(command[1]))
            else:
                print(f"INPUT ERROR >>>\nWe only take nickels, dimes, quarters, or half dollars.\nCoin(s) returned.")
            return True
        
        elif command[0].lower() == "select":
            
            if int(command[1]) in [1, 2, 3, 4, 5]:
                self.selector.select(int(command[1]))
            else:
                print(f"Invalid selection. Try selecting one of the 5 listed products")
            return True
        
        elif command[0].lower() == "cancel":

            if self.cash_box.credit > 0:
                self.cash_box.returnCoins()
            return True
        
        elif command[0].lower() == "quit":

            if self.cash_box.credit > 0:
                self.cash_box.returnCoins()
            return False
        
        else:
            print(f"Invalid command.")
            return True

    def totalCash(self):
        """Returns the total recieved by the machine."""

        return self.cash_box.total()


def main():
    m = CoffeeMachine()
    while m.oneAction():
        pass
    total = m.totalCash()
    print(f"Total cash: ${total/100:.2f}")


if __name__ == "__main__":
    main()