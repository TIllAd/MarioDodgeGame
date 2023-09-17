import pygame
import time
import random
from enum import Enum
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MarioDodgeGame")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_HEIGHT = 10
STAR_WIDTH = 20
STAR_VEL = 3

POWERUP_VEL = 1


class GoodEffects(Enum):
    Invincibility = 1
    SmallSize = 2
    ExtraLife = 3

    #
    # SmallSize = 2



sound_channels = [pygame.mixer.Channel(i) for i in range(8)]


# game_music = pygame.mixer.music.load("GameSound.mp3")
# game_music = pygame.mixer.Sound("GameSound.mp3")


game_music = pygame.mixer.Sound("Media/Audio/GameSound.mp3")
game_music_channel = pygame.mixer.find_channel()
game_music_channel.play(game_music, loops=-1)


gameloss_sound = pygame.mixer.Sound("Media/Audio/GameLossSound.mp3")

player_healthup = pygame.mixer.Sound("Media/Audio/PlayerHealthUp.mp3")

# powerup_sound = pygame.mixer.Sound("Mario Powerup.wav")
powerup_sound = pygame.mixer.Sound("Media/Audio/MarioPowerUp.mp3")

BG = pygame.image.load("Media/Graphics/MarioBG.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

player_image = pygame.image.load("Media/Graphics/Mario.png")
player_image = pygame.transform.scale(player_image,(PLAYER_WIDTH,PLAYER_HEIGHT) )

star_image = pygame.image.load("Media/Graphics/GreenShell.png")
star_image = pygame.transform.scale(star_image, (STAR_WIDTH, STAR_HEIGHT))

powerup_image = pygame.image.load("Media/Graphics/PowerUp.png")
powerup_image = pygame.transform.scale(
    powerup_image, (STAR_WIDTH, STAR_HEIGHT))

player_image_powerup = pygame.image.load("Media/Graphics/MarioPowerUp.png")
player_image_powerup = pygame.transform.scale(
    player_image_powerup, (PLAYER_WIDTH, PLAYER_HEIGHT))

current_player_image = player_image
FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars, powerups, current_player_image, player_health):

    WIN.blit(BG, (0, 0))
    # pygame.draw.rect(WIN, (0, 0, 0), player)
    player_outline = player.copy()
    player_outline.inflate_ip(5, 5)
    pygame.draw.rect(WIN, (255, 0, 0), player_outline, 2)

    WIN.blit(current_player_image, (player.x, player.y))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    health_text = FONT.render(f"Health: {player_health}", 1 , "red")
    WIN.blit(time_text, (10, 10))
    WIN.blit(health_text,(WIDTH - 200, 10))

    for star in stars:
        WIN.blit(star_image, (star.x, star.y))

    for powerup in powerups:
        WIN.blit(powerup_image, (powerup.x, powerup.y))

    pygame.display.update()


def set_image_alpha(image, alpha):

    return image.copy().convert_alpha()

def halfPLayerSize(player, current_player_image):
    
    player.height /= 2
    player.width /= 2
    
    
    scaled_image = pygame.transform.scale(current_player_image, (player.width, player.height))
    return player, scaled_image

def doublePlayerSize(player, current_player_image):
    player.height *= 2
    player.width *= 2
    scaled_image = pygame.transform.scale(current_player_image, (PLAYER_WIDTH*2, PLAYER_HEIGHT*2))
    return player, scaled_image

def main():
    run = True


    original_player_image = player_image  # Save the original image
    original_player_size = (PLAYER_WIDTH, PLAYER_HEIGHT)

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    player_invincible = False
    player_smallsize = False
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    selected_good_effect = None
    invincibility_effect_duration = 0
    small_size_duration = 0

    star_add_increment = 2000
    star_count = 0

    powerup_add_increment = 3000
    powerup_count = 0
    powerups = []
    hitGood = False

    stars = []
    hitBAD = False
    is_blinking = False
    player_health = 3
    player_play_again = False
    player_game_loss  = False

    while run:

        star_count += clock.tick(60)
        powerup_count += clock.tick(40)
        elapsed_time = time.time() - start_time

        if powerup_count > powerup_add_increment:
            for _ in range(1):
                powerup_x = random.randint(0, WIDTH - STAR_WIDTH)
                powerup = pygame.Rect(
                    powerup_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                powerups.append(powerup)
                powerup_add_increment = max(200, powerup_add_increment - 50)
                powerup_count = 0

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT,
                                   STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + player.height + PLAYER_VEL < HEIGHT:
            player.y += PLAYER_VEL

        if player.y + player.height <= HEIGHT:
            player.y += PLAYER_VEL / 2.5

        if player_invincible:
            invincibility_effect_duration -= clock.tick(60) / 1000
          
            print(invincibility_effect_duration)
            
            alpha = max(0, int((invincibility_effect_duration / 150) * 255))
            current_player_image = set_image_alpha(player_image_powerup, alpha)
        
            if invincibility_effect_duration < 1:
                is_blinking = not is_blinking
                if is_blinking:
                    alpha = max(0, int((invincibility_effect_duration / 150) * 255))
                    current_player_image = set_image_alpha(player_image_powerup, alpha)
                else:
                    current_player_image = player_image
               

           

        if player_smallsize:
            
            if PLAYER_HEIGHT == player.height and PLAYER_WIDTH == player.width:
                player, current_player_image = halfPLayerSize(player, current_player_image)
            
            print(small_size_duration)
            
            if small_size_duration <= 0:
                player_smallsize = False  
                current_player_image = player_image
                player.height = PLAYER_HEIGHT
                player.width = PLAYER_WIDTH
           

            small_size_duration -= clock.tick(60) / 1000
            
        


        if invincibility_effect_duration <= 0:
            player_invincible = False
            

            invincibility_effect_duration = 0
            current_player_image = player_image
         

        for powerup in powerups[:]:
            powerup.y += POWERUP_VEL
            if powerup.y > HEIGHT:
                powerups.remove(powerup)
            elif powerup.y + powerup.height >= player.y and powerup.colliderect(player):
                powerups.remove(powerup)
                hitGood = True

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hitBAD = True
                break

        if hitBAD and player_invincible == False:

            player_health -= 1
            

            print("subtracting player health")

            if player_health < 0:
                player_game_loss = True
                lost_text = FONT.render("You Lost!", 1, "white")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width() /
                        2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                game_music.stop()

                gameloss_channel = sound_channels[0] 
                gameloss_channel.play(gameloss_sound, loops=-1)

                pygame.time.delay(4000)

                break
            hitBAD = False
        
       



        if hitGood:

          
            powerup_channel = sound_channels[1]  # Use the second sound channel
            powerup_channel.play(powerup_sound, 1)

            selected_good_effect = random.choice(list(GoodEffects))

            if selected_good_effect == GoodEffects.SmallSize:
                player_smallsize = True
                small_size_duration = 4
            if selected_good_effect == GoodEffects.Invincibility:
                player_invincible = True
                invincibility_effect_duration = 1
            if selected_good_effect == GoodEffects.ExtraLife:
                player_health += 1
                gameloss_channel = sound_channels[2] 
                gameloss_channel.play(player_healthup, 1)
           

              
            hitGood = False

         

        draw(player, elapsed_time, stars, powerups, current_player_image, player_health)
        
        


    pygame.quit()


if __name__ == "__main__":
    main()
