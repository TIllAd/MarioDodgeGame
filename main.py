import pygame
import time
import random
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

#game_music = pygame.mixer.music.load("GameSound.mp3")  
#game_music = pygame.mixer.Sound("GameSound.mp3")  


game_music = pygame.mixer.Sound("GameSound.mp3")
game_music_channel = pygame.mixer.find_channel()
game_music_channel.play(game_music, loops=-1)


music2 = pygame.mixer.Sound("GameLossSound.mp3")  

BG = pygame.image.load("MarioBG.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

player_image = pygame.image.load("Mario.png")
star_image = pygame.image.load("GreenShell.png")

star_image = pygame.transform.scale(star_image, (STAR_WIDTH, STAR_HEIGHT))

player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars):
     

    WIN.blit(BG, (0, 0))
    #pygame.draw.rect(WIN, (0, 0, 0), player)
    player_outline = player.copy()
    player_outline.inflate_ip(5,5)
    pygame.draw.rect(WIN,(255, 0, 0), player_outline, 2)

    WIN.blit(player_image, (player.x, player.y))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
   

    for star in stars:
       WIN.blit(star_image, (star.x, star.y))

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit  = False
    while run:
    
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
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
            player.y +=PLAYER_VEL

        if player.y + player.height <= HEIGHT:
            player.y += PLAYER_VEL / 2.5

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            game_music.stop()
          
            music2_channel = pygame.mixer.find_channel()
            music2_channel.play(music2, loops=-1, )  

            pygame.time.delay(4000)
            break


        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main()
