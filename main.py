import random

import arcade 

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Space Invaders"
CHARACTER_SCALING = 1

class Star:
    def __init__(self):
        self.x = 0
        self.y = 0

class SpaceInvader(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BLACK)

        self.star_list = None
        self.player_list = None
        self.player_sprite = None

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
        self.player_list = arcade.SpriteList()

        image_source = ":resources:images/space_shooter/playerShip1_orange.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        self.clear()

        for star in self.star_list:
            arcade.draw_circle_filled(star.x, star.y, star.size, arcade.color.WHITE)

        self.player_list.draw()

def main():
    window = SpaceInvader()
    window.setup()
    window.render_star()
    arcade.run()

if __name__ == "__main__":
    main()
