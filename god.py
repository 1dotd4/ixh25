import random
from player import Car
from gameserver import GameServer

class God:
    def __init__(self):
        self.flags: dict[int, list[int]] = {}
        self.coeff = [random.randint(0, 21) for _ in range(10)]

    def create_flags(self, car: Car) -> list[int]:
        flags = [random.randint(1, 999) for _ in range(10)]
        self.flags[car.id] = flags
        return flags
    
    def update_flags(self, car: Car, training_list: list[int] = [0]*10) -> None:
        delta = random.randint(-20,20)
        new_flags = [(f + b*delta) % 1001 for f,b in zip(self.flags[car.id], training_list)]
        self.flags[car.id] = new_flags

    def create_shares(self, car_id: int, server_list: list[GameServer]) -> None:
        shares = []
        for f,c in zip(self.flags[car_id], self.coeff):
            s = c * (f % 1001)
            shares.append(self.secret_sharing(s, len(server_list)))
        for i in range(len(server_list)):
            vec = [shares[j][i] for j in range(len(shares))]
            server_list[i].receive_shares(car_id, vec)
        return 

    def calculate_speed(self, car: Car, training_list: list[int] = [0]*10) -> int:
        flags = self.flags.get(car.id)
        if flags is None:
            flags = self.create_flags(car)
        speed = sum((f+b) * c for f,c,b in zip(flags, self.coeff, training_list))
        car.speed = speed
        return speed

    def secret_sharing(self, secret: int, n_shares: int) -> list[int]:
        if n_shares < 1:
            raise ValueError("n_shares must be >= 1")
        shares: list[int] = []
        for _ in range(max(0, n_shares - 1)):
            shares.append(random.randint(0, 1000)) 
        last = secret - sum(shares) 
        shares.append(last) 
        return shares
