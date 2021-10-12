# **SOLID** Design Principles

These principles establish practices that aim for better software development with considerations for maintaining and extending as the project grows. Adopting these practices can also contribute to avoiding code smells or code refactoring.

The SOLID concept was first published in year 2000 by Robert C. Martin AKA "Uncle Bob".

> Main concepts  and definitions from this video: https://youtu.be/pTB30aXS77U  
> Most of code here used is from this repo: https://github.com/ArjanCodes/betterpython  
> Among other sources credited at the bottom.  


**SOLID** is an acronym for 5 design principles:

**S**ingle Responsibility  
**O**pen/Closed  
**L**iskov Substitution  
**I**nterface Segregation  
**D**ependency Inversion


Solid Design principles help to write code that is easy to reuse and easy to extend.

#### **Single Responsibility** Principle
"A class should have one and only one reason to change, meaning that a class should have only one job."

#### **Open/Closed** Principle
"Objects or entities should be open for extension but closed for modification.

#### **Liskov Substitution** Principle
"Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program."

> This means that every subclass or derived class should be substitutable for their base or parent class.

#### **Interface Segregation** Principle
"A client should never be forced to implement an interface that it doesn't, or clients shouldn't be forced to depend on methods they do not use."


#### **Dependency Inversion** Principle
"Entities must depend on abstractions, not on concretions. It states that the high-level module must not depend on the low-level module, but they should depend on abstractions."

In order to understand deeply these principles lets look at code examples for each principle.

## Code Examples for each principle:

### **S**ingle Responsibility

```python
# Code Before
class Order:
    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

    def pay(self, payment_type, security_code):
        if payment_type == "debit":
            print("Processing debit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        elif payment_type == "credit":
            print("Processing credit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        else:
            raise Exception(f"Unknown payment type: {payment_type}")
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/single-responsibility-before.py
```
The problem with the previous code is that Order class has to many responsibilities, we could separate Pay function as his own class. These principle does not imply that each class must have only one function, but rather that each class must attend his own responsibilities.


```python
# Code After
class Order:

    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class PaymentProcessor:
    def pay_debit(self, order, security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

    def pay_credit(self, order, security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/single-responsibility-after.py
```
Now we have each object, payment and order each with their own responsibilities

Here is another example:

```python
# code before
class Vehicle:
    def __init__(self, name):
        self._name = name
        self._persistence = MySQLdb.connect()
        self._engine = Engine()

    def getName():
        return self._name()

    def getEngineRPM():
        return self._engine.getRPM()

    def getMaxSpeed():
        return self._speed

    def print():
        print("Vehicle: {}, Max Speed: {}, RMP: {}".format(self._name, self._speed, self._engine.getRPM()))
# source: https://softwarecrafters.io/python/principios-solid-python
```
In the example before Vehicle class is responsible for initiating a Vehicle, Saving to database and printing/presenting the info.

Applying Single Responsibility design principle means we can separate presentation (printing) logic from business logic from saving to database logic.

```python
# code after
class Vehicle:
    def __init__(self, name, engine):
        self._name = name
        self._engine = engine

    def getName(self):
        return self._name()

    def getEngineRPM(self):
        return self._engine.getRPM()

    def getMaxSpeed(self):
        return self._speed


class VehicleRepository:
    def __init__(self, vehicle, db):
        self._persistence = db
        self._vehicle = vehicle


class VehiclePrinter:
    def __init__(self, vehicle, db):
        self._persistence = db
        self._vehicle = vehicle

    def print(self):
        print("Vehicle: {}, Max Speed: {}, RMP: {}".format(self._vehicle.getName(), self._vehicle.getMaxSpeed(), self._vehicle.getRPM()))
# source: https://softwarecrafters.io/python/principios-solid-python
```

**Single Responsibility** Principle increases **Cohesion**, so function are closed to the data that they compute and have less responsibilities. This principle ensures that each class can be reused in other parts of the code for latter purposes.


### **O**pen/Closed
> "Objects or entities should be open for extension but closed for modification."

Write code that is **Open** for extension but **Closed** for modification.

This means that a class or a function should be extendable without modifying the class/function itself.

This principle recommends that when creating new functionality into our code instead of modifying the original classes we should extend the already existing ones or redefine the methods from the parent class also is valid to pass dependencies that implement the wanted new function.

These ensures code stability avoiding continuous changes to the code, which makes dependency chains more reliable. The principle is useful when working with a framework or legacy code. Like extending the AbstractUser class in Django to create a custom user.

For example in the following code:

