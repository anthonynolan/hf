import arcade
import random

# Set up constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 12
GRAVITY = 0.5
PLAYER_START_X = 100
PLAYER_START_Y = 100
PLAYER_SIZE = 50
PLATFORM_HEIGHT = 20
ENEMY_SIZE = 50
ENEMY_SPEED = 3
ENEMY_JUMP_SPEED = 10
JUMP_SOUND_PATH = "jump.wav"
COLLISION_SOUND_PATH = "collision.wav"
FONT_SIZE = 36


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "My Platform Game")
        arcade.set_background_color(arcade.color.AMAZON)

        # Set up variables for the player
        self.player = arcade.Sprite("player.png")
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y
        self.player.change_x = 0
        self.player.change_y = 0
        self.player.is_jumping = False
        self.player.score = 0

        # Set up variables for the platforms
        self.platforms = arcade.SpriteList()
        self.setup_platforms()

        # Set up variables for the enemies
        self.enemies = arcade.SpriteList()
        self.setup_enemies()

        # Set up sounds
        self.jump_sound = arcade.load_sound(JUMP_SOUND_PATH)
        self.collision_sound = arcade.load_sound(COLLISION_SOUND_PATH)

        # Set up the score text
        self.score_text = arcade.create_text("Score: 0", arcade.color.WHITE, FONT_SIZE)

    def setup_platforms(self):
        # Set up the ground platform
        ground = arcade.SpriteSolidColor(
            SCREEN_WIDTH, PLATFORM_HEIGHT, arcade.color.DARK_GREEN
        )
        ground.position = (SCREEN_WIDTH / 2, 0)
        self.platforms.append(ground)

        # Set up some random platforms
        for i in range(5):
            platform = arcade.SpriteSolidColor(
                random.randint(50, 200), PLATFORM_HEIGHT, arcade.color.DARK_GREEN
            )
            platform.position = (
                random.randint(0, SCREEN_WIDTH - 50),
                random.randint(100, SCREEN_HEIGHT - 50),
            )
            self.platforms.append(platform)

    def setup_enemies(self):
        # Set up some random enemies
        for i in range(3):
            enemy = arcade.Sprite("enemy.png")
            enemy.center_x = random.randint(0, SCREEN_WIDTH)
            enemy.center_y = random.randint(
                PLATFORM_HEIGHT + ENEMY_SIZE, SCREEN_HEIGHT - ENEMY_SIZE
            )
            enemy.change_x = ENEMY_SPEED
            enemy.change_y = 0
            self.enemies.append(enemy)

    def on_draw(self):
        arcade.start_render()

        # Draw the platforms
        self.platforms.draw()

        # Draw the player
        self.player.draw()

        # Draw the enemies
        self.enemies.draw()

        # Draw the score text
        arcade.render_text(
            self.score_text, SCREEN_WIDTH - 150, SCREEN_HEIGHT - FONT_SIZE
        )

    def update(self, delta_time):
        # Update the player
        self.player.update()

        # Handle player movement
        if self.player.change_y > -PLAYER_JUMP_SPEED and self.player.is_jumping:
            self.player.change_y -= GRAVITY
        if self.player.change_y < 0 and not self.player.is_jumping:
            self.player.change_y -= GRAVITY
            self.player.center_y = PLATFORM_HEIGHT + PLAYER_SIZE / 2
            self.player.change_y = 0
            self.player.is_jumping = False
            self.player.center_x += self.player.change_x
            self.player.center_y += self.player.change_y

            # Handle player collision with platforms
            hit_list = arcade.check_for_collision_with_list(self.player, self.platforms)
            for platform in hit_list:
                if (
                    self.player.center_y - PLAYER_SIZE / 2
                    > platform.center_y + PLATFORM_HEIGHT / 2
                ):
                    self.player.center_y = (
                        platform.center_y + PLATFORM_HEIGHT / 2 + PLAYER_SIZE / 2
                    )
                    self.player.change_y = 0
                    self.player.is_jumping = False
                elif (
                    self.player.center_y - PLAYER_SIZE / 2
                    < platform.center_y + PLATFORM_HEIGHT / 2
                ):
                    self.player.center_y = (
                        platform.center_y - PLATFORM_HEIGHT / 2 - PLAYER_SIZE / 2
                    )
                    self.player.change_y = 0
                else:
                    self.player.change_x = 0

            # Handle player collision with enemies
            hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)
            for enemy in hit_list:
                arcade.play_sound(self.collision_sound)
                self.player.score -= 10
                enemy.remove_from_sprite_lists()
                if self.player.score < 0:
                    self.player.score = 0

            # Handle enemy movement
            for enemy in self.enemies:
                if enemy.right >= SCREEN_WIDTH:
                    enemy.change_x = -ENEMY_SPEED
                elif enemy.left <= 0:
                    enemy.change_x = ENEMY_SPEED
                if random.random() < 0.01 and enemy.change_y == 0:
                    enemy.change_y = ENEMY_JUMP_SPEED
                if enemy.change_y > -ENEMY_JUMP_SPEED:
                    enemy.change_y -= GRAVITY
                enemy.center_x += enemy.change_x
                enemy.center_y += enemy.change_y

            # Handle player jumping
            if not self.player.is_jumping and arcade.key.UP in self.current_keys:
                arcade.play_sound(self.jump_sound)
                self.player.change_y = PLAYER_JUMP_SPEED
                self.player.is_jumping = True

            # Handle player movement
            if arcade.key.LEFT in self.current_keys:
                self.player.change_x = -PLAYER_SPEED
            elif arcade.key.RIGHT in self.current_keys:
                self.player.change_x = PLAYER_SPEED
            else:
                self.player.change_x = 0

            # Update the score text
            self.score_text = arcade.create_text(
                "Score: {}".format(self.player.score), arcade.color.WHITE, FONT_SIZE
            )

        def on_key_press(self, key, modifiers):
            self.current_keys.add(key)

        def on_key_release(self, key, modifiers):
            self.current_keys.remove(key)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
