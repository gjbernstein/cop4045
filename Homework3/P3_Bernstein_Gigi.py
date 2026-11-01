'''predator-prey-human simulation on a 2d island grid.'''

from __future__ import annotations

import random
from typing import Type

import matplotlib.pyplot as plt


class Island:
	'''n-by-n grid that stores prey, predators, and humans'''

	def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0, count_humans: int = 0) -> None:
		'''create an island and randomly place the initial population
        preconditions: 
		    - n is positive;
		    - all population counts are nonnegative;
		    - their sum does not exceed grid capacity
		postconditions: 
		    - grid contains the requested number of each class'''
		if n <= 0:
			raise ValueError("island size must be positive")
		populations = (prey_count, predator_count, count_humans)
		if any(count < 0 for count in populations):
			raise ValueError("population counts cannot be negative")
		if sum(populations) > n * n:
			raise ValueError("initial population exceeds island capacity")

		self.grid_size: int = n
		self.grid: list[list[Animal | int]] = [[0 for _ in range(n)] for _ in range(n)]
		self.init_animals(prey_count, predator_count, count_humans)

	def init_animals(
		self, prey_count: int, predator_count: int, count_humans: int
	) -> None:
		'''randomly place requested numbers of prey, predators, and humans
        paramaters:
            - prey_count: number of prey to place
            - predator_count: number of predators to place
            - count_humans: number of humans to place
        returns: None'''
		self._place_random_animals(prey_count, Prey)
		self._place_random_animals(predator_count, Predator)
		self._place_random_animals(count_humans, Human)

	def _place_random_animals(self, count: int, animal_class: Type[Animal]) -> None:
		'''place count instances of animal_class in randomly selected empty cells
        paramaters:
            - count: number of animals to place
            - animal_class: the class of animals to place
        returns: None'''
		placed = 0
		while placed < count:
			x = random.randrange(self.grid_size)
			y = random.randrange(self.grid_size)
			if not self.animal(x, y):
				self.register(animal_class(island=self, x=x, y=y))
				placed += 1

	def clear_all_moved_flags(self) -> None:
		'''reset every animal's moved flag before a new time unit begins
        paramaters: None
        returns: None'''
		for column in self.grid:
			for occupant in column:
				if isinstance(occupant, Animal):
					occupant.clear_moved_flag()

	def size(self) -> int:
		'''return the length of one side of the square island
        paramaters: None
        returns: int'''
		return self.grid_size

	def register(self, animal: Animal) -> None:
		'''place animal in the grid cell matching its current coordinates
        paramaters:
            - animal: the animal to place
        returns: None'''
		self.grid[animal.x][animal.y] = animal

	def remove(self, animal: Animal) -> None:
		'''empty animal's current grid cell if that cell still contains it
        paramaters:
            - animal: the animal to remove
        returns: None'''
		if self.grid[animal.x][animal.y] is animal:
			self.grid[animal.x][animal.y] = 0

	def animal(self, x: int, y: int) -> Animal | int:
		'''return the occupant at (x, y), or -1 when coordinates are out of bounds
        paramaters:
            - x: the x-coordinate
            - y: the y-coordinate
        returns: Animal | int'''
		if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
			return self.grid[x][y]
		return -1

	def __str__(self) -> str:
		'''return a grid display with the island's lower-left cell at the bottom
        paramaters: None
        returns: str'''
		rows: list[str] = []
		for y in range(self.grid_size - 1, -1, -1):
			row = []
			for x in range(self.grid_size):
				occupant = self.grid[x][y]
				row.append(str(occupant) if isinstance(occupant, Animal) else ".")
			rows.append(" ".join(row))
		return "\n".join(rows)

	def count_prey(self) -> int:
		'''return the number of Prey objects currently on the grid
        paramaters: None
        returns: int'''
		return sum(
			isinstance(occupant, Prey)
			for column in self.grid
			for occupant in column
		)

	def count_predators(self) -> int:
		'''return the number of Predator objects currently on the grid
        paramaters: None
        returns: int'''
		return sum(
			isinstance(occupant, Predator)
			for column in self.grid
			for occupant in column
		)

	def count_humans(self) -> int:
		'''return the number of Human objects currently on the grid
        paramaters: None
        returns: int'''
		return sum(
			isinstance(occupant, Human)
			for column in self.grid
			for occupant in column
		)


