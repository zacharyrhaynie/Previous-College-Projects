"""
I declare that the following source code was written solely by me. I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""

from abc import abstractmethod, ABC
import os

employees = []

# PAY_LOGFILE is a global variable holding ‘paylog.txt’
PAY_LOGFILE = 'paylog.txt'

class PayMethod(ABC):
    """Abstract class for the two pay methods, DirectMethod and MailMethod. Creates the baseline for what they should do."""

    def __init__(self, employee):
        """Initializes with the employee's information which will be needed for either their full address, or their bank information
        depending upon what payment method they utilize."""
        self.employee = employee
    
    @abstractmethod
    def pay(self):
        """Sets the framework requiring any inheriting classes to have a pay method."""
        pass

class DirectMethod(PayMethod):
    """Class that direct deposits money into the employees account. Needs the employee which you'll see in the __init__ and then pays
    the employee writing to the paylog.txt."""

    def __init__(self, employee):
        """Needs information from the employee so calls for it from it's parents __init__"""
        super().__init__(employee)
    
    def pay(self, amount):
        """Pays out to the employee. This one is a bit different because it's direct depositing versus MailMethod's mailing."""
        if amount > 0:
            with open(PAY_LOGFILE, 'a') as pay_file:
                print(f"Transferred {amount:.2f} for {self.employee.name} to {self.employee.account} at {self.employee.route}", file=pay_file)
        else:
            pass

class MailMethod(PayMethod):
    """Class the mails the employees money to them. Needs the employee which will be in the __init__ and writes to the paylog.txt"""

    def __init__(self, employee):
        """Calls the super's __init__ to get access to that sweet sweet employeee data."""
        super().__init__(employee)

    def pay(self, amount):
        """Pays out. Mails to employee instead of direct deposit."""
        if amount > 0:
            with open(PAY_LOGFILE, 'a') as pay_file:
                print(f"Mailing {amount:.2f} to {self.employee.name} at {self.employee.address}, {self.employee.city}, {self.employee.state} {self.employee.zip_code}.", file=pay_file)
        else:
            pass

class Classification(ABC):
    """Abstract class that sets the employees classification. """
    
    def __init__(self):
        """Initializes the class but all information needed will be passed into the other classifications (i.e. when I make an employee
        hourly, they will have their rate in the Employee object so I don't really need anything here.)"""
        pass

    @abstractmethod
    def calc_pay(self):
        """Any child of this class will need a way to calculate payment, thus this method."""
        pass

class Hourly(Classification):
    """Hourly classification, requires a rate (float) and timecards (an array of floats (the floats being the hours worked) which this 
    class will process as well), and then calculates the payment."""

    def __init__(self, rate):
        """On instantiation it'll set the hourly rate for the employee. Also holds the timecards for the employee."""
        self.rate = rate
        self.timecards = []
    
    def add_timecard(self, times):
        """Will be called by process_timecards if this is an employee that it will be adding timecards to. Will be passed a list of hours worked
        by that function and will add them to self.timecards"""
        if isinstance(times, (list, tuple, set)):
            self.timecards.extend(times)
        else:
            self.timecards.append(times)
    
    def calc_pay(self):
        """Calculates the payment of the employee by multiplying the rate by the sum of the timecards and returns a float. Also clears the 
        timecard from previous hours"""
        sum_timecards = sum(map(float, self.timecards))
        payment = self.rate * sum_timecards
        self.timecards.clear()
        return payment

class Salary(Classification):
    """Salary Classification, requires a salary and they recieve 1/24th of that every paycheck."""
    def __init__(self, salary):
        """Sets up that salary and gets it READY TO RUMMMMBLEEEEE!"""
        self.salary = salary

    def calc_pay(self):
        """Calculates the salaried employee's wage by taking their salary and dividing it by 24."""
        payment = self.salary / 24
        return payment

class Commission(Salary):
    """Commissioned employee, they are salaried but fancier. They have a set of receipts from their sales and a rate at which they recieve
    a portion of that sale."""
    def __init__(self, salary, rate):
        """Calls its super to get the salary and then sets up a list of receipts and their rate (which needs to be passed in as a float)."""
        super().__init__(salary)
        self.rate = rate
        self.receipt_list = []
    
    def add_receipt(self, receipts):
        """Adds them juicy receipts. Checks to see if it's a list, like when process_receipts is called, but is flexible enough to add
        one at a time."""
        if isinstance(receipts, (list, tuple, set)):
            self.receipt_list.extend(receipts)
        else:
            self.receipt_list.append(receipts)
    
    def calc_pay(self):
        """Calculates the commissioned employees pay check. Doesn't need anything as it uses it's salary and then accesses it's receipt_list.
        Clears the receipt list so they don't get paid twice for their sales."""
        base_payment = self.salary / 24
        commissioned_payment = (sum(map(float, self.receipt_list))) * (self.rate / 100)
        final_payment = base_payment + commissioned_payment
        self.receipt_list.clear()
        return final_payment
    