```python
# code before
class Order:
    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class PaymentProcessor:
    def pay_debit(self, order, security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

    def pay_credit(self, order, security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
# to call it:
order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())
processor = PaymentProcessor()
processor.pay_debit(order, "0372846")
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/open-closed-before.py
```

The problem with this code is if we wanted to add a new payment method like paypal or bitcoin we have to modify the PaymentProcessor class.

For applying the Open/Close principle we can create a structure of classes so we can define a new subclass for every payment type.

Like the following code:

```python
# Code after
from abc import ABC, abstractmethod

class Order:
    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order, security_code):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
#to call it you simply call the wanted payment method:
order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())
processor = DebitPaymentProcessor()
processor.pay(order, "0372846")
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/open-closed-after.py
```

In the previous code if we wanted to add a new payment method we don't need to change Order or PaymentProcessor classes.

For Example, lets add a new payment method:

```python
class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing paypal payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/open-closed-after.py
```

### **L**iskov Substitution


If you have objects in a program you should be able to substitute those objects with instances of their subtypes or subclasses without altering the correctness of the program.

for example with the next code:

```python
# code before
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order, security_code):
        pass

class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing paypal payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/liskov-substitution-before.py
```

Lets say that Paypal does not work with security code but with email adresses, but as the code is right now we would need to write something like this:

```python
class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing paypal payment type")
        print(f"Verifying email address: {security_code}")
        order.status = "paid"
```

The problem with this is that we are using the abstract class security_code as an email and therefore violating Liskov substitution principle, to call it we would need to do:

```python
order = Order()
order.add_item("Keyboard", 1, 50)
print(order.total_price())
processor = PaypalPaymentProcessor()
processor.pay(order, "jhon_perez@gmail.com")
```

but in this previous example we are using  security_code to pass email.


To solve this we should remove the method parameter and move it to the initializers so we can do different things depending on the class we create.

```python
# code after
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address):
        self.email_address = email_address

    def pay(self, order):
        print("Processing paypal payment type")
        print(f"Using email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
print(order.total_price())
processor = PaypalPaymentProcessor("hi@arjancodes.com")
processor.pay(order)
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/liskov-substitution-after.py
```

> Another great example is the following from this article: https://www.linkedin.com/pulse/solid-design-principles-python-examples-hiral-amodia/
> code can be found here: https://github.com/amodiahs/SOLID_Design_Principles/tree/master/Liskov_Substitution_Principle


```python
class Car():
  def __init__(self, type):
    self.type = type

class PetrolCar(Car):
  def __init__(self, type):
    self.type = type

car = Car("SUV")
car.properties = {"Color": "Red", "Gear": "Auto", "Capacity": 6}

petrol_car = PetrolCar("Sedan")
petrol_car.properties = ("Blue", "Manual", 4)

cars = [car, petrol_car]

def find_red_cars(cars):
  red_cars = 0
  for car in cars:
    if car.properties['Color'] == "Red":
      red_cars += 1
  print(f'Number of Red Cars = {red_cars}')

find_red_cars(cars)
# source: https://github.com/amodiahs/SOLID_Design_Principles/tree/master/
```

"""As we can see here, there is no standard specification to add properties of the Car and it is left to the developers to implement in the way convenient to them. One developer may implement it as a Dictionary and another may implement it as a Tuple and thus it can be implemented in multiple ways."""

"""As we can see here, we are trying to loop through a list of car objects. And here we break the Liskov Substitution principle as we cannot replace Super type Car’s objects with objects of Subtype PetrolCar in the function written to find Red cars."""

"""
A better way to implement this would be to introduce setter and getter methods in the Superclass Car using which we can set and get Car’s properties without leaving that implementation to individual developers.
"""

like the following code:
```python
# code after
class Car():
  def __init__(self, type):
    self.type = type
    self.car_properties = {}

  def set_properties(self, color, gear, capacity):
    self.car_properties = {"Color": color, "Gear": gear, "Capacity": capacity}

  def get_properties(self):
    return self.car_properties

class PetrolCar(Car):
  def __init__(self, type):
    self.type = type
    self.car_properties = {}

car = Car("SUV")
car.set_properties("Red", "Auto", 6)
petrol_car = PetrolCar("Sedan")
petrol_car.set_properties("Blue", "Manual", 4)
cars = [car, petrol_car]

def find_red_cars(cars):
  red_cars = 0
  for car in cars:
    if car.get_properties()['Color'] == "Red":
      red_cars += 1
  print(f'Number of Red Cars = {red_cars}')

find_red_cars(cars)
# source: https://github.com/amodiahs/SOLID_Design_Principles/tree/master/
```

### Interface Segregation