class Animal:
	'''Base class for entities that move and breed on an Island.'''

	breed_time: int
	breed_clock: int

	def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "A") -> None:
		'''initialize an animal at (x, y) on island with display symbol s
        paramaters:
            - island: the island on which the animal resides
            - x: the x-coordinate
            - y: the y-coordinate
            - s: the display symbol
        returns: None'''
		self.island: Island = island
		self.name: str = s
		self.x: int = x
		self.y: int = y
		self.moved: bool = False

	def position(self) -> tuple[int, int]:
		'''return the animal's current (x, y) coordinates
        paramaters: none
        returns: tuple[int, int]'''
		return self.x, self.y

	def __str__(self) -> str:
		'''return the animal's one-character grid symbol
        paramaters: none
        returns: str'''
		return self.name

	def check_grid(self, type_looking_for: type = int) -> tuple[int, int] | int:
		'''return a neighboring cell containing the exact requested type, or 0
        paramaters:
            - type_looking_for: the type of animal to look for
        returns: tuple[int, int] | int'''
		offsets = ((-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1))
		for dx, dy in offsets:
			x = self.x + dx
			y = self.y + dy
			if 0 <= x < self.island.size() and 0 <= y < self.island.size():
				if type(self.island.animal(x, y)) is type_looking_for:
					return x, y
		return 0

	def _move_to(self, location: tuple[int, int]) -> None:
		'''move this animal into location and mark it as moved for this time unit
        paramaters:
            - location: the (x, y) coordinates to move to
        returns: none'''
		self.island.remove(self)
		self.x, self.y = location
		self.island.register(self)
		self.moved = True

	def move(self) -> None:
		'''move to the first neighboring empty cell unless already moved
        paramaters: none
        returns: None'''
		if not self.moved:
			location = self.check_grid(int)
			if isinstance(location, tuple):
				self._move_to(location)

	def breed(self) -> None:
		'''create an offspring in a neighboring empty cell when breed_clock expires
        paramaters: none
        returns: none'''
		if self.breed_clock <= 0:
			location = self.check_grid(int)
			if isinstance(location, tuple):
				self.breed_clock = self.breed_time
				offspring = type(self)(self.island, x=location[0], y=location[1])
				self.island.register(offspring)

	def clear_moved_flag(self) -> None:
		'''mark the animal as not yet moved during the next time unit
        paramaters: none
        returns: none'''
		self.moved = False


class Prey(Animal):
	'''An animal that moves and breeds but does not eat other animals.'''

	breed_time: int = 3

	def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "O") -> None:
		'''create prey and initialize its breeding clock from Prey.breed_time
        paramaters:
            - island: the island on which the prey resides
            - x: the x-coordinate
            - y: the y-coordinate
            - s: the display symbol
        returns: None'''
		super().__init__(island, x, y, s)
		self.breed_clock = self.breed_time

	def clock_tick(self) -> None:
		'''advance the breeding clock by one time unit
        paramaters: none
        returns: none'''
		self.breed_clock -= 1


class Predator(Animal):
	'''An animal that eats prey and starves when it cannot eat in time.'''

	breed_time: int = 6
	starve_time: int = 3

	def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "X") -> None:
		'''create a predator and initialize breeding and starvation clocks
        paramaters:
            - island: the island on which the predator resides
            - x: the x-coordinate
            - y: the y-coordinate
            - s: the display symbol
        returns: None'''
		super().__init__(island, x, y, s)
		self.starve_clock: int = self.starve_time
		self.breed_clock = self.breed_time

	def clock_tick(self) -> None:
		'''advance clocks and remove the predator if its starvation clock expires
        paramaters: none
        returns: none'''
		self.breed_clock -= 1
		self.starve_clock -= 1
		if self.starve_clock <= 0:
			self.island.remove(self)

	def eat(self) -> None:
		'''eat a neighboring Prey, move into its cell, and reset starvation
        paramaters: none
        returns: none'''
		if not self.moved:
			location = self.check_grid(Prey)
			if isinstance(location, tuple):
				prey = self.island.animal(*location)
				if isinstance(prey, Prey):
					self.island.remove(prey)
					self._move_to(location)
					self.starve_clock = self.starve_time


