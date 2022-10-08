import pygame, time

class Wait:
    # delaying the program in a while loop for a certain amount of seconds
    def seconds(seconds: float, clock: pygame.time.Clock, fps: int) -> None:
        from main import Events
        from data.scripts.RootClass import Root

        start_tick = time.perf_counter()

        while time.perf_counter() - start_tick < seconds:
            for event in pygame.event.get():
                Events.on_quit(event)

            Root.update(clock, fps)