# TicTacToe by Markimark aka GiorDior aka Giorgio

import pygame, time, random, math, sys
# creates the window
from data.scripts.RootClass import Root
# lets the program wait while still updating the program (not like in time.sleep)
from data.scripts.TimeWaitClass import Wait
# button system used in the menu
from data.scripts.ButtonClass import Button
# sound system to play a sound
from data.scripts.SoundClass import Sound
from data.scripts.RenderClass import Render
# includes the necessary functionalities of the computer 
from data.scripts.ComputerClass import Computer

# handles events like:
#   quit
#   user presses escape 
#   user clicks the mouse
class Events:
    # checking whether events occur which are necessary for the menu
    def handle_menu(buttons) -> None:
        for event in pygame.event.get():
            # checking if user quits the app
            Events.on_quit(event)
            # checking if user presses the mouse in case the user 
            # presses a button
            if Events.get_click(event, 1):
                for button in buttons:
                    # checks if mouse collides with the button
                    if button.get_hover():
                        # play a sound for animation
                        Sound.play("data/sounds/sound_click.wav")
                        # executes the corresponding command (starts te game)
                        button.command()

     # checking whether events occur which are necessary for the game
    def handle(game) -> None:
        # global access to the variables in order to stop the game 
        # in case of an event and to start the menu again
        global menu_running, pvp_running, pvc_running
        for event in pygame.event.get():
            # checking if user quits the app
            Events.on_quit(event)
            if Events.get_click(event, 1):
                # save the position of the mouse position for x and y (0 <= x <= 2; 0 <= y <= 2)
                # Since the distance from the edge to the board is 150 pixels, these must be subtracted from the original mouse position.
                # A square has the size of 200 pixels, so the position of the mouse is divided by 200.
                position_x = int((pygame.mouse.get_pos()[0] - 150)/200)
                position_y = int((pygame.mouse.get_pos()[1] - 150)/200)

                # checking if the player really clicks on the board
                # if the player click on the left or top side of the screen, the result for the x and y positions would be still 0 
                if pygame.mouse.get_pos()[0] > 150 and pygame.mouse.get_pos()[1] > 150 and\
                    -1 < position_x < 3 and -1 < position_y < 3:
                    # checking if the square the player clicks is empty
                    if game.board[position_x + position_y * 3] == 0:
                        # play sound for animation
                        Sound.play("data/sounds/sound_place.wav")
                        # making the move the player did
                        game.board = Game.make_move(game.board, (position_x, position_y), game.turn)
                        # checking if current gamemode is pvp to change the turn to the other player
                        if game.type == "pvp":
                            game.turn = game.turn % 2 + 1
                        else:
                            # if not, the computer makes a move
                            # in case that the player just ended the game, we must check if the game still runs
                            if not Game.is_over(game.board):
                                # 9 stands for the depth the computer looks ahead (9 moves ahead)
                                game.board = Computer.make_move(game.board, 9)
                    else:
                        # play a different sound if the square is occupied
                        Sound.play("data/sounds/sound_place_error.wav")

            # checking if player clicks escape to return back to the menu
            if Events.get_escape(event):
                game.running = False
                Commands.on_escape_click()

    # checking if the player closes the game
    def on_quit(event) -> None:
        if event.type == pygame.QUIT:
            sys.exit()

    # checksing if the player presses escape
    def get_escape(event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return False

    # checks, if the player clicked the mouse
    def get_click(event, mouse_button: int) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == mouse_button:
                return True
        return False

# class which contains function which are called 
# on a button click
class Commands:
    # starting game (pvp)
    def on_button_click_pvp() -> None:
        global menu_running, pvp_running
        menu_running = False
        pvp_running = True

    # starting game (pvc)
    def on_button_click_pvc() -> None:
        global menu_running, pvc_running
        menu_running = False
        pvc_running = True

    # returning to the menu
    def on_escape_click() -> None:
        global menu_running, pvp_running, pvc_running
        menu_running = True
        pvp_running = False
        pvc_running = False

# runs the game and handles all game related functions
class Game:
    def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock, fps: int, type: str) -> None:
        # creating an empty board
        self.board = [
            0, 0, 0,
            0, 0, 0,
            0, 0, 0,
        ]
        # saving if the game is pvp or pvc
        self.type = type
        # render surface
        self.surface = surface
        self.clock = clock
        self.fps = fps
        # game score
        self.score = [0, 0]
        
        # randomly decide who starts
        self.turn = random.randint(1, 2)
        # a variable, to keep track track who started firstly
        self.start_turn = self.turn

        # computer does a move in case its his turn and the game is pvc
        if self.type == "pvc" and self.turn == 2:
            self.board[random.randint(0, 8)] = 2
            self.turn = 1

    # run game
    def run(self) -> None:

        self.running = True
        while self.running:
            # checking game related events 
            Events.handle(self)

            Render.background(self.surface)
            # rendering the score on the top and the current turn in the bottom left edge
            Game.render_stats(self.surface, self.score, self.turn)
            Game.render_board(self.surface, self.board)
            # renders the semi-transparent square on the board
            Game.on_hover_render_animation(self.surface, self.board)

            # update screen
            Root.update(self.clock, self.fps)

            if Game.is_over(self.board):
                # add score to player 1
                if Game.has_won(self.board, 1):
                    self.score[0] += 1
                    Game.winning_animation(self.board, 1)

                # add score to player 2
                elif Game.has_won(self.board, 2):
                    self.score[1] += 1
                    Game.winning_animation(self.board, 2)

                # render the pattern which won the game and delete all other squares
                Render.background(self.surface)
                Game.render_stats(self.surface, self.score, self.turn)
                Game.render_board(self.surface, self.board)
                Root.update(self.clock, self.fps)
                time.sleep(1)

                # reset board
                self.board = [0 for i in range(9)]
                # changes the player who starts the game
                self.start_turn = self.start_turn % 2 + 1
                self.turn = self.start_turn
                
                # computer does a move in case its his turn and the game is pvc
                if self.type == "pvc" and self.turn == 2:
                    self.board[random.randint(0, 8)] = 2
                    self.turn = 1

                # clear all events which could occur during the winning animation to prevent
                # clicks on the board which were not meant
                pygame.event.clear()
    
    def winning_animation(board: list, player_index: int) -> list:
        # reset all squares except for the winning pattern
        for pattern in Game.get_winning_patterns():
            # checking all possible winning patterns and if the squares are all equal and not empty
            if (board[pattern[0]] == board[pattern[1]] == board[pattern[2]] and board[pattern[0]] == player_index):
                for index in range(len(board)):
                    if not index in pattern:
                        board[index] = 0
        return board

    # rendering the score on the top and the current turn in the bottom left edge
    def render_stats(surface: pygame.Surface, scores: tuple, turn: int) -> None:
        font = pygame.font.Font("data/fonts/pixel.ttf", 90)
        Render.text(surface, font, str(scores[0])+" : "+str(scores[1]), (900/2, 70))
        
        font = pygame.font.Font("data/fonts/pixel.ttf", 75)
        if turn == 1:
            Render.text(surface, font, "turn: X", (145, 850))
        else:
            Render.text(surface, font, "turn: O", (145, 850))

    def render_board(surface: pygame.Surface, board: list) -> None:
        Render.image(surface, (150, 150), "data/images/image_board.png")
        for x in range(3):
            for y in range(3):
                # 3 stands for the x range
                if board[x + y * 3] == 1:
                    Render.image(surface, (x * 200 + 150, y * 200 + 150), "data/images/image_cross.png")
                if board[x + y * 3] == 2:
                    Render.image(surface, (x * 200 + 150, y * 200 + 150), "data/images/image_circle.png")
        
    def on_hover_render_animation(surface: pygame.Surface, board: list) -> None:
        # save the position of the mouse position for x and y (0 <= x <= 2; 0 <= y <= 2)
        # Since the distance from the edge to the board is 150 pixels, these must be subtracted from the original mouse position.
        # A square has the size of 200 pixels, so the position of the mouse is divided by 200.
        position_x = int((pygame.mouse.get_pos()[0] - 150)/200)
        position_y = int((pygame.mouse.get_pos()[1] - 150)/200)
        if pygame.mouse.get_pos()[0] > 150 and pygame.mouse.get_pos()[1] > 150 and\
            -1 < position_x < 3 and -1 < position_y < 3:
            # checking if the square is empty
            if board[position_x + position_y * 3] == 0:
                transparent_surface = pygame.Surface((200, 200))
                transparent_surface.set_alpha(50)
                surface.blit(transparent_surface, (position_x * 200 + 150, position_y * 200 + 150))
    
    # all possible winning patterns
    def get_winning_patterns() -> list:
        patterns = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]
        return patterns

    def has_won(board: list, player_index: int) -> bool:
        patterns = Game.get_winning_patterns()
        for pattern in patterns:
            # checking all possible winning patterns and if the squares are all equal and not empty
            if (board[pattern[0]] == board[pattern[1]] == board[pattern[2]] and board[pattern[0]] == player_index):
                return True
        return False
    
    def is_over(board):
        # checking if one player one the game
        if Game.has_won(board, 1) or Game.has_won(board, 2):
            return True
        
        # checking if no square is empty
        for square in board:
            if square == 0:
                return False
        return True

    # return 10, if player 1 won (x) and return -10, if player 2 won (o), else return 0
    # serves for the precalculation for the computer
    def evaluate(board: list) -> int:
        "evaluates a position, returns the value"
        patterns = Game.get_winning_patterns()
        for pattern in patterns:
            # checking all possible winning patterns and if the squares are all equal and not empty
            if (board[pattern[0]] == board[pattern[1]] == board[pattern[2]]\
                and board[pattern[0]] != 0):
                # checking if the player is player 1 or 2
                if board[pattern[0]] == 1:
                    return 10
                elif board[pattern[0]] == 2:
                    return -10
        return 0

    # making a move on the board
    def make_move(board: list, position: tuple[int], player_index: int) -> list:
        move = position[0] + position[1] * 3
        board[move] = player_index
        return board

