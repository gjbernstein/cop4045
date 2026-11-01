
class ParkingPermit:
    '''Base class for parking permits.
    attributes:
        owner_name (str): name of permit owner
        months_purchased (int): number of months the permit is valid for
        fee_schedule (dict): dictionary of fees associated with the permit
    methods:
        cost() -> float: calculates the total cost of the permit based on fee schedule
        __str__() -> str: returns a string representation of the permit
        __repr__() -> str: returns a detailed string representation of the permit
    '''
    def __init__(self, owner_name: str, months_purchased: int, fee_schedule: dict) -> None:
        '''initializes a ParkingPermit instance.
        parameters:
            owner_name (str): name of permit owner
            months_purchased (int): number of months the permit is valid for
            fee_schedule (dict): dictionary of fees associated with the permit
        '''
        self.owner_name = owner_name
        self.months_purchased = months_purchased
        self.fee_schedule = fee_schedule

    def cost(self) -> float:
        '''calculates the total cost of the permit based on the fee schedule.
        parameters:
            none
        returns:
            float - the total cost of the permit'''
        total = 0
        for fee_type, fee_amount in self.fee_schedule.items():
            total += fee_amount
        return total

    def __str__(self) -> str:
        '''returns a string representation of the permit.
        parameters:
            none
        returns:
            str - a string representation of the permit'''
        return f"ParkingPermit(owner_name={self.owner_name}, months_purchased={self.months_purchased}, fee_schedule={self.fee_schedule})"

    def __repr__(self) -> str:
        '''returns a detailed string representation of the permit.
        parameters:
            none
        returns:
            str - a detailed string representation of the permit'''
        return f"ParkingPermit(owner_name={self.owner_name}, months_purchased={self.months_purchased}, fee_schedule={self.fee_schedule})"

class StudentPermit(ParkingPermit):
    '''class representing a student parking permit
    inherits from ParkingPermit
    attributes:
        num_vehicles (int): number of vehicles covered by the student permit'''
    def __init__(self, owner_name: str, months_purchased: int, fee_schedule: dict, num_vehicles: int) -> None:
        '''initializes a StudentPermit instance.
        parameters:
            owner_name (str): name of the permit owner
            months_purchased (int): number of months the permit is valid
            fee_schedule (dict): dictionary of fees associated with the permit
            num_vehicles (int): number of vehicles covered by the student permit
        returns:
            none'''
        super().__init__(owner_name, months_purchased, fee_schedule)
        self.num_vehicles = num_vehicles

    def cost(self) -> float:
        '''calculates the total cost of the student permit.
        parameters:
            none
        returns:
            float - total cost of the student permit'''
        total = super().cost()
        total += 25 * self.months_purchased
        if self.num_vehicles > 1:
            total += 10 * (self.num_vehicles - 1)
        return total

    def __str__(self) -> str:
        '''returns a string representation of the student permit.
        parameters:
            none
        returns:
            str - a string representation of the student permit'''
        return f"StudentPermit(owner_name={self.owner_name}, months_purchased={self.months_purchased}, fee_schedule={self.fee_schedule}, num_vehicles={self.num_vehicles})"

    def __repr__(self) -> str:
        '''returns a detailed string representation of the student permit.
        parameters:
            none
        returns:
            str - a detailed string representation of the student permit'''
        return f"StudentPermit(owner_name={self.owner_name}, months_purchased={self.months_purchased}, fee_schedule={self.fee_schedule}, num_vehicles={self.num_vehicles})"

class FacultyPermit(ParkingPermit):
    '''class representing a faculty parking permit
    inherits from ParkingPermit
    attributes:
        garage_access (bool): indicates if the faculty permit includes garage access'''
    def __init__(self, owner_name: str, months_purchased: int, fee_schedule: dict, garage_access: bool) -> None:
        '''initializes a FacultyPermit instance.
        parameters:
            owner_name (str): name of the permit owner
            months_purchased (int): number of months the permit is valid
            fee_schedule (dict): dictionary of fees associated with the permit
            garage_access (bool): indicates if the faculty permit includes garage access
        returns:
            none'''
        super().__init__(owner_name, months_purchased, fee_schedule)
        self.garage_access = garage_access

    def cost(self) -> float:
        '''calculates the total cost of the faculty permit.
        parameters:
            none
        returns:
            float - total cost of the faculty permit'''
        total = super().cost()
        total += 40 * self.months_purchased
        if self.garage_access:
            total += 15 * self.months_purchased
        return total

    def __str__(self) -> str:
        '''returns a string representation of the faculty permit.
        parameters:
            none
        returns:
            str - a string representation of the faculty permit'''
        return f"FacultyPermit(owner_name={self.owner_name}, months_purchased={self.months_purchased}, fee_schedule={self.fee_schedule}, garage_access={self.garage_access})"

    def __repr__(self) -> str:
        '''returns a detailed string representation of the faculty permit.
        parameters:
            none
        returns:
            str - a detailed string representation of the faculty permit'''
        return f"FacultyPermit(owner_name={self.owner_name}, months_purchased={self.months_purchased}, fee_schedule={self.fee_schedule}, garage_access={self.garage_access})"

def main():
    '''main function to demonstrate the use of StudentPermit and FacultyPermit classes.'''
    student_permit = StudentPermit("Abby West", 6, {"monthly": 50}, 1)
    faculty_permit = FacultyPermit("JStella Rose", 12, {"monthly": 100}, True)

    print("name: Gigi Bernstein")
    print("Z number: Z23652485")

    print(student_permit)
    print(f"student permit cost: {student_permit.cost()}")

    print(faculty_permit)
    print(f"faculty permit cost: {faculty_permit.cost()}")

if __name__ == "__main__":
    main()