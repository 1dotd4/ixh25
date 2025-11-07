# IXH25

- Submission 12:00 November 8.
- [Submission form](https://hackathons.xrpl-commons.org/)

## Cryptographic track

### Assumptions
- A *car* is a list of 10 *flags*: `t0,...,t9`
  - Each *flag* has a range `0 <= ti <= 1000`
- The *flags* are *secret* and *random*.
  - *unknown* even to the car's owner
- The speed of a car is given by a *secret* formula (which we'll call the *speed*)
- At the start of the game, each user has a car and 10 tokens XPF
- A user can train its car (cost: 1XPF), by changing randomly its *flags* (plus/minus <20 each) and testing the *speed* of the new car's version
- When __a race is created by the game__, all users can participate with one of their car (cost: 1XPF)
- *The fastest car wins 100XPF*

*Players wants to win*
They shall not see:
- their *flags* (or others' *flags*)
- the *speed* formula

They shall not modify their *flags*

*Can we trust the server?*
The server shall not __see or modify__:
- the *speed* (function)
- the users' *flags*

The server must run the race *fairly*

To *design* and *implement* a cryptographic protocol
that allows the secure running of F1-AI.

The protocol mus use some blockchain technology.