class Human(Animal):
	'''An animal that periodically hunts predators and can itself starve.'''

	hunt_time: int = 4
	starve_time: int = 12
	breed_time: int = 8

	def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "H") -> None:
		'''create a human with clocks initialized from Human's class attributes
        paramaters:
            - island: the island on which the human resides
            - x: the x-coordinate
            - y: the y-coordinate
            - s: the display symbol
        returns: None'''
		super().__init__(island, x, y, s)
		self.hunt_clock: int = self.hunt_time
		self.starve_clock: int = self.starve_time
		self.breed_clock = self.breed_time

	def eat(self) -> None:
		'''hunt at each hunt_time interval, eating a neighboring Predator if found
        paramaters: none
        returns: none

		A successful hunt moves the human into the predator's cell and resets its
		starvation clock. Prey are never targeted by this method.
		'''
		self.hunt_clock -= 1
		if self.hunt_clock > 0:
			return
		self.hunt_clock = self.hunt_time
		if not self.moved:
			location = self.check_grid(Predator)
			if isinstance(location, tuple):
				predator = self.island.animal(*location)
				if isinstance(predator, Predator):
					self.island.remove(predator)
					self._move_to(location)
					self.starve_clock = self.starve_time

	def clock_tick(self) -> None:
		'''advance human clocks and remove the human if it starves
        paramaters: none
        returns: none'''
		self.breed_clock -= 1
		self.starve_clock -= 1
		if self.starve_clock <= 0:
			self.island.remove(self)


def main(
	predator_breed_time: int = 6,
	predator_starve_time: int = 3,
	initial_predators: int = 10,
	prey_breed_time: int = 3,
	initial_prey: int = 50,
	size: int = 10,
	ticks: int = 1000,
	human_hunt_time: int = 4,
	human_starve_time: int = 12,
	human_breed_time: int = 8,
    initial_humans: int = 2) -> tuple[list[int], list[int], list[int]]:
	'''Run the island simulation, plot populations, and return their histories.
	parameters: 
	    - the *_time arguments set class clock periods
	    - the initial_* arguments set starting populations
	    - size is the grid width
	    - ticks is capped at 1000
	    - set starting populations; size is the grid width; ticks is capped at 1000.
	    - simulation stops after 20 time units in a row with unchanged counts or when tick limit is reached
	returns:
	    - returned lists include time zero.
	'''
	if ticks < 0:
		raise ValueError("ticks cannot be negative")
	if any(clock <= 0 for clock in (
			predator_breed_time,
			predator_starve_time,
			prey_breed_time,
			human_hunt_time,
			human_starve_time,
			human_breed_time,)):
		raise ValueError("all clock periods must be positive")

	Predator.breed_time = predator_breed_time
	Predator.starve_time = predator_starve_time
	Prey.breed_time = prey_breed_time
	Human.hunt_time = human_hunt_time
	Human.starve_time = human_starve_time
	Human.breed_time = human_breed_time

	island = Island(size, initial_prey, initial_predators, initial_humans)
	print("Initial island:")
	print(island)

	prey_history = [island.count_prey()]
	predator_history = [island.count_predators()]
	human_history = [island.count_humans()]
	unchanged_ticks = 0
	stability_window = 20

	# Snapshotting ensures every animal present at tick start acts at most once.
	for tick in range(min(ticks, 1000)):
		island.clear_all_moved_flags()
		animals = [
			occupant
			for column in island.grid
			for occupant in column
			if isinstance(occupant, Animal)
		]
		for animal in animals:
			if island.animal(animal.x, animal.y) is not animal:
				continue
			if isinstance(animal, (Predator, Human)):
				animal.eat()
			animal.move()
			animal.breed()
			animal.clock_tick()

		current_counts = (
			island.count_prey(),
			island.count_predators(),
			island.count_humans(),
		)
		previous_counts = (
			prey_history[-1],
			predator_history[-1],
			human_history[-1],
		)
		prey_history.append(current_counts[0])
		predator_history.append(current_counts[1])
		human_history.append(current_counts[2])
		unchanged_ticks = unchanged_ticks + 1 if current_counts == previous_counts else 0

		if tick % 10 == 0:
			print(f"Tick {tick + 1}: prey={current_counts[0]}, predators={current_counts[1]}, humans={current_counts[2]}")
		if unchanged_ticks >= stability_window:
			print(f"Populations remained constant for {stability_window} ticks.")
			break

	print("name: Gigi Bernstein")
	print("Z number: Z23652485")

	print("Final island:")
	print(island)

	plt.plot(prey_history, label="Prey")
	plt.plot(predator_history, label="Predators")
	plt.plot(human_history, label="Humans")
	plt.xlabel("Time unit")
	plt.ylabel("Population")
	plt.title("Island Population Over Time")
	plt.legend()
	plt.tight_layout()
	plt.show()
	return prey_history, predator_history, human_history


if __name__ == "__main__":
	main()


