import pygame,sys,random
pygame.init()
screen=pygame.display.set_mode((576,800))
clock=pygame.time.Clock()
message=pygame.transform.scale((pygame.image.load("message.png")),(200,400))
bg_day=pygame.transform.scale(pygame.image.load("backgroung_flappy_upper.jpg"),(576,800)).convert_alpha()
bg_night=pygame.transform.scale(pygame.image.load("background-night.png"),(576,800)).convert_alpha()
bg_frames=[bg_day,bg_night]
bg_index=0
bg_surface=bg_frames[bg_index]
# bg_surface=pygame.image.load("backgroung_flappy_upper.jpg").convert_alpha()
# bg_surface=pygame.transform.scale(bg_surface,(576,800)).convert_alpha()
floor_surface=pygame.image.load("ground.png").convert_alpha()
floor_surface=pygame.transform.scale(floor_surface,(600,100)).convert_alpha()
bird_upflap=pygame.transform.scale2x(pygame.image.load("bluebird-upflap.png")).convert_alpha()
bird_midflap=pygame.transform.scale2x(pygame.image.load("bluebird-midflap.png")).convert_alpha()
bird_downflap=pygame.transform.scale2x(pygame.image.load("bluebird-downflap.png")).convert_alpha()
bird_frames=[bird_downflap,bird_midflap,bird_upflap]
bird_index=0
bird_surface=bird_frames[bird_index]
bird_rect=bird_surface.get_rect(center=(100,300))
pipe_surface=pygame.image.load("pipe.png").convert_alpha()
pipe_surface=pygame.transform.scale2x(pipe_surface).convert_alpha()
floor_x_pos=0

bird_flap=pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
def gameloop():
    p=0
    global bird_index,floor_x_pos,bg_index
    def draw_floor():
        screen.blit(floor_surface, (floor_x_pos, 700))
        screen.blit(floor_surface, (floor_x_pos+576, 700))
    def create_pipe():
        random_pipe_pos=random.choice(pipe_heights)
        bottom_pipe=pipe_surface.get_rect(midtop=(600,random_pipe_pos))
        top_pipe=pipe_surface.get_rect(midbottom=(600,random_pipe_pos-180))
        print(random_pipe_pos)
        return bottom_pipe,top_pipe
    def move_pipes(pipes):
        for pipe in pipes:
            pipe.centerx-=3
        return pipes
    def draw_pipes(pipes):
        for pipe in pipes:
            if pipe.bottom>=800:
                screen.blit(pipe_surface,pipe)
            else:
                flipped_pipe=pygame.transform.flip(pipe_surface,False,True)
                screen.blit(flipped_pipe,pipe)
    def check_collision(pipe_list):
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe):
                return False
        if bird_rect.top<=0 or bird_rect.bottom>=700:
            return False
        return True
    def rotate_bird(bird):
        new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
        return new_bird
    def pause():
        paused=True
        font=pygame.font.Font(None,50)
        text1=font.render("GAME PAUSED",True,(255,255,255))
        text2=font.render("press enter to continue",True,(255,255,255))
        while paused:
            screen.blit(bg_surface, (0, 0))
            screen.blit(floor_surface, (0, 700))
            screen.blit(text1, (160,100))
            screen.blit(text2, (100,300))
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        paused=False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    swapn_pipe=pygame.USEREVENT
    change_day=pygame.USEREVENT+2
    pygame.time.set_timer(swapn_pipe,1200)
    pygame.time.set_timer(change_day,15000)
    pipe_list=[]
    pipe_heights=[300,400,500,600]
    gravity=0.1
    bird_movement=0
    fps=140
    game_active=True
    while True:
        bg_surface=bg_frames[bg_index]
        screen.blit(bg_surface, (0, 0))
        bird_surface = bird_frames[bird_index]

        if game_active:
            rotated_bird = rotate_bird(bird_surface)
            if p==0:
                pipe_list = move_pipes(pipe_list)
            screen.blit(rotated_bird, bird_rect)
            draw_pipes(pipe_list)
            game_active = check_collision(pipe_list)
            bird_movement += gravity
            bird_rect.centery += bird_movement
        else:
            screen.blit(message,(180,200))
        draw_floor()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    bird_movement=0
                    bird_movement=-4
                if event.key==pygame.K_SPACE and game_active==False:
                    game_active=True
                    bird_rect.center=(100, 300)
                    pipe_list.clear()
                    bird_movement=0
                if event.key==pygame.K_ESCAPE:
                    pause()
            if event.type==swapn_pipe:
                pipe_list.extend(create_pipe())
            if event.type==bird_flap:
                if bird_index<2:
                    bird_index+=1
                else:
                    bird_index=0
            if event.type==change_day:
                if bg_index==0:
                    bg_index=1
                else:
                    bg_index=0
        floor_x_pos -= 1
        if (floor_x_pos<=-576):
            floor_x_pos=0
        clock.tick(fps)
        pygame.display.update()
gameloop()