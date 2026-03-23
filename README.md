# space-orbiter
a cool little 2D planet-orbiting simulator/game in Python 3.8

Guide a spacecraft into stable orbit around celestial bodies by managing thrust, fuel, and gravitational forces.

This is a personal side project and work in progress — not a shipped or finished game. It is the prototype and physics proof-of-concept for a larger project, currently in early planning.

## What it is

space-orbiter simulates Newtonian gravity, atmospheric drag, and real orbital mechanics concepts. The goal is to maneuver your ship into a stable orbit within a target zone around a planet — not too close, not too far.

Orbit quality is measured by eccentricity. A near-circular orbit within the goldilocks zone scores highest. The scoring formula rewards precision: the closer to zero eccentricity, the higher your score.

## Features

- Newtonian gravity with sphere of influence
- Atmospheric drag with layered density model
- Prograde and retrograde burns
- Periapsis, apoapsis, and eccentricity tracking
- Fuel system with fine and coarse thrust control
- Thrust plume animation
- Orbital trail rendering
- Time warp controls

## Controls

| Key | Action |
|-----|--------|
| W / A / S / D | Directional thrust |
| E | Prograde burn |
| R | Retrograde burn |
| Shift | Fine thrust modifier |
| T | Kill velocity (when near zero) |
| +/- | Time warp |
| Q | Quit |

## Running it
```bash
pip install pygame
python main.py
```

## Architecture

Physics engine built around an inheritance hierarchy:
```
Body
├── Gravitative  (mass, gravity)
│   ├── Planet
│   └── Mobile   (velocity, kinematics)
│       ├── Satellite
│       └── Ship  (thrust, fuel, drag, animation)
└── Atmosphere   (drag layers)
```

## Status

Active side project. Currently a single-system sandbox. This codebase may be ported or reimplemented in Godot/GDScript as development toward a fuller game continues.