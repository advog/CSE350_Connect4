import button
import pygame

#define colors
menu_color = (2,178,255)
button_color = (51,255,255)
white_color = (255, 255, 255)
pressed_button_color = (0, 90, 110)
empty_color = (1, 0, 60)
player1_color = (255, 0, 0)
player2_color = (255, 255, 0)
menu_color = (2,178,255)

#load assets
logo = pygame.image.load('logo2.png')

#useful functions
def check_clicked(button_list, pos):
    for i in range(len(button_list)):
        if button_list[i].check_clicked(pos):
            return i
    return -1

def click_anywhere():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

###############
#gameboard gui#
###############

class game_gui:
    # args: pygame.surface display_surface, int width, int height
    def __init__(self, display_surface, width, height):

        # initialize game_surface
        self.game_surface = pygame.Surface((width, height))
        self.display_surface = display_surface
        self.width = width
        self.height = height
        self.block_width = width/7
        self.block_height = height/7

        # add buttons to game_surface
        self.column_buttons = []
        for i in range(7):
            tmp_button = button.invisible_button((self.block_width * i, self.block_height), (self.block_width, self.block_width*6))
            self.column_buttons.append(tmp_button)

        # add textbox to game_surface (it is technically a click button but we just will never check if it is clicked)
        self.game_textbox = button.click_button((0, 0), (self.width, self.block_width), menu_color, "Textbox", self.game_surface)

    #draw methods
    def draw_board(self, board):
        circle_size = min(self.block_width,self.block_height) * 0.4

        for x in range(7):
            for y in range(6):
                #draw grid
                rect_offset = (x * self.block_width, (y+1) * self.block_height)
                rect = pygame.Rect(rect_offset, (self.block_width, self.block_height))
                pygame.draw.rect(self.game_surface, (255, 255, 255), rect, 1)

                #draw circles over grid
                color = empty_color
                if (board[x][y] == 1):
                    color = player1_color
                elif (board[x][y] == 2):
                    color = player2_color
                circ_offset = (int((x+.5) * self.block_width), int((y + 1.5) * self.block_height))
                pygame.draw.circle(self.game_surface, color, circ_offset, int(circle_size))

    def draw_text(self, text):
        self.game_textbox.text = text
        self.game_textbox.draw()

    def update_display(self):
        self.display_surface.blit(self.game_surface, (0, 0))
        pygame.display.flip()

    # loops until player returns move
    # returns: int indicating column chosen by player
    def request_move_player(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked_index = check_clicked(self.column_buttons, pos)
                    if clicked_index != -1:
                        return clicked_index

                # event.key 49-55 map to the number keys 1-7
                if event.type == pygame.KEYDOWN:
                    if 49 <= event.key <= 55:
                        return event.key - 49

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

##########
#menu gui#
##########

class menu_gui:
    # args: pygame.surface display_surface, int width, int height
    def __init__(self, display_surface, width, height):
        self.width = width
        self.height = height
        self.display_surface = display_surface

        #init the surface
        self.menu_surface = pygame.Surface((self.width, self.height))
        self.menu_surface.fill(menu_color)
        self.menu_surface.blit(logo, (0, 0))

        # add buttons to menu_surface
        self.menu_buttons = []
        lpvp_button = button.click_button((self.width / 2 - 130, self.height*(5/7)), (120, 50), button_color, "Local PvP", self.menu_surface)
        self.menu_buttons.append(lpvp_button)
        opvp_button = button.click_button((self.width / 2 + 10, self.height*(5/7)), (120, 50), button_color, "Online PvP", self.menu_surface)
        self.menu_buttons.append(opvp_button)
        aivp_button = button.click_button((self.width / 2 - 130, self.height*(5/7)+ 60), (120, 50), button_color, "PvAI", self.menu_surface)
        self.menu_buttons.append(aivp_button)
        aivai_button = button.click_button((self.width / 2 + 10, self.height*(5/7)+ 60), (120, 50), button_color, "AIvAI", self.menu_surface)
        self.menu_buttons.append(aivai_button)
        rewatch_button = button.click_button((self.width / 2 - 60, self.height*(5/7)+ 120), (120, 50), button_color, "Rewatch", self.menu_surface)
        self.menu_buttons.append(rewatch_button)

        # map for readability
        self.menu_button_map = ["lpvp", "opvp", "aivp", "aivai", "rewatch"]

    #draws all buttons
    def draw_buttons(self):
        for b in self.menu_buttons:
            b.draw()

    #copies internal surface to the external surface
    def update_display(self):
        self.display_surface.blit(self.menu_surface, (0, 0))
        pygame.display.flip()

    # loops until the player chooses a gamemode by clicking on a button
    # returns: int indicating which button was clicked
    def request_menu_choice(self):
        self.draw_buttons()
        self.update_display()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked_index = check_clicked(self.menu_buttons, pos)
                    if clicked_index != -1:
                        return clicked_index

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

###############
#AI config gui#
###############

class ai_config_gui:
    def __init__(self, display_surface, width, height):
        self.width = width
        self.height = height
        self.display_surface = display_surface
        self.level = 3
        self.turn = 0

        #init the surface
        self.ai_config_surface = pygame.Surface((self.width, self.height))
        self.ai_config_surface.fill(menu_color)

        # add level_buttons
        self.level_buttons = []
        random_button = button.click_button((self.width / 12, self.height*(3/8)), (240, 50), button_color, "Random", self.ai_config_surface)
        self.level_buttons.append(random_button)
        easy_button = button.click_button((self.width / 12, self.height*(3/8)+ 60), (240, 50), button_color, "Easy", self.ai_config_surface)
        self.level_buttons.append(easy_button)
        hard_button = button.click_button((self.width / 12, self.height*(3/8)+ 120), (240, 50), button_color, "Hard", self.ai_config_surface)
        self.level_buttons.append(hard_button)
        impossible_button = button.click_button((self.width / 12, self.height*(3/8)+ 180), (240, 50), pressed_button_color, "Impossible", self.ai_config_surface)
        self.level_buttons.append(impossible_button)

        #add turn_buttons
        self.turn_buttons = []
        player_first_button = button.click_button((self.width / 12, self.height*(1/8)), (240, 50), pressed_button_color, "Player Goes First", self.ai_config_surface)
        self.turn_buttons.append(player_first_button)
        ai_first_button = button.click_button((self.width / 12 + 270, self.height*(1/8)), (240, 50), button_color, "AI Goes First", self.ai_config_surface)
        self.turn_buttons.append(ai_first_button)
        
        #create confirm button
        self.confirm_button = button.click_button((self.width / 12 + 270, self.height*(3/8)), (240, 230), white_color, "Confirm", self.ai_config_surface)

    def draw_buttons(self):
        for b in self.level_buttons:
            b.draw()
        for b in self.turn_buttons:
            b.draw()
        self.confirm_button.draw()

    def update_display(self):
        self.display_surface.blit(self.ai_config_surface, (0, 0))
        pygame.display.flip()

    #seeds control of program to event loop
    #returns player_turn and ai_difficulty
    def get_config(self):
        self.draw_buttons()
        self.update_display()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if self.confirm_button.check_clicked(pos) == True:
                        return (self.turn, self.level)

                    #if a level button is clicked then update GUI and member variable
                    clicked_index = check_clicked(self.level_buttons, pos)
                    if clicked_index != -1:
                        self.level_buttons[self.level].change_color(button_color)
                        self.level_buttons[clicked_index].change_color(pressed_button_color)
                        self.level = clicked_index

                    #if a turn button is clicked then ditto
                    clicked_index = check_clicked(self.turn_buttons, pos)
                    if clicked_index != -1:
                        self.turn_buttons[self.turn].change_color(button_color)
                        self.turn_buttons[clicked_index].change_color(pressed_button_color)
                        self.turn = clicked_index

                    #update display
                    self.draw_buttons()
                    self.update_display()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


####################
#network config GUI#
####################

class network_config_gui:
    def __init__(self, display_surface, width, height):
        self.width = width
        self.height = height
        self.display_surface = display_surface

        # init the display
        self.menu_surface = pygame.Surface((self.width, self.height))
        self.menu_surface.fill(menu_color)
        self.menu_surface.blit(logo, (0, 0))

        self.text_buttons = []
        connect_textbox_button = button.click_button((self.width / 2 - 250, self.height * (5 / 7)), (200, 50), button_color, "", self.menu_surface)
        self.text_buttons.append(connect_textbox_button)
        host_textbox_button = button.click_button((self.width / 2 - 250, self.height * (5 / 7) + 60), (200, 50), button_color,"", self.menu_surface)
        self.text_buttons.append(host_textbox_button)
        feedback_button = button.click_button((self.width / 2 - 250, self.height * (5 / 7) + 120), (500, 50),button_color, "Feedback", self.menu_surface)
        self.text_buttons.append(feedback_button)

        self.menu_buttons = []
        host_button = button.click_button((self.width / 2 -40, self.height * (5 / 7) + 60), (290, 50), button_color,"Generate Host Code", self.menu_surface)
        self.menu_buttons.append(host_button)
        connect_game_button = button.click_button((self.width / 2 - 40, self.height * (5 / 7)), (290, 50), button_color, "Connect to Game", self.menu_surface)
        self.menu_buttons.append(connect_game_button)

        #menu_buttons: host, connect
        #text_buttons: connect, host, feedback

    #draws components of GUI to the internal surface
    def draw_buttons(self):
        for b in self.menu_buttons:
            b.draw()
        for b in self.text_buttons:
            b.draw()

    def draw_text_host(self, text):
        self.text_buttons[1].text = text
        self.text_buttons[1].draw()

    def draw_text_feedback(self,text):
        self.text_buttons[2].text = text
        self.text_buttons[2].draw()

    #copies the internal surface to the external_surface
    def update_display(self):
        self.display_surface.blit(self.menu_surface, (0, 0))
        pygame.display.flip()

    #returns player_turn and ai_difficulty
    def get_config(self):
        code = ""
        self.text_buttons[0].text = code
        self.text_buttons[1].text = ""
        self.text_buttons[2].text = ""
        code_entered = False
        self.draw_buttons()
        self.update_display()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked_index = check_clicked(self.menu_buttons, pos)
                    if clicked_index != -1:
                        if clicked_index == 0:
                            return (0, "")
                        elif clicked_index == 1 and code_entered == True:
                            return (1, code)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        code = code[:-1]
                    if 49 <= event.key <= 55 and len(code) < 6:
                        code = code + event.unicode
                    self.text_buttons[0].text = code
                    if len(code) == 6:
                        code_entered = True

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.draw_buttons()
            self.update_display()