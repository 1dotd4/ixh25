# Racechain - Racing Blockchain Simulator

A Python simulation of a blockchain-based racing game where players compete in races and earn tokens, with decentralized validation through servers.

## Overview

This project implements a blockchain system for racing competitions with the following key features:

- Players participate in races with their cars
- Speeds are calculated using secret sharing mechanisms
- Servers act as validators for race results
- Winners get blocks added to the chain and receive token rewards
- Training system to improve car performance

## Components

### Core Classes

- `Racechain`: Implements the blockchain with blocks containing race results
- `Block`: Represents a block in the chain with race data and validator signatures
- `Player`: Manages player data, cars, and token balance
- `Car`: Represents a racing car with its ID and speed
- `God`: Handles speed calculations and secret sharing mechanisms
- `GameServer`: Acts as a validator and stores speed share data

### Server Implementation

- Flask-based web server implementation
- WebSocket support for real-time updates
- User session management
- Chat functionality for players

## Key Features

### Secret Sharing System

The system uses additive secret sharing to split speed calculations across multiple servers:

1. Speed flags are created for each car
2. Training vectors can modify these flags
3. Shares are distributed across validator servers
4. Speed is reconstructed by combining shares

### Validation Process

1. Servers validate race winners independently
2. Each server checks reported speeds against calculations
3. Majority consensus required for block addition
4. Small probability of validator faults simulated (~1%)

### Token System

- Players start with 10 tokens
- Training costs 1 token
- Race winners receive 100 tokens as reward
- Tokens required for certain actions (e.g., training)

## File Structure

- `game.py`: Main race simulation logic
- `racechain.py`: Blockchain implementation
- `player.py`: Player and Car class definitions
- `god.py`: Speed calculation and secret sharing
- `gameserver.py`: Validator server implementation
- `server.py`: Web server and WebSocket handling

## Technical Details

### Speed Calculation

Speeds are calculated using:

- Random flags (1-999 range)
- Training vectors (binary)
- Coefficient system
- Modular arithmetic for updates

### Block Structure

Each block contains:

- Race winner ID
- Proposer ID
- Speed data
- Validator signatures
- Previous block hash
- Block reward information

## Requirements

```pip
bidict==0.23.1
blinker==1.9.0
click==8.3.0
Flask==3.1.2
Flask-SocketIO==5.5.1
h11==0.16.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
python-dotenv==1.2.1
python-engineio==4.12.3
python-socketio==5.14.3
simple-websocket==1.1.0
Werkzeug==3.1.3
wsproto==1.2.0
```

## Setup and Usage

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python server.py`
4. Start a race simulation: `python game.py`

## Security Considerations

- Secret sharing prevents speed data manipulation
- Validator consensus required for block addition
- Token system prevents abuse of training
- Fault tolerance in validation system
