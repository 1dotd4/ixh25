"""
Simple simulation of a blockchain where races are held between players.
Servers act as validators: after each race servers validate the winner.
If a majority of servers agree, the winner creates (proposes) a block that
is appended to the chain and the winner receives 100 tokens as reward.
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Block:
    index: int
    previous_hash: str
    proposer: int  # player id who proposed (the winner)
    winner_id: int
    speeds: dict[int, int]
    validators: List[int]
    reward: int = 100
    hash: Optional[str] = field(default=None)

    def compute_hash(self) -> str:
        payload = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "proposer": self.proposer,
            "winner_id": self.winner_id,
            "speeds": self.speeds,
            "validators": self.validators,
            "reward": self.reward,
        }
        s = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(s.encode()).hexdigest()


class Racechain:
    def __init__(self):
        self.chain: List[Block] = []

    def last_hash(self) -> str:
        if not self.chain:
            return "0" * 64
        return self.chain[-1].hash or self.chain[-1].compute_hash()

    def add_block(self, block: Block) -> bool:
        # previous hash match 
        if block.previous_hash != self.last_hash():
            return False
        # at least one validator
        if not block.validators:
            return False
        block.hash = block.compute_hash()
        self.chain.append(block)
        return True
