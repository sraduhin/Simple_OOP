from time import sleep


class Button:

    def __init__(self, floor):
        self.__floor = floor
        self.__state = False

    @property
    def floor(self):
        return self.__floor

    @property
    def state(self):
        return self.__state

    @property
    def is_active(self):
        return self.__state is True

    def push_the_button(self):
        if not self.state:
            print(f"{self.floor}th floor was requested")
        self.__state = not self.__state


class Doors:
    OPEN_DELAY = 3

    def __init__(self, floor):
        self.__floor = floor
        self.__is_open = False

    @property
    def is_open(self):
        return self.__is_open

    @property
    def floor(self):
        return self.__floor

    def open(self):
        self.__is_open = True
        print(f"Doors opened on the {self.floor}th floor")
        sleep(self.OPEN_DELAY)
        print(f"Doors closed on the {self.floor}th floor")
        self.__is_open = False


class Elevator:
    MOVING_DELAY = 1
    UP, DOWN, STOP = DIRECTION_LIST = ["up", "down", "stop"]
    DIRECTIONS = {i: i for i in DIRECTION_LIST}

    def __init__(self, floors):
        self._verify_floors(floors)
        self.__floors = floors
        self.__current_floor = 1
        self.__direction = 'stoped'
        self.doors = [Doors(i) for i in range(self.floors)]
        self.floor_buttons = [Button(i) for i in range(self.floors)]
        self.lift_buttons = [Button(i) for i in range(self.floors)]

    @classmethod
    def _verify_floors(cls, floors):
        if type(floors) != int or floors < 2:
            raise TypeError("Incorrect parameters")

    def _verify_manual_input(self, button):
        if button not in range(1, self.floors + 1):
            raise ValueError(f"Out of range. Must be in [1, {self.floors}")

    @property
    def floors(self):
        return self.__floors

    @property
    def requested_floors(self):
        return [button.floor for button in self.floor_buttons if button.is_active]

    @property
    def requested_floor(self):
        """Getting the nearest floor according to direction"""
        pushed_floors = self.requested_floors
        match len(pushed_floors):
            case 0:
                return None
            case 1:
                return self.requested_floors[0]
            case _:
                if self.direction == self.DIRECTIONS[self.UP]:
                    return min(floor for floor in pushed_floors if floor >= self.current_floor)
                return max(floor for floor in pushed_floors if floor >= self.current_floor)

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value: str):
        self.__direction = value

    @property
    def current_floor(self):
        return self.__current_floor

    @current_floor.setter
    def current_floor(self, value):
        print(f"current_floor: {value}")
        self.__current_floor = value

    def _move(self, direction):
        print(f"Lift moving {direction}")
        sleep(self.MOVING_DELAY)
        multiplier = 1 if direction == self.DIRECTIONS[self.UP] else -1
        self.current_floor += 1 * multiplier

    def _set_direction(self):
        if self.current_floor > self.requested_floor:
            self.direction = self.DIRECTIONS[self.DOWN]
        else:
            self.direction = self.DIRECTIONS[self.UP]

    def button_handler(self):
        button = input("Enter some button or skip: ")
        if button:
            button = int(button)
            self._verify_manual_input(button)
            self.floor_buttons[button].push_the_button()

    def start(self):
        while True:
            self.button_handler()
            if not self.requested_floor:
                continue
            while self.current_floor != self.requested_floor:
                self.button_handler()
                self._set_direction()
                self._move(self.direction)
            self.floor_buttons[self.current_floor].push_the_button()
            self.doors[self.current_floor].open()


num_floors = int(input("Create an elevator with count of floors: "))
elevator = Elevator(num_floors)
print(f"You've been create an elevator with {elevator.floors} floors")
elevator.start()
