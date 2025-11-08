import random
from typing import Optional

N_PLAYERS = 3
N_SERVERS = 5

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

    def get_shares(self, car_id: int) -> list[int]:
        return self.shares.get(car_id)
    
    def validate_winner(self, winner_id: int, speeds: dict[int, int]) -> bool:
        """Simulate validation of the winner using the reported speeds.

        In a real system servers would check signatures and inputs. Here we
        simulate a mostly-honest validator with a small chance to disagree
        (simulating faults or disagreements).
        """
        computed_winner = max(speeds.items(), key=lambda kv: kv[1])[0]
        honest = computed_winner == winner_id
        # small chance of random faulty validator (~5%)
        if not honest and random.random() < 0.05:
            # rare: faulty but accidentally agrees
            return True
        if honest and random.random() < 0.05:
            # rare: honest but flips
            return False
        return honest

class God:
    def __init__(self):
        self.flags: dict[int, list[int]] = {}
        self.coeff = [random.randint(0, 21) for _ in range(10)]

    def create_flags(self, car: Car) -> list[int]:
        flags = [random.randint(0, 1000) for _ in range(10)]
        self.flags[car.id] = flags
        return flags

    def create_shares(self, car_id: int, server_list: list[Server]) -> None:
        shares = []
        for f,c in zip(self.flags[car_id], self.coeff):
            s = c * (f % 1001)
            shares.append(self.secret_sharing(s, N_SERVERS))
        for i in range(N_SERVERS):
            vec = [shares[j][i] for j in range(len(shares))]
            server_list[i].receive_shares(car_id, vec)
        return 

    def calculate_speed(self, car: Car) -> int:
        flags = self.flags.get(car.id)
        if flags is None:
            flags = self.create_flags(car)
        speed = sum(f * c for f, c in zip(flags, self.coeff))
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


class Game:
    def __init__(self, n_players: int, n_servers: int):
        self.servers = [Server(i) for i in range(n_servers)]
        self.players = [Player(i) for i in range(n_players)]
        self.god = God()

    def demo(self, player_index: int = 0) -> None:
        """Demo: create flags, compute speed, secret-share across servers and verify reconstruction."""
        player = self.players[player_index]
        car = player.car
        print(f"Player {player.id} Car {car.id}")
        self.god.create_flags(car)
        print(f"Created flags: {self.god.flags[car.id]}")
        speed = self.god.calculate_speed(car)
        print(f"Calculated speed: {speed}")
        self.god.create_shares(car.id, self.servers)
        print(f"Shares created and sent to servers.")
        reconstructed = player.reconstruct_speed(car.id, self.servers)
        print(f"Original speed: {speed}, Reconstructed: {reconstructed}")
        assert reconstructed == speed, "Reconstructed speed does not match original"

    def run(self):
        while True:
            for player in self.players:
                self.demo(player.id)


if __name__ == '__main__':
    game = Game(N_PLAYERS, N_SERVERS)
    game.run()