> "A client should never be forced to implement an interface that it doesn’t use, or clients shouldn’t be forced to depend on methods they do not use."

This suggest creating several and smaller interfaces  instead of a single large interface.

Consider the same code we have been working on with some modifications:

```python
# code before
class Order:
    #same as before, omitted for brevity
    (...)

class PaymentProcessor(ABC):
    @abstractmethod
    def auth_sms(self, code):
        pass

    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def auth_sms(self, code):
        raise Exception("Credit card payments don't support SMS code authorization.")

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address):
        self.email_address = email_address
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Using email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())
processor = DebitPaymentProcessor("2349875")
processor.auth_sms(465839)
processor.pay(order)
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/interface-segregation-before.py
```

The issue with the previous code is that CreditPaymentProcessor does not have two factor authentication so its weird to always raise an Exception for instances of this classes.

In this case not all subclasses support two factor authentication so its better separate interfaces for this. What we could do is add a second subclass of PaymentProcessor that support SMS authentication like this:

```python
#code after
from abc import ABC, abstractmethod

class Order:
    #same as before, omitted for brevity
    (...)

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class PaymentProcessor_SMS(PaymentProcessor):
    @abstractmethod
    def auth_sms(self, code):
        pass

    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor_SMS):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor_SMS):
    def __init__(self, email_address):
        self.email_address = email_address
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Using email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())
processor = PaypalPaymentProcessor("hi@arjancodes.com")
processor.auth_sms(465839)
processor.pay(order)
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/interface-segregation-after.py
```

On the previous code, instead of one general purpose interfaces we have splited with more meaningful behavior classes and several instances for each case when it support SMS authentication

Also is possible to use "composition" to apply interface segregation principle like the following code:
```python
from abc import ABC, abstractmethod

class Order:
  #same as before, omitted for brevity
  (...)

#create this new class
class SMSAuthorizer:
    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print(f"Verifying SMS code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass


class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizer: SMSAuthorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address, authorizer: SMSAuthorizer):
        self.email_address = email_address
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Using email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
print(order.total_price())
authorizer = SMSAuthorizer()
authorizer.verify_code(465839)
processor = PaypalPaymentProcessor("hi@arjancodes.com", authorizer)
processor.pay(order)
#source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/interface-segregation-after-comp.py
```

On previous code we created an SMSAuthorizer class that handles the functionality of authentication. Each class is responsible to handle their own authentication methods and each class implements it.

### Dependency Inversion


>Entities must depend on abstractions, not on concretions. It states that the high-level module must not depend on the low-level module, but they should depend on abstractions.

Lets see the code we have been working with and apply this principle:

```python
#code before
from abc import ABC, abstractmethod

class Order:
  #same as before, omitted for brevity
  (...)

class SMSAuthorizer:
    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print(f"Verifying SMS code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizer: SMSAuthorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address, authorizer: SMSAuthorizer):
        self.email_address = email_address
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Using email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())
authorizer = SMSAuthorizer()
# authorizer.verify_code(465839)
processor = PaypalPaymentProcessor("hi@arjancodes.com", authorizer)
processor.pay(order)
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/dependency-inversion-before.py
```

Here there is an issue, the main problem is that classes depend on specific authorizers (SMSAuthorizer) in order to solve this lets create another abstract Authorizer class to pass to the PaymentProcessor.

```python
#code after
from abc import ABC, abstractmethod

class Order:
  #same as before, omitted for brevity
  # (...)

class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

class Authorizer_SMS(Authorizer):
    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print(f"Verifying SMS code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizer: Authorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address, authorizer: Authorizer):
        self.email_address = email_address
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Using email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())
authorizer = Authorizer_Robot()
authorizer.verify_code(465839)
processor = PaypalPaymentProcessor("hi@arjancodes.com", authorizer)
processor.pay(order)
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/dependency-inversion-after.py
```

This principle is useful when you want to extend the code and create a new authorization method for example:

```python
class Authorizer_Robot(Authorizer):

    def __init__(self):
        self.authorized = False

    def not_a_robot(self):
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class Authorizer_Google(Authorizer):
    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print(f"Verifying Google auth code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized
# source: https://github.com/ArjanCodes/betterpython/blob/main/9%20-%20solid/dependency-inversion-after.py
```

sources:  
https://www.youtube.com/watch?v=pTB30aXS77U  
https://github.com/ArjanCodes/betterpython/tree/main/9%20-%20solid  
https://www.linkedin.com/pulse/solid-design-principles-python-examples-hiral-amodia/  
https://softwarecrafters.io/python/principios-solid-python  
https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design  
