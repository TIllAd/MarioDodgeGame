import pygame
import time
import random
from enum import Enum
import math
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MarioDodgeGame")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

BOWSER_WIDTH = 100
BOWSER_HEIGHT = 150


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

class Fireball:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 7  # Adjust the speed as needed
        self.image = fireball_image  # Load the fireball image
        # Calculate the velocity towards the target (player)
        direction_x = target_x - x
        direction_y = target_y - y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance > 0:
            self.velocity_x = direction_x / distance * self.speed
            self.velocity_y = direction_y / distance * self.speed

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def out_of_bounds(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

    def colliderect(self, rect):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()).colliderect(rect)

                    
                    



sound_channels = [pygame.mixer.Channel(i) for i in range(8)]


game_music = pygame.mixer.Sound("Media/Audio/GameSound.mp3")
game_music_channel = pygame.mixer.find_channel()
game_music_channel.play(game_music, loops=-1)
gameloss_sound = pygame.mixer.Sound("Media/Audio/GameLossSound.mp3")
player_healthup = pygame.mixer.Sound("Media/Audio/PlayerHealthUp.mp3")
powerup_sound = pygame.mixer.Sound("Media/Audio/MarioPowerUp.mp3")
bowser_start_sound = pygame.mixer.Sound("Media/Audio/bowser_start.mp3")
bowser_laugh_sound = pygame.mixer.Sound("Media/Audio/bowser_laugh.wav")

BG = pygame.image.load("Media/Graphics/MarioBG.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
BG_Bowser = pygame.image.load("Media/Graphics/Bossfight.png")
BG_Bowser = pygame.transform.scale(BG_Bowser,(WIDTH, HEIGHT))
bowser_transition_screen = pygame.image.load("Media/Graphics/bowser_transition_screen.jpg")
bowser_transition_screen = pygame.transform.scale(bowser_transition_screen,(WIDTH, HEIGHT))

bowser_idle = pygame.image.load("Media/Graphics/Bowser.png")
bowser_idle = pygame.transform.scale(bowser_idle,(BOWSER_WIDTH, BOWSER_HEIGHT))
bowser_running = pygame.image.load("Media/Graphics/bowser_running.jpeg")
bowser_running = pygame.transform.scale(bowser_running,(BOWSER_WIDTH, BOWSER_HEIGHT))
bowser_angry = pygame.image.load("Media/Graphics/bowser_shooting.jpeg")
bowser_angry = pygame.transform.scale(bowser_angry,(BOWSER_WIDTH, BOWSER_HEIGHT))




fireball_image = pygame.image.load("Media/Graphics/fireball.png")
fireball_image = pygame.transform.scale(fireball_image,(BOWSER_WIDTH, BOWSER_HEIGHT))


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


def draw(player, elapsed_time, stars, powerups, current_player_image, player_health, current_countdown_number):

    WIN.blit(BG, (0, 0))
    player_outline = player.copy()
    player_outline.inflate_ip(5, 5)
   # pygame.draw.rect(WIN, (255, 0, 0), player_outline, 2)
    WIN.blit(current_player_image, (player.x, player.y))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    health_text = FONT.render(f"Health: {player_health}", 1 , "red")
    WIN.blit(time_text, (10, 10))
    WIN.blit(health_text,(WIDTH - 200, 10))

    for star in stars:
        WIN.blit(star_image, (star.x, star.y))

    for powerup in powerups:
        WIN.blit(powerup_image, (powerup.x, powerup.y))

    if(current_countdown_number != None):
        countdown = FONT.render(f" {round(current_countdown_number)}...", 1, "white")
        WIN.blit(countdown, (WIDTH/2 , HEIGHT/2))

    pygame.display.update()

def drawBossBowser( player, player_health, Bowser, fireballs ,bowser_state):


    if bowser_state == "Idle":
        bowser_image = bowser_idle
    elif bowser_state == "Charging":
        bowser_image = bowser_running
    elif bowser_state == "Angry":
        bowser_image = bowser_angry



    WIN.blit(BG_Bowser, (0,0))
    WIN.blit(bowser_image, (Bowser.x, Bowser.y))
    WIN.blit(player_image, (player.x, player.y))

    for fireball in fireballs:
        WIN.blit(fireball_image, (fireball.x, fireball.y))

    pygame.display.update()

def draw_transition_screen(background, displaytext):
    WIN.blit(background, (0, 0))
    displaytext = FONT.render(f"Boss : {(displaytext)}", 1, "white")
    
    WIN.blit(displaytext, (10, 10))
    pygame.display.update()

def draw_countdown(start_number):
    print("reached")
    countdown = FONT.render(f" {round(start_number)}", 1, "white")
    WIN.blit(countdown, (WIDTH/2 , HEIGHT/2))

    pygame.display.update()
    
    print("reached2")
     


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

def setBowserState(state):
    
    if state == "Idle":
        bowser_idle_start_time = time.time()
       
        return "Idle" , time.time()
    elif state == "Charging":
        
        return "Charging", time.time()
    elif state == "Angry":
        return "Angry" , time.time()
 

    bowser_state = state
    
    return bowser_state , bowser_idle_start_time

def GameLoss():
    
    lost_text = FONT.render("You Lost!", 1, "white")
    WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width() /
                        2, HEIGHT/2 - lost_text.get_height()/2))
    pygame.display.update()
    game_music.stop()

    gameloss_channel = sound_channels[0] 
    gameloss_channel.play(gameloss_sound, loops=-1)

    pygame.time.delay(4000)
    pygame.quit()
    
    

