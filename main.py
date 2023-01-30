"""Space Invaders!"""

import random
import math
import time

import arcade

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Space Invaders"
CHARACTER_SCALING = 1
SCALE = 0.5
MOVEMENT_SPEED = 6.5
BULLET_SPEED = 15
enemy_list = arcade.SpriteList()
enemy_objects = []
boss_list = arcade.SpriteList()
boss_objects = []

class Player_Bullets(arcade.Sprite):
    """ class for player bullets"""
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

class Enemy_Bullets(arcade.Sprite):
    """class for enemy bullets"""
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

class Enemy_Bullets(arcade.Sprite):
    """class for enemy bullets"""
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
    def __init__(self):
        self.player_health = 100

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

class Enemy(arcade.Sprite):
    def __init__(self, x_position):
        self.enemy_health = 100
        self.stuck = False
        enemy_image_source = "sprites\enemy-sprite.png"
        self.enemy_sprite = arcade.Sprite(enemy_image_source, CHARACTER_SCALING)
        self.enemy_sprite.center_x = x_position 
        self.enemy_sprite.center_y = SCREEN_HEIGHT - self.enemy_sprite.height 
        enemy_list.append(self.enemy_sprite)

class Boss(arcade.Sprite):
    def __init__(self, x_position):
        self.boss_health = 150
        self.stuck = False
        boss_image_source = "sprites\\boss-sprite-3.png"
        self.boss_sprite = arcade.Sprite(boss_image_source, CHARACTER_SCALING)
        self.boss_sprite.center_x = x_position
        self.boss_sprite.center_y = SCREEN_HEIGHT - self.boss_sprite.height
        boss_list.append(self.boss_sprite)

