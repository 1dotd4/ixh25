import random
from god import God
from player import Player
from racechain import Racechain, Block
from gameserver import GameServer
class Race:
    def __init__(self, n_players: int, n_servers: int):
        self.players = {i: Player(i) for i in range(n_players)}
        self.servers = [GameServer(i) for i in range(n_servers)]
        self.god = God()
        self.chain = Racechain()

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

    def run(self) -> None:
        # 1) Each player sends a training vector (local computation)
        training_vectors: dict[int, list[int]] = {}
        for pid, player in self.players.items():
            car = player.car
            print(f"Player {player.id} Car {car.id}")
            # create flags exist for the car
            self.god.create_flags(car)
            print(f"Created flags: {self.god.flags[car.id]}")
            # calculate speed (for logging/consistency)
            speed = self.god.calculate_speed(car)
            print(f"Calculated speed: {speed}")
            # create and distribute shares to servers using the training vector
            self.god.create_shares(car.id, self.servers)
            print(f"Shares created and sent to servers for car {car.id}.")
            # training probability
            if random.random() < 0.5:
                training_vectors[pid] = player.training_vector()
                self.god.update_flags(car, training_vectors[pid])
                self.god.create_shares(car.id, self.servers)

        # 3) Players reconstruct speeds by summing shares from servers
        speeds: dict[int, int] = {}
        for pid, player in self.players.items():
            reconstructed = player.reconstruct_speed(player.car.id, self.servers)
            speeds[pid] = reconstructed
            print(f"Player {pid} original speed: {self.god.flags[player.car.id] and self.god.calculate_speed(player.car)}; Reconstructed: {reconstructed}")

        # 4) determine winner from reconstructed speeds
        winner_id = max(speeds.items(), key=lambda kv: kv[1])[0]

        # 5) servers validate the declared winner
        validators: list[int] = []
        for server in self.servers:
            if server.validate_winner(winner_id, speeds):
                validators.append(server.id)

        # require majority
        majority = len(self.servers) // 2 + 1
        if len(validators) < majority:
            print(f"Race result rejected: only {len(validators)} validators (<{majority}) agreed")
            return

        # 6) winner proposes a block and receives reward
        index = len(self.chain.chain)
        previous_hash = self.chain.last_hash()
        block = Block(
            index=index,
            previous_hash=previous_hash,
            proposer=winner_id,
            winner_id=winner_id,
            speeds=speeds,
            validators=validators,
            reward=100,
        )

        ok = self.chain.add_block(block)
        if not ok:
            print("Failed to add block to chain (validation failed)")
            return

        # award tokens to winner
        self.players[winner_id].token += block.reward
        print(f"Block {block.index} added by player {winner_id}. Validators: {validators}. Rewarded {block.reward} tokens.")

    def simulate(self, n_rounds: int = 5) -> None:
        for r in range(n_rounds):
            print(f"\n-- Race {r} --")
            self.run()
        print("\nFinal balances:")
        for pid, p in self.players.items():
            # Player uses attribute `token` in Player class
            print(f"Player {pid}: {p.token} tokens")


if __name__ == '__main__':
    sim = Race(n_players=3, n_servers=5)
    sim.simulate(10)
