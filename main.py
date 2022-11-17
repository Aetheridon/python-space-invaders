"""Space Invaders!"""

import math
import random

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Space Invaders"
CHARACTER_SCALING = 1
SCALE = 0.5
MOVEMENT_SPEED = 5
BULLET_SPEED = 10


class Bullet(arcade.Sprite):
    """Generic class for bullets"""

    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))


class Star:
    """Generic class for the star sprites"""

    def __init__(self):
        self.x = 0  # pylint: disable=C0103
        self.y = 0  # pylint: disable=C0103
        self.size = 0
        self.speed = 0

    def reset_pos(self):
        """reset the position of the star"""
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)


class Player(arcade.Sprite):
    """Generic class for the player"""

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
    """A class to manage and control our game"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BLACK)

        self.frame_count = 0

        self.enemy_list = None  # List for enemy ships
        self.star_list = None  # List for stars
        self.player_list = None  # Player sprite is appended to this list
        self.player_sprite = None  # Player sprite
        self.enemy_sprite = None  # Enemy sprite
        self.bullet_list = None  # Bullet sprites

    def render_stars(self):
        """renders our star sprite"""
        self.star_list = []

        for _ in range(50):
            star = Star()

            star.x = random.randrange(SCREEN_WIDTH)
            star.y = random.randrange(SCREEN_HEIGHT + 200)

            star.size = random.randrange(4)
            star.speed = random.randrange(20, 40)

            self.star_list.append(star)

        self.set_mouse_visible(False)

    def setup(self):
        """the initialisation function for starting a new game"""
        self.bullet_list = arcade.SpriteList()

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
        self.bullet_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.frame_count += 1

        for star in self.star_list:
            star.y -= star.speed * delta_time

            if star.y < 0:
                star.reset_pos()

        for enemy in self.enemy_list:
            start_x = enemy.center_x
            start_y = enemy.center_y

            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            enemy.angle = math.degrees(angle) - 90

            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.angle = math.degrees(angle)

                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()

    def handle_shoot(self):
        """Handle the actions for user shooting event"""
        bullet_sprite = Bullet(":resources:images/space_shooter/laserBlue01.png")
        bullet_sprite.guid = "Bullet"
        bullet_sprite.change_y = math.cos(math.radians(self.player_sprite.angle)) * BULLET_SPEED
        bullet_sprite.change_y = math.cos(math.radians(self.player_sprite.angle)) * BULLET_SPEED
        bullet_sprite.center_x = self.player_sprite.center_x
        bullet_sprite.center_y = self.player_sprite.center_y
        bullet_sprite.update()
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
        self.bullet_list.append(bullet_sprite)

    def handle_user_movement(self, symbol):
        """Handle the action for user movement"""
        if symbol == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif symbol == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_press(self, symbol, modifiers):
        """generic event handler for key press"""
        if symbol == arcade.key.SPACE:
            self.handle_shoot()

        if symbol in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.handle_user_movement(symbol)

    def on_key_release(self, symbol, modifiers):
        """generic event handler for key release"""
        if symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """main function where the magic happens"""
    window = SpaceInvader()
    window.setup()
    window.render_stars()
    arcade.run()


if __name__ == "__main__":
    main()
