import arcade
import random
import warnings

# Suppress the performance warning window log completely from clogging the terminal console
warnings.filterwarnings("ignore", category=UserWarning)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Avoid the Falling Blocks! (Arcade Edition)"
WINNING_SCORE = 10

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.BLACK
        
        # Game State Control
        self.game_state = "PLAYING"
        self.score = 0
        self.end_message = ""

        # Player Properties
        self.player_x = SCREEN_WIDTH / 2
        self.player_y = 100
        self.player_size = 50
        self.player_speed = 7
        
        # Jump Properties
        self.is_jumping = False
        self.jump_count = 10

        # Falling Obstacle Properties
        self.obstacle_size = 50
        self.obstacle_x = random.randint(0, SCREEN_WIDTH - self.obstacle_size)
        self.obstacle_y = SCREEN_HEIGHT + 50
        self.obstacle_speed = 5

        # Tracking active keystrokes
        self.left_pressed = False
        self.right_pressed = False

        # 🛠️ FIXED: Pre-load the static sound assets into memory correctly for Arcade 3.x
        # Using the engine's built-in asset catalog string format
        self.point_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")

    def on_draw(self):
        """ Render Engine """
        self.clear()

        if self.game_state == "PLAYING":
            # Draw shapes via the XYWH layout
            player_rectangle = arcade.XYWH(self.player_x, self.player_y, self.player_size, self.player_size)
            arcade.draw_rect_filled(player_rectangle, arcade.color.RED)

            obstacle_rectangle = arcade.XYWH(self.obstacle_x, self.obstacle_y, self.obstacle_size, self.obstacle_size)
            arcade.draw_rect_filled(obstacle_rectangle, arcade.color.BLUE)

            # Draw the HUD UI metric text 
            arcade.draw_text(
                f"Score: {self.score} / {WINNING_SCORE}",
                20, SCREEN_HEIGHT - 40,
                arcade.color.WHITE, 20, font_name="Arial"
            )

        else:
            color = arcade.color.GREEN if "WIN" in self.end_message else arcade.color.RED
            arcade.draw_text(
                self.end_message,
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20,
                color, 40, bold=True, anchor_x="center"
            )
            arcade.draw_text(
                "Press ENTER to play again",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                arcade.color.WHITE, 20, anchor_x="center"
            )

    def on_update(self, delta_time):
        """ Physics & Logic Processing Loop Engine """
        if self.game_state != "PLAYING":
            return

        # Player Movement
        if self.left_pressed: self.player_x -= self.player_speed
        if self.right_pressed: self.player_x += self.player_speed

        half_size = self.player_size / 2
        if self.player_x < half_size: self.player_x = half_size
        if self.player_x > SCREEN_WIDTH - half_size: self.player_x = SCREEN_WIDTH - half_size

        # Jump calculations
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count >= 0 else -1
                self.player_y += (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10
                self.player_y = 100

        # Obstacle Fall update 
        self.obstacle_y -= self.obstacle_speed

        # Point Condition Check
        if self.obstacle_y < -50:
            self.score += 1
            self.obstacle_speed += 0.5
            self.respawn_obstacle()
            
            # 🛠️ FIXED: Play the pre-loaded point tracking audio channel safely 
            arcade.play_sound(self.point_sound)

            if self.score >= WINNING_SCORE:
                self.game_state = "FINISHED"
                self.end_message = "YOU WIN! 🏆"

        # Geometric Coordinate Collision Check
        if (abs(self.player_x - self.obstacle_x) < self.player_size) and \
           (abs(self.player_y - self.obstacle_y) < self.player_size):
            
            # 🛠️ FIXED: Play the pre-loaded game over tracking audio channel safely
            arcade.play_sound(self.game_over_sound)
            self.game_state = "FINISHED"
            self.end_message = "GAME OVER ❌"

    def respawn_obstacle(self):
        self.obstacle_y = SCREEN_HEIGHT + 50
        self.obstacle_x = random.randint(int(self.obstacle_size), int(SCREEN_WIDTH - self.obstacle_size))

    def on_key_press(self, key, modifiers):
        if self.game_state == "PLAYING":
            if key == arcade.key.LEFT: self.left_pressed = True
            elif key == arcade.key.RIGHT: self.right_pressed = True
            elif key == arcade.key.SPACE and not self.is_jumping: self.is_jumping = True
        else:
            if key == arcade.key.ENTER: self.reset_game()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT: self.left_pressed = False
        elif key == arcade.key.RIGHT: self.right_pressed = False

    def reset_game(self):
        self.score = 0
        self.obstacle_speed = 5
        self.player_x = SCREEN_WIDTH / 2
        self.player_y = 100
        self.is_jumping = False
        self.jump_count = 10
        self.respawn_obstacle()
        self.game_state = "PLAYING"

def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
	