def main():
    run = True



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
    bowser_charging_start_time = 0
    star_add_increment = 2000
    star_count = 0

    powerup_add_increment = 3000
    powerup_count = 0
    powerups = []
    hitGood = False
    fireballs = []
    stars = []
    hitBAD = False
    is_blinking = False
    player_health = 3
    bowser_fight_starttime = 2
    player_play_again = False
    player_game_loss  = False
    time_last_countdown = 0
    time_elapsed_countdown = None
   
    current_cd_display = None
    player_bowser_positioned = False
    time_between_fireballs = 2
    fireball_timer = 0

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
                gameloss_channel = sound_channels[4] 
                gameloss_channel.play(gameloss_sound, loops=-1)
                pygame.time.delay(4000)
                GameLoss()
                

                break
            hitBAD = False
        
       



        if hitGood:

          
            powerup_channel = sound_channels[1]  
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

        

      

      


        print(round(bowser_fight_starttime - elapsed_time))

        if(  bowser_fight_starttime - elapsed_time > 3 or round(bowser_fight_starttime - elapsed_time) <= 0 ):
                current_countdown_number = None         
        else:
            current_countdown_number = round(bowser_fight_starttime - elapsed_time)           
               


       

        if elapsed_time > bowser_fight_starttime - 0.5:
            

            Bowser = pygame.Rect(300, HEIGHT - BOWSER_HEIGHT, BOWSER_WIDTH, BOWSER_HEIGHT)

            draw_transition_screen(bowser_transition_screen, "Bowser" )

            pygame.mixer.music.pause()
            pygame.time.delay(4000)

            powerup_channel = sound_channels[3]  # Use the second sound channel
            powerup_channel.play(bowser_start_sound, 0)

            battle_master1 = True
            

            bowser_state , bowser_idle_start_time = setBowserState("Idle")
            
            while battle_master1 and run:
                start_time = time.time()
                clock.tick(30)

                #avoid insta lose
                if(player_bowser_positioned == False):
                    Bowser.x, Bowser.y = 100 , 100
                    player.x , player.y = WIDTH -100,  HEIGHT - 100
                    player_bowser_positioned = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        battle_master1 = False
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
                

                if player.colliderect(Bowser):
                    bowser_laugh_sound_channel = sound_channels[5] 
                    bowser_laugh_sound_channel.play(bowser_laugh_sound, 1)
                    pygame.time.delay(2000)
                    GameLoss()
                    break
                        
                    
                
                bowser_charge_duration = 3
                bowser_charge_speed = 5
                bowser_idle_duration = 100
                bowser_idle_random_move_duration = 2  # Adjust the random move duration as needed
                bowser_idle_random_move_start_time = time.time()
                bowser_idle_random_move_direction = (0, 0)
                bowser_idle_speed = 3
                

                
                
                if bowser_state == "Idle":
                   
                    time_elapsed_Bowser = time.time() - bowser_idle_start_time  # Calculate elapsed time

                    if time.time()- bowser_idle_start_time  > 10 :
                       
                        bowser_state, bowser_charging_start_time = setBowserState("Charging")
                        

                        
                    else:

                        destination_random_x = random.choice([0, WIDTH, 0, WIDTH])
                        destination_random_y = random.choice([0, HEIGHT, 0, HEIGHT])
                        bowser_idle_speed = 4
                      

                        direction_x = destination_random_x - Bowser.x
                        direction_y = destination_random_y - Bowser.y

                        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

                        if distance > 0:
                            direction_x /= distance
                            direction_y /= distance 
                        
                        Bowser.x += direction_x * bowser_idle_speed
                        Bowser.y += direction_y * bowser_idle_speed

                if bowser_state == "Charging":

                    time_elapsed_Bowser = time.time() - bowser_charging_start_time

                    print("Time Elsapes" ,time_elapsed_Bowser)

                    if time_elapsed_Bowser < 4:
                            # Bowser stands still for 4 seconds
                            Bowser.x += 0
                            Bowser.y += 0
                    else:
                            
                        bowser_charging_speed = 4
                        print ("charging")

                    
                        direction_x = player.x - Bowser.x
                        direction_y = player.y - Bowser.y

                        
                        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

                        if distance > 0:
                            direction_x /= distance
                            direction_y /= distance

                        Bowser.x += direction_x * bowser_charging_speed
                        Bowser.y += direction_y * bowser_charging_speed
                        print(bowser_charging_start_time - time.time())

                        if(distance <= bowser_charging_speed or time.time()- bowser_charging_start_time  > 10 ):
                            bowser_state, bowser_angry_start_time = setBowserState("Angry")

                       
                    
                    

                if(bowser_state == "Angry"):
                    
                    bowser_image = bowser_angry
                    fireball_timer += clock.tick(60) /1000

                    print("clock tick",clock.tick(60) /10)
                    print(fireball_timer)
                
                    if  fireball_timer>= time_between_fireballs:
                        fireball = Fireball(Bowser.x, Bowser.y, player.x, player.y)
                        fireballs.append(fireball)
                        fireball_timer = 0  # Reset the timer

                    for fireball in fireballs:
                        fireball.update()
                        if fireball.colliderect(player):
                            GameLoss()
                        if fireball.out_of_bounds():
                            fireballs.remove(fireball)
                      

                    #for fireball in fireballs:
                    #    WIN.blit(fireball_image, (fireball.x, fireball.y))
                    print("HERE:" , time.time() - bowser_angry_start_time)

                    if time.time() - bowser_angry_start_time > 20:
                        bowser_state , bowser_idle_start_time = setBowserState("Idle")

                    

























                print(bowser_state)

                drawBossBowser(player, player_health, Bowser, fireballs ,bowser_state)  

    

        
            print("bowser x,y", Bowser.x , Bowser.y)
        
        draw(player, elapsed_time, stars, powerups, current_player_image, player_health, current_countdown_number)
        
        


    pygame.quit()


if __name__ == "__main__":
    main()
