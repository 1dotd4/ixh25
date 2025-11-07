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

    def reconstruct_speed(self, car_id: int, server_list: list[Server]) -> int:
        """Reconstruct the speed by summing shares stored on all servers."""
        total = 0
        for server in server_list:
            shares: list = server.get_share(car_id) 
            total += sum(shares) 
        return total

    def send_training_request(self) -> bool:
        pass

class Server:
    def __init__(self, id: int):
        self.id = id
        self.shares: dict[int, list[int]] = {}

    def handle_training_request(self, user: Player) -> bool:
        if user.token < 0:
            # raise ValueError("Not enough tokens.")
            return False
        else:
            user.token -= 1
            return True
        
    def receive_payment(self) -> bool:
        pass

    def receive_shares(self, car_id: int, share: list[int]) -> None:
        self.shares[car_id] = share

    def get_share(self, car_id: int) -> Optional[int]:
        return self.shares.get(car_id)

class God:
    def __init__(self):
        self.flags: dict[int, list[int]] = {}
        self.coeff = [random.randint(-10, 10) for _ in range(10)]

    def create_flags(self, car: Car) -> list[int]:
        flags = [random.randint(0, 1000) for _ in range(10)]
        self.flags[car.id] = flags
        return flags

    def create_shares(self, car_id: int) -> dict[int, list[int]]:
        if car_id not in self.flags:
            tmp = Car(id=car_id)
            self.create_flags(tmp)
        return {car_id: self.flags[car_id]}

    def calculate_speed(self, car: Car) -> int:
        flags = self.flags.get(car.id)
        if flags is None:
            flags = self.create_flags(car)
        speed = sum(f * c for f, c in zip(flags, self.coeff))
        car.speed = speed
        return speed

    def secret_share_speed(self, car: Car, n_shares: int) -> list[int]:
        """Split the car.speed (computed) into n_shares additive shares.

        This is a simple additive secret sharing: shares sum to the secret.
        Shares can be negative integers. The function returns a list of length
        n_shares where the i-th element is the share intended for server i.
        """
        if n_shares < 1:
            raise ValueError("n_shares must be >= 1")

        secret = self.calculate_speed(car)
        shares: list[int] = []
        for _ in range(max(0, n_shares - 1)):
            shares.append(random.randint(-1000, 1000)) 
        last = secret - sum(shares) 
        shares.append(last) 
        return shares


class Game:
    def __init__(self, n_players: int, n_servers: int):
        self.servers = [Server(i) for i in range(n_servers)]
        self.players = [Player(i) for i in range(n_players)]
        self.god = God()

    def setup(self):
        pass

    def run(self):
        while True:
            for player in self.players:
                # do something
                pass


if __name__ == '__main__':
    n_players = 3
    n_servers = 5
    game = Game(n_players, n_servers)
    game.run()

