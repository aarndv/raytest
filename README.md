# Ray Test

A tiny 2D ray-casting playground made with Python and Pygame. Move a colored
light around the scene and watch its rays stop at randomly scattered circles.
It started as a hands-on experiment with geometry, trigonometry, and making
something move on screen.

> **Made before AI.** This little project is handmade, pushed through with
> will and interest, one curious experiment at a time.

## Run it

You’ll need Python 3 and Pygame. From the project directory:

```bash
python -m pip install pygame
python ray.py
```

## Controls

| Input | What it does |
| --- | --- |
| Move the mouse | Steer the light source |
| Left click | Scatter a fresh set of circles |
| Mouse wheel up/down | Add or remove five rays |
| Space | Cycle through ray colors |
| Close the window | Quit |

The scene is drawn at 640 × 480 and scaled up to a 1280 × 960 window. Rays are
evenly spaced around the light; each ends at the nearest circle it hits, or at
the edge of the scene.

## Project layout

```text
ray.py              Pygame window, input, and main loop
scripts/entities.py Circles, light source, and ray geometry
```

## A note on the math

Each ray is represented by an origin and a direction. For every obstacle,
the program solves the ray-circle quadratic and keeps the nearest positive
intersection. If a ray misses every circle, it is extended to the scene edge.
