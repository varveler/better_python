# **SOLID** Design Principles

These principles establish practices that lend to developing software with considerations for maintaining and extending as the project grows. Adopting these practices can also contribute to avoiding code smells, refactoring code, and Agile or Adaptive software development.  

> Was published in year 2000 by Robert C. Martin AKA "Uncle Bob"

**SOLID** is an acronym/acrostic for 5 design principles:

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
"Let q(x) be a property provable about objects of x of type T. Then q(y) should be provable for objects y of type S where S is a subtype of T."

> This means that every subclass or derived class should be substitutable for their base or parent class.

#### **Interface Segregation** Principle
"A client should never be forced to implement an interface that it doesn’t use, or clients shouldn’t be forced to depend on methods they do not use."


#### **Dependency Inversion** Principle
"Entities must depend on abstractions, not on concretions. It states that the high-level module must not depend on the low-level module, but they should depend on abstractions."

In order to understand deeply these principles lets look at code examples for each principle.

## Code Examples for each principle:

### **S**ingle Responsabilty

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
```
Now we have each object, payment and order each with their own responsibilities

Here is another example:

```python
# code before
# source: https://softwarecrafters.io/python/principios-solid-python
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
```
In the example before Vehicle class is responsible for initiating a Vehicle, Saving to database and printing/presenting the info.

Applying Single Responsibility design principle means we can separate presentation (printing) logic from business logic from saving to database logic.

```python
# code after
# source: https://softwarecrafters.io/python/principios-solid-python
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
```

**Single Responsibility** Principle increases **Cohesion**, so function are closed to the data that they compute and have less responsibilities. This principle ensures that each class can be reused in other parts of the code for latter purposes.


### **O**pen/Closed

to be continued...



sources:  
https://github.com/ArjanCodes/betterpython/tree/main/9%20-%20solid
https://www.youtube.com/watch?v=pTB30aXS77U
https://softwarecrafters.io/python/principios-solid-python
https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
