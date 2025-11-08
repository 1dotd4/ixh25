import random
from player import Player

class GameServer:
    def __init__(self, id: int):
        self.id = id
        self.shares: dict[int, list[int]] = {}

    def handle_training_request(self, user: Player, training_vector: list) -> bool:
        if user.token < 1:
            # raise ValueError("Not enough tokens.")
            return False
        else:
            if self.receive_payment():
                user.token -= 1
                return True
        
    def receive_payment(self, player: Player) -> bool:
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
        # small chance of random faulty validator (~1%)
        if not honest and random.random() < 0.01:
            # rare: faulty but accidentally agrees
            return True
        if honest and random.random() < 0.01:
            # rare: honest but flips
            return False
        return honest