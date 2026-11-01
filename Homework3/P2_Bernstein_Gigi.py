
import math
import turtle


def _leaf_centerline_point(progress: float, blade_length: float, curve_amount: float) -> tuple[float, float]:
    return curve_amount * math.sin(math.pi * progress), blade_length * progress


def _draw_leaf_vein(
    length: float,
    base_heading: float,
    side: int,
    recursion_level: int,
    curved: bool,
    branch_angle: float = 52,
) -> None:
    start_position = turtle.position()
    turtle.setheading(base_heading + side * branch_angle)

    if curved:
        for _ in range(10):
            turtle.forward(length / 10)
            turtle.left(side * 0.8)
    else:
        turtle.forward(length)

    end_heading = turtle.heading()
    if recursion_level > 1:
        child_length = length * 0.48
        _draw_leaf_vein(child_length, end_heading, -1, recursion_level - 1, curved, 34)
        _draw_leaf_vein(child_length, end_heading, 1, recursion_level - 1, curved, 34)

    turtle.penup()
    turtle.goto(start_position)
    turtle.setheading(base_heading)
    turtle.pendown()


def _draw_leaf(
    recursion_level: int,
    petiole_length: float,
    curved: bool,
    start_position: tuple[float, float],
) -> None:
    if recursion_level < 1:
        raise ValueError("recursion_level must be at least 1")
    if petiole_length <= 0:
        raise ValueError("petiole_length must be positive")

    turtle.delay(0)
    turtle.penup()
    turtle.goto(start_position)
    turtle.setheading(90)
    turtle.pendown()
    turtle.forward(petiole_length)

    blade_length = petiole_length * 1.5
    curve_amount = blade_length * 0.24 if curved else 0
    blade_start = turtle.position()

    if curved:
        for step in range(1, 41):
            progress = step / 40
            x, y = _leaf_centerline_point(progress, blade_length, curve_amount)
            turtle.goto(blade_start[0] + x, blade_start[1] + y)
    else:
        turtle.forward(blade_length)

    station_count = max(4, recursion_level * 2 + 2)
    for station in range(1, station_count + 1):
        progress = station / (station_count + 1)
        if curved:
            x, y = _leaf_centerline_point(progress, blade_length, curve_amount)
            tangent = math.degrees(
                math.atan2(
                    blade_length,
                    curve_amount * math.pi * math.cos(math.pi * progress),
                )
            )
        else:
            x, y = 0, blade_length * progress
            tangent = 90

        turtle.penup()
        turtle.goto(blade_start[0] + x, blade_start[1] + y)
        turtle.setheading(tangent)
        turtle.pendown()
        vein_length = blade_length * 0.34 * math.sin(math.pi * progress)
        _draw_leaf_vein(vein_length, tangent, -1, recursion_level, curved)
        _draw_leaf_vein(vein_length, tangent, 1, recursion_level, curved)

    turtle.penup()
    turtle.goto(blade_start[0] + curve_amount * math.sin(math.pi), blade_start[1] + blade_length)
    turtle.setheading(90)
    turtle.pendown()


def draw_leaf_straight(
    recursion_level: int,
    petiole_length: float,
    start_position: tuple[float, float] = (0, 0),
) -> None:
    '''draw a vertical, straight-midrib leaf with recursively branching veins'''
    _draw_leaf(recursion_level, petiole_length, curved=False, start_position=start_position)


def draw_leaf_curved(
    recursion_level: int,
    petiole_length: float,
    start_position: tuple[float, float] = (0, 0),
) -> None:
    '''draw a vertical leaf with a curved midrib and curved recursive veins'''
    _draw_leaf(recursion_level, petiole_length, curved=True, start_position=start_position)


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
    faculty_permit = FacultyPermit("Stella Rose", 12, {"monthly": 100}, True)

    print("name: Gigi Bernstein")
    print("Z number: Z23652485")

    print(student_permit)
    print(f"student permit cost: {student_permit.cost()}")

    print(faculty_permit)
    print(f"faculty permit cost: {faculty_permit.cost()}")

    print("\nleaf drawings:")
    turtle.setup(width=700, height=500)
    turtle.title("recursive leaves")
    draw_leaf_straight(2, 80, (-160, -180))
    draw_leaf_curved(2, 80, (160, -180))
    turtle.penup()
    turtle.goto(-230, -225)
    turtle.write("Straight", align="center", font=("Arial", 14, "normal"))
    turtle.goto(160, -225)
    turtle.write("Curved", align="center", font=("Arial", 14, "normal"))
    turtle.done()

if __name__ == "__main__":
    main()