# contains all functions related to the menu
class Menu:
    # starting screen which shows "Markimark"
    def start_screen(surface: pygame.display.set_mode, clock: pygame.time.Clock, fps: int):
        Render.image(surface, (0, 0), "data/images/image_starting_screen.png")
        Sound.play("data/sounds/sound_wooden_click.wav")
        Wait.seconds(1.5, clock, fps)

    def run(surface: pygame.Surface, clock: pygame.time.Clock, fps: int):
        global menu_running
        if menu_running:
            # play a sound when the user enters the menu
            Sound.play("data/sounds/sound_wooden_click.wav")
            # logo on the top
            logo = Menu.logo()
            # storing both buttons in this array
            buttons = [
                Button(["data/images/image_button_pvp.png", "data/images/image_button_pvp_animation.png"], 
                (900/2, 500), Commands.on_button_click_pvp),
                Button(["data/images/image_button_pvc.png", "data/images/image_button_pvc_animation.png"], 
                (900/2, 700), Commands.on_button_click_pvc)]

        while menu_running:
            # checking menu related events
            Events.handle_menu(buttons)

            Render.background(surface)
            # logo goes up and down
            logo.animate(surface)
            # draw buttons to the screen
            for button in buttons:
                button.update()
                button.render(surface)
            
            # update screen
            Root.update(clock, fps)

    # class which animates the main (TicTacToe) logo
    # 
    # a class is necessary for the animation
    # as we have to keep track of a variable in a function
    # which is called different times
    class logo:
        def __init__(self) -> None:
            self.position_y = 100
            # keeps track of the current direction the logo is going
            self.animation_state = 0
            self.file = "data/images/image_tictactoe_logo.png"
            self.tick = time.perf_counter()
            # logo movement speed
            self.speed = 3

        def animate(self, surface: pygame.Surface):
            # changes the direction
            # if the logo reaches a certain position
            if self.position_y > 125:
                self.animation_state = 1

            elif self.position_y < 100:
                self.animation_state = 0

            # move logo only every 0.1 seconds
            if time.perf_counter() - self.tick > 0.1:
                self.tick = time.perf_counter()
                if self.animation_state == 0:
                    self.position_y += self.speed
                else:
                    self.position_y -= self.speed

            Render.image(surface, (125.5, self.position_y), self.file)
            
def main() -> None:
    global menu_running, pvp_running, pvc_running
    # initialization
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    # creating the window
    root = Root.init((900, 900), "TicTacToe")
    clock = pygame.time.Clock()
    fps = 60

    # keeping track which section of the game is running
    menu_running = True
    pvp_running = False
    pvc_running = False

    # starting the introduction/start screen
    Menu.start_screen(root, clock, fps)

    while True:
        Menu.run(root, clock, fps)
        
        # running game
        if pvp_running or pvc_running:
            if pvp_running:
                game = Game(root, clock, fps, "pvp")
            else:
                game = Game(root, clock, fps, "pvc")
            game.run()
        
if __name__ == "__main__":
    main()