class SpaceInvader(arcade.Window):
    """A class to manage and control our game"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.frame_count = 0
        self.enemy_list = None  # List for enemy ships
        self.boss_list = None # List for boss ships
        self.star_list = None  # List for stars
        self.player_list = None  # Player sprite is appended to this list
        self.player_sprite = None  # Player sprite
        self.enemy_sprite = None  # Enemy sprite
        self.boss_sprite = None # Boss sprite
        self.player_bullet_list = None  # Bullet sprites for player
        self.enemy_bullet_list = None # Bullet sprites for enemy
        self.boss_bullet_list = None # Bullet sprites for boss
        self.player_shoot_delta = 0.5
        self.player_last_shoot_time = 0
        self.player_bullet_damage = 10
        self.enemy_bullet_damage = 2
        self.boss_bullet_damage = 20
        self.stuck = False
        self.level = 1
        self.wave = 1
        self.boss_spawned = False
        self.enemy_dodge_skill = 50
        self.boss_dodge_skill = 175

    def render_stars(self):
        """renders our star sprite"""
        self.star_list = []
        for _ in range(50):
            star = Star()
            star.x = random.randrange(SCREEN_WIDTH)
            star.y = random.randrange(SCREEN_HEIGHT + 200)
            star.size = random.randrange(4)
            star.speed = random.randrange(30, 50)
            self.star_list.append(star)
        self.set_mouse_visible(False)

    def setup(self):
        """the initialisation function for starting a new game"""
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        ###### PLAYER SPRITE ######
        self.player_list = arcade.SpriteList()
        player_image_source = "sprites\player-sprite.png"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 100
        self.player_sprite.angle = 180
        self.player_list.append(self.player_sprite)
        self.player = Player()
        
        self.enemy = Enemy(x_position=random.randint(0, SCREEN_WIDTH))
        self.enemy2 = Enemy(x_position=random.randint(0, SCREEN_WIDTH))

        enemy_objects.append(self.enemy)
        enemy_objects.append(self.enemy2)

    def enemy_health_bar(self):
        health_bar_width = 200
        for enemy in enemy_objects:
            if enemy.enemy_health > 0:
                bar_x, bar_y = enemy.enemy_sprite.center_x, SCREEN_HEIGHT - 20
                arcade.draw_text(f"Enemy Health: {enemy.enemy_health}", enemy.enemy_sprite.center_x - 100, SCREEN_HEIGHT - 20, arcade.color.WHITE, 20, 180, "left")
                if enemy.enemy_health < 100:
                    arcade.draw_rectangle_filled(bar_x, bar_y + -10, health_bar_width, 3, arcade.color.RED)
                
                health_width = health_bar_width * (enemy.enemy_health / 100)

                arcade.draw_rectangle_filled(bar_x - 0.5 * (health_bar_width - health_width), bar_y - 10, health_width, 3, arcade.color.GREEN)

    def player_health_bar(self):
        health_bar_width = 200
        if self.player.player_health > 0:
            bar_x, bar_y = self.player_sprite.center_x, self.player_sprite.center_y - 100
            arcade.draw_text(f"Player Health: {self.player.player_health}", self.player_sprite.center_x - 100, self.player_sprite.center_y - 100, arcade.color.WHITE, 20, 180, "left")

            if self.player.player_health < 100:
                arcade.draw_rectangle_filled(bar_x, bar_y + -10, health_bar_width, 3, arcade.color.RED)
                
            health_width = health_bar_width * (self.player.player_health / 100)

            arcade.draw_rectangle_filled(bar_x - 0.5 * (health_bar_width - health_width), bar_y - 10, health_width, 3, arcade.color.GREEN)
        else:
            arcade.draw_text("GAME OVER!", SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2, arcade.color.WHITE, 20, 180)

    def boss_health_bar(self):
        health_bar_width = 200
        for boss in boss_objects:
            if boss.boss_health > 0:
                bar_x, bar_y = boss.boss_sprite.center_x, SCREEN_HEIGHT - 25
                arcade.draw_text(f"Boss Health: {boss.boss_health}", boss.boss_sprite.center_x - 100, SCREEN_HEIGHT - 25, arcade.color.WHITE, 20, 180, "left")
                if boss.boss_health < 150:
                    arcade.draw_rectangle_filled(bar_x, bar_y + -10, health_bar_width, 3, arcade.color.RED)
                
                health_width = health_bar_width * (boss.boss_health / 150)

                arcade.draw_rectangle_filled(bar_x - 0.5 * (health_bar_width - health_width), bar_y - 10, health_width, 3, arcade.color.GREEN)
                
    def on_draw(self):
        self.clear()
        for star in self.star_list:
            arcade.draw_circle_filled(star.x, star.y, star.size, arcade.color.WHITE)
        self.player_list.draw()
        enemy_list.draw()
        boss_list.draw()
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.enemy_health_bar()
        self.player_health_bar()
        self.boss_health_bar()
        arcade.draw_text(f"Level: {self.level}", 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20, 180, "left")
        arcade.draw_text(f"Wave: {self.wave}", 20, SCREEN_HEIGHT - 80, arcade.color.WHITE, 20, 180, "left")
        
        
    def check_player_bullet_pos(self):
        for bullet in self.player_bullet_list:
            if bullet.top > SCREEN_HEIGHT:
                self.player_bullet_list.remove(bullet)

    def check_enemy_bullet_pos(self):
        for bullet in self.enemy_bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def check_star_pos(self, delta_time):
        for star in self.star_list:
            star.y -= star.speed * delta_time
            if star.y < 0:
                star.reset_pos()
    
    def start_new_game(self):
        if self.wave < 3:
            self.wave += 1 
        else:
            self.level += 1
            self.wave = 0
            self.enemy_bullet_damage += 2
            self.enemy_dodge_skill += 50
            self.boss_dodge_skill += 50
 
        self.player.player_health = 100

        if self.level % 5 == 0 and self.wave == 3:
            self.boss = Boss(x_position=random.randint(0, SCREEN_WIDTH))
            boss_objects.append(self.boss)
            self.boss_spawned = True

        else:
            self.enemy = Enemy(x_position=random.randint(0, SCREEN_WIDTH))
            self.enemy2 = Enemy(x_position=random.randint(0, SCREEN_WIDTH))

        enemy_objects.append(self.enemy)
        enemy_objects.append(self.enemy2)

    def check_to_move_to_next_lvl(self):
        if self.boss_spawned:
            for boss in boss_objects:
                if boss.boss_health <= 0:
                    boss.boss_sprite.remove_from_sprite_lists()
                    self.boss_spawned = False
                    self.start_new_game()

        else:
            enemy_death_count = 0
            for enemy in enemy_objects:
                if enemy.enemy_health == 0:
                    enemy_death_count += 1
            
            if enemy_death_count == len(enemy_objects):
                self.start_new_game()
    
    def check_boss_hit(self):
        for boss in boss_objects:
            hit_list = arcade.check_for_collision_with_list(boss.boss_sprite, self.player_bullet_list)
            for sprites in hit_list:
                sprites.remove_from_sprite_lists()
                if boss.boss_health > 0:
                    boss.boss_health -= self.player_bullet_damage
                    self.check_to_move_to_next_lvl()

    def check_enemy_hit(self):
        for enemy in enemy_objects:
            hit_list = arcade.check_for_collision_with_list(enemy.enemy_sprite, self.player_bullet_list)
            for sprites in hit_list:
                sprites.remove_from_sprite_lists()
                if enemy.enemy_health > 0:
                    enemy.enemy_health -= self.player_bullet_damage
                    self.check_to_move_to_next_lvl()
    
    def check_player_hit(self):
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)
        for sprites in hit_list:
            sprites.remove_from_sprite_lists()
            if self.boss_spawned:
                self.player.player_health -= self.boss_bullet_damage
            else:
                self.player.player_health -= self.enemy_bullet_damage

    def move_enemy(self):
        for enemy in enemy_objects:
            for bullet in self.player_bullet_list:
                if enemy.enemy_sprite.center_y - bullet.center_y < self.enemy_dodge_skill: # decrease to make it easier, increase to make harder
                    if bullet.center_x >= enemy.enemy_sprite.center_x:
                        if enemy.enemy_sprite.center_x <= 100:
                            enemy.enemy_sprite.change_x = 100 # Prevents player going out of bounds
                        else:
                            enemy.enemy_sprite.change_x = -MOVEMENT_SPEED

                    elif bullet.center_x <= enemy.enemy_sprite.center_x:
                        if enemy.enemy_sprite.center_x >= SCREEN_WIDTH - 100:
                            if enemy.enemy_sprite.center_x >= SCREEN_WIDTH - 200: # Move player away from bounds
                                enemy.enemy_sprite.change_x = -100
                        else:
                            enemy.enemy_sprite.change_x = MOVEMENT_SPEED

                if bullet.center_y > enemy.enemy_sprite.center_y:
                    enemy.enemy_sprite.change_x = 0

    def move_boss(self):
        for boss in boss_objects:
            for bullet in self.player_bullet_list:
                if boss.boss_sprite.center_y - bullet.center_y < self.boss_dodge_skill:
                    if bullet.center_x >= boss.boss_sprite.center_x:
                        if boss.boss_sprite.center_x <= 100:
                            boss.boss_sprite.change_x = 100 # Prevents player going out of bounds
                        else:
                            boss.boss_sprite.change_x = -MOVEMENT_SPEED

                    elif bullet.center_x <= boss.boss_sprite.center_x:
                        if boss.boss_sprite.center_x >= SCREEN_WIDTH - 100:
                            if boss.boss_sprite.center_x >= SCREEN_WIDTH - 200: # Move player away from bounds
                                boss.boss_sprite.change_x = -100
                        else:
                            boss.boss_sprite.change_x = MOVEMENT_SPEED

                if bullet.center_y > boss.boss_sprite.center_y:
                    boss.boss_sprite.change_x = 0
            

    def check_player_pos(self):
        if self.player_sprite.center_y < 0:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.player_sprite.center_y > SCREEN_HEIGHT:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif self.player_sprite.center_x < 0:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif self.player_sprite.center_x > SCREEN_WIDTH:
            self.player_sprite.change_x = -MOVEMENT_SPEED

    def enemy_shoot(self):
            for enemy in enemy_list:
                start_x = enemy.center_x
                start_y = enemy.bottom
                dest_x = self.player_sprite.center_x
                dest_y = self.player_sprite.center_y
                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)
                if self.player.player_health > 0:
                    if self.frame_count % 60 == 0:
                        bullet = Enemy_Bullets(":resources:images/space_shooter/laserBlue01.png")
                        bullet.center_x = start_x
                        bullet.center_y = start_y
                        bullet.angle = math.degrees(angle)
                        bullet.change_x = math.cos(angle) * BULLET_SPEED
                        bullet.change_y = math.sin(angle) * BULLET_SPEED
                        self.enemy_bullet_list.append(bullet)
                        self.check_enemy_bullet_pos()
                else:
                    return

    def boss_shoot(self):
        for boss in boss_list:
            start_x = boss.center_x
            start_y = boss.bottom
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)
            if self.player.player_health > 0:
                if self.frame_count % 60 == 0:
                    bullet = Enemy_Bullets(":resources:images/space_shooter/laserBlue01.png")
                    bullet.center_x = start_x
                    bullet.center_y = start_y
                    bullet.angle = math.degrees(angle)
                    bullet.change_x = math.cos(angle) * BULLET_SPEED
                    bullet.change_y = math.sin(angle) * BULLET_SPEED

                    bullet2 = Enemy_Bullets(":resources:images/space_shooter/laserBlue01.png")
                    bullet2.center_x = start_x - 20
                    bullet2.center_y = start_y
                    bullet2.angle = math.degrees(angle)
                    bullet2.change_x = math.cos(angle) * BULLET_SPEED
                    bullet2.change_y = math.sin(angle) * BULLET_SPEED

                    self.enemy_bullet_list.append(bullet)
                    self.enemy_bullet_list.append(bullet2)
                    self.check_enemy_bullet_pos()

                else:
                    return

    def on_update(self, delta_time):
        self.player_list.update()
        self.frame_count += 1
        self.enemy_shoot()
        self.boss_shoot()
        self.check_star_pos(delta_time)
        self.check_player_pos()
        self.player_bullet_list.update()
        self.enemy_bullet_list.update()
        self.check_enemy_hit()
        self.check_player_hit()
        self.check_boss_hit()
        self.move_enemy()

        if self.boss_spawned:
            self.move_boss()
            self.boss_health_bar()

        enemy_list.update()
        boss_list.update()

        if self.player.player_health <= 0:
            self.player_sprite.remove_from_sprite_lists()

        for enemy in enemy_objects:
            if enemy.enemy_health == 0:
                enemy.enemy_sprite.remove_from_sprite_lists()

    def check_player_shoot(self):
        """Check if we have passed a small delta of allow time before the player is allowed to shoot"""
        return (time.perf_counter() - self.player_last_shoot_time) > self.player_shoot_delta

    def handle_shoot(self):
        """Handle the actions for user shooting event"""
        if not self.check_player_shoot():
            return
        bullet_sprite = Player_Bullets(":resources:images/space_shooter/laserBlue01.png")
        bullet_sprite.guid = "Bullet"
        bullet_sprite.change_y = -math.cos(math.radians(180)) * BULLET_SPEED
        bullet_sprite.center_x = self.player_sprite.center_x
        bullet_sprite.center_y = self.player_sprite.top
        bullet_sprite.update()
        self.check_player_bullet_pos()
        self.player_bullet_list.append(bullet_sprite) 
        self.player_last_shoot_time = time.perf_counter()

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
        if symbol == arcade.key.SPACE and self.player.player_health != 0:
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
