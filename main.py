import random

import arcade 

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Space Invaders"
CHARACTER_SCALING = 1
MOVEMENT_SPEED = 5

class Star:
    def __init__(self):
        self.x = 0
        self.y = 0

class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1        

class SpaceInvader(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BLACK)

        self.enemy_list = None # List for enemy ships
        self.star_list = None # List for stars
        self.player_list = None # Player sprite is appended to this list
        self.player_sprite = None # Player sprite
        self.enemy_sprite = None # Enemy sprite

    def render_star(self):
        self.star_list = []

        for i in range(50):
            star = Star()

            star.x = random.randrange(SCREEN_WIDTH)
            star.y = random.randrange(SCREEN_HEIGHT + 200)

            star.size = random.randrange(4)

            self.star_list.append(star)

        self.set_mouse_visible(False)

    def setup(self):
        ###### PLAYER SPRITE ######
        self.player_list = arcade.SpriteList()
        player_image_source = ":resources:images/space_shooter/playerShip1_orange.png"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        ###### ENEMY SPRITE ######
        self.enemy_list = arcade.SpriteList()
        enemy_image_source = ":resources:images/space_shooter/playerShip3_orange.png"
        self.enemy_sprite = arcade.Sprite(enemy_image_source, CHARACTER_SCALING)
        self.enemy_sprite.center_x = 120
        self.enemy_sprite.center_y = SCREEN_HEIGHT - self.enemy_sprite.height
        self.enemy_sprite.angle = 200
        self.enemy_list.append(self.enemy_sprite)

    def on_draw(self):
        self.clear()

        for star in self.star_list:
            arcade.draw_circle_filled(star.x, star.y, star.size, arcade.color.WHITE)

        self.player_list.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    window = SpaceInvader()
    window.setup()
    window.render_star()
    arcade.run()

if __name__ == "__main__":
    main()
