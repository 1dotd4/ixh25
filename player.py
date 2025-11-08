import random
from typing import Optional

class Car:
    def __init__(self, id: int = 1):
        self.id = id
        self.speed: Optional[int] = None

class Player:
    def __init__(self, id: int):
        self.id = id
        self.car: Car = Car(id=id)
        self.token = 10

    def reconstruct_speed(self, car_id: int, server_list) -> int: 
        """Reconstruct the speed by summing shares stored on all servers."""
        total = 0
        for server in server_list:
            shares: list = server.get_shares(car_id) 
            total += sum(shares) 
        return total

    def training_vector(self) -> list:
        return [random.randint(0,1) for _ in range(10)]