class Employee:
    """The big Momma. Instantiated on load_employees with all their info. Also is composed of a certain instance of PayMethod and Classification.
    Both of these are determined in the employees.csv as well as all their information. Has methods to change classification and pay method."""
    def __init__(self, ID, name, address, city, state, zip_code, classification, pay_method, route, account):
        """Takes some information from the load_employees and starts it up. load_employees will do the heavy lifting with determining which
        classification and payment method is required while passing in the relevant information."""
        self.ID = ID
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.classification = classification
        self.pay_method = pay_method
        self.route = route
        self. account = account

    def make_salaried(self, salary):
        """Changes the employee to be salaried(float)."""
        self.classification = Salary(salary)
    
    def make_hourly(self, rate):
        """Makes the employee hourly and establishes their rate (float)."""
        self.classification = Hourly(rate)
    
    def make_commissioned(self, salary, commision_rate):
        """Makes the employee commissioned and establishes their salary(float) and commission rate(float)."""
        self.classification = Commission(salary, commision_rate)

    def direct_method(self, route, account):
        """Updates the payment method to Direct Deposit."""
        self.route = route
        self.account = account
        self.pay_method = DirectMethod(self)
    
    def mail_method(self):
        """Updates the payment method to Mail."""
        self.pay_method = MailMethod(self)
    
    def issue_payment(self):
        """Issues the payment to the employee. First checks what they should be paid through their classification, then pays it to the employee."""
        payment = self.classification.calc_pay()
        self.pay_method.pay(payment)
    
def load_employees():
    """Starts up the employees! Reads in employees.csv and skips the first line. Takes the employees and splits them up then makes an employee object
    using their information. Finds out what classification and pay method they will be using and sets it up like that. Populates all this data
    to the employees module level list established at the start of this file."""
    with open("employees.csv", "r") as employee_file:
        employee_file.readline()

        ID, name, address, city, state, zip_code , classification, pay_method, salary, hourly, commission, route, account = range(13) #thanks for showing us this trick

        for line in employee_file:
            employee_data = line.strip().split(",")

            #Following line is pretty long. Sets up the Employee with everything but classification and paymethod, which will be determined directly afterwards
            employee = Employee(employee_data[ID], employee_data[name], employee_data[address], employee_data[city], employee_data[state], employee_data[zip_code], None, None, employee_data[route], employee_data[account])

            if employee_data[classification] == '1':
                employee.make_hourly(float(employee_data[hourly]))

            elif employee_data[classification] == '2':
                employee.make_salaried(float(employee_data[salary]))
            
            else: 
                employee.make_commissioned(float(employee_data[salary]), float(employee_data[commission]))
            
            if employee_data[pay_method] == '1':
                    employee.direct_method(employee_data[route], employee_data[account])
            else:
                    employee.mail_method()
            
            employees.append(employee)

def find_employee_by_id(ID):
    """Finds the employee by using their ID. Returns the employee object out the list of employees using a tuple comprehension
    and defaulting to None if it doesn't exist (which should happen)."""
    employee = next((emp for emp in employees if emp.ID == ID), None)
    return employee

def process_timecards():
    """Proccesses the time cards. Reads in the timecards.txt file and then uses find_employee_by_id to find the employee and help assign the time."""
    with open("timecards.txt", "r") as timecard_input:
        for timecard_data in timecard_input:
            data = timecard_data.strip().split(",")

            ID = data.pop(0)
            employee = find_employee_by_id(ID)

            employee.classification.add_timecard(data)

def process_receipts():
    """Very similar to process_timecards, only for commissioned people and their receipts."""
    with open("receipts.txt", "r") as receipt_input:
        for receipt_data in receipt_input:
            data = receipt_data.strip().split(",")

            ID = data.pop(0)
            employee = find_employee_by_id(ID)

            employee.classification.add_receipt(data)
            
def run_payroll():
    """Function given me in the documentation. Runs the payroll by calling issue_payment for every employee. Also clears the old PAY_LOGFILE"""
    if os.path.exists(PAY_LOGFILE):
        os.remove(PAY_LOGFILE)
    for emp in employees:
        emp.issue_payment()