




## I will contend that conceptual integrity is the most important consideration in system design.
## It is better to have a system omit certain anomalous features and improvements,
## but to reflect one set of design ideas, than to have one that contains many good but independent and uncoordinated ideas
## Fred Brooks - The Mytical Man-Month
## source: https://www.youtube.com/watch?v=Df0WVO-c3Sw


## Coupling: Coupling is the measure of the degree of interdependence between the modules. A good software will have low coupling.
## Cohesion: Cohesion is a measure of the degree to which the elements of the module are functionally related. It is the degree to which
## all elements directed towards performing a single task are contained in the component. Basically, cohesion is the internal glue that
## keeps the module together. A good software design will have high cohesion.
## source: https://www.geeksforgeeks.org/software-engineering-coupling-and-cohesion/

## To remember:
## Good software will have
## Coupling --> low
## Cohesion --> high

## in order to add functions or modules easier, also refactor is made easier
## redability is also increased by keeping info and their calculation together


## great video explaning concepts
##  When one class uses other class methods, has high coupliing
## also called spaguetti code which is fragile vs rigid
## fragile is when one change may breake many parts
## the lower the coupling the more easy to manting
## the lower the coupling is more usefull it is
## source: https://www.youtube.com/watch?v=6UGepSuS0sY



## All code and ideas from video https://youtu.be/eiDyK_ofPPM
## and https://github.com/ArjanCodes/betterpython/tree/main/1%20-%20coupling%20and%20cohesion
################################################################################
## BEFORE CODE
import string
import random
class VehicleRegistry:

    def generate_vehicle_id(self, length):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id):
        return f"{id[:2]}-{''.join(random.choices(string.digits, k=2))}-{''.join(random.choices(string.ascii_uppercase, k=2))}"


class Application:

    ## This method has low cohesion because is in charge of doing a lot of things (way to many responsabilities)
    ## and also high coppling because if any change in Vehicle Registry is made, this method will need changes also.
    ## It ss better to have low coupling
    ## Its better to keep cohesion high
    def register_vehicle(self, brand: string):
        # create a registry instance
        registry = VehicleRegistry()

        # generate a vehicle id of length 12
        vehicle_id = registry.generate_vehicle_id(12)

        # now generate a license plate for the vehicle
        # using the first two characters of the vehicle id
        license_plate = registry.generate_vehicle_license(vehicle_id)


        ## direct coupling of brand and catalogue price
        ## mesy code will need to add another if statment for every new car
        # compute the catalogue price
        catalogue_price = 0
        if brand == "Tesla Model 3":
            catalogue_price = 60000
        elif brand == "Volkswagen ID3":
            catalogue_price = 35000
        elif brand == "BMW 5":
            catalogue_price = 45000

        ## also here we ca see there is a direct coupling between the brand and tax percentage
        # compute the tax percentage (default 5% of the catalogue price, except for electric cars where it is 2%)
        tax_percentage = 0.05
        if brand == "Tesla Model 3" or brand == "Volkswagen ID3":
            tax_percentage = 0.02

        # compute the payable tax
        payable_tax = tax_percentage * catalogue_price

        # print out the vehicle registration information
        print("Registration complete. Vehicle information:")
        print(f"Brand: {brand}")
        print(f"Id: {vehicle_id}")
        print(f"License plate: {license_plate}")
        print(f"Payable tax: {payable_tax}")

app = Application()
app.register_vehicle("Volkswagen ID3")


################################################################################
# AFTER CODE
import string
import random


## here all thata is stored ore logically and methods do specific things regarding their
## data objects, for ex. VehicleInfo is now in charge of caluclating taxes
## each method only has one responsability
## function are closed to the data that they compute
## coupling here is pretty low
class VehicleInfo:

    def __init__(self, brand, electric, catalogue_price):
        self.brand = brand
        self.electric = electric
        self.catalogue_price = catalogue_price

    def compute_tax(self):
        tax_percentage = 0.05
        if self.electric:
            tax_percentage = 0.02
        return tax_percentage * self.catalogue_price

    def print(self):
        print(f"Brand: {self.brand}")
        print(f"Payable tax: {self.compute_tax()}")

class Vehicle:

    def __init__(self, id, license_plate, info):
        self.id = id
        self.license_plate = license_plate
        self.info = info

    def print(self):
        print(f"Id: {self.id}")
        print(f"License plate: {self.license_plate}")
        self.info.print()


class VehicleRegistry:

    def __init__(self):
        ## probably this will look diferent in a real wolrd app, for ex, fetching data base
        self.vehicle_info = { }
        self.add_vehicle_info("Tesla Model 3", True, 60000)
        self.add_vehicle_info("Volkswagen ID3", True, 35000)
        self.add_vehicle_info("BMW 5", False, 45000)
        self.add_vehicle_info("Tesla Model S", True, 90000)

    def add_vehicle_info(self, brand, electric, catalogue_price):
        self.vehicle_info[brand] = VehicleInfo(brand, electric, catalogue_price)

    def generate_vehicle_id(self, length):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id):
        return f"{id[:2]}-{''.join(random.choices(string.digits, k=2))}-{''.join(random.choices(string.ascii_uppercase, k=2))}"

    def create_vehicle(self, brand):
        id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(id)
        return Vehicle(id, license_plate, self.vehicle_info[brand])


class Application:

    def register_vehicle(self, brand: string):
        # create a registry instance
        registry = VehicleRegistry()


        ## some coupling is ineveitbale (and necesary) because here registry needs to know that the Vehicle Registry has a method: create_vehicle
        return registry.create_vehicle(brand)



app = Application()
vehicle = app.register_vehicle("Volkswagen ID3")
vehicle.print()
