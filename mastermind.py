import pygame
import random

pygame.init()
# colors=[(255, 0, 0),(0, 255, 0)]
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
YELLOW=(255, 255, 0)
CYAN=(0, 255, 255)
PURPLE=(255, 0, 255)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
GRAY=(136,136,136)
DIM_GREY=(105,105,105)
DIM_GREY2=(160,160,160)
WIDTH, HEIGHT = 700, 600
PEGS = ["red","blue","green","yellow","cyan","purple","pink","white"]
# 8 colors
# circleX=500
# circleY=400
# radius=10

big_font=pygame.font.Font(None,50)
small_font=pygame.font.Font(None,16)
medium_font=pygame.font.Font(None,25)

class MasterMind:
    circleX=500
    circleY=400
    radius=10
    
    def __init__(self):
        #Pegs to be displayed
        self.pegs=[]

        #Split the pegs in a new line after the first four
        split_peg_line=0

        #What colors you picked
        self.clicked_colors=[]

        #Amount of tries before you fail
        self.tries=12

        #Move the text a specific y angle.
        self.move_y=40

        #Unique colors
        # self.secret_code=random.sample(PEGS,4)
        #Mixed random colors
        self.secret_code = random.choices(PEGS, k=4)

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.window.fill((GRAY))
        #tries Box
        pygame.draw.rect(self.window,WHITE,(450,0,250,350)) #(x,y,width,heigth)
        #Added Box
        pygame.draw.rect(self.window,DIM_GREY2,(250,0,200,350)) #(x,y,width,heigth)
        #Info Box
        pygame.draw.rect(self.window,DIM_GREY,(0,0,WIDTH-250,150)) #(x,y,width,heigth)
        #Color box
        pygame.draw.rect(self.window,BLACK,(WIDTH-250,HEIGHT-250,250,350)) #(x,y,width,heigth)
        pygame.display.set_caption("Mastermind")
        self.window.blit(big_font.render("Mastermind!",True,RED),(20, 20))
        self.window.blit(medium_font.render("Tries",True,RED),(550, 20))
        self.window.blit(medium_font.render("Added",True,RED),(320, 180))
        self.draw_text("Rules!\nGuess the four random colors\nRed=correct color in the right spot\nWhite=correct color but wrong spot\nDud= Not a secret color", RED, 250, 20)
        print(self.secret_code)
        
        #Prints the color in the blackbox
        for i in range(8):
            if split_peg_line==4:
                self.circleY+=80
                self.circleX=500
            peg=pygame.draw.circle(self.window,PEGS[i],(self.circleX,self.circleY),self.radius)
            self.pegs.append((peg,PEGS[i]))
            self.circleX+=50
            split_peg_line+=1
        pygame.display.update()

        self.start()

    #Rules textbox
    def draw_text(self, text, color, x, y):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            rendered_line = small_font.render(line, True, color)
            self.window.blit(rendered_line, (x, y + i * 20)) 

    def start(self):
        move_X=20
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                #Checks what color the mouse button is on.
                elif event.type== pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    for circle,color in self.pegs:
                        if circle.collidepoint(x, y):# Check if the click is within the circle
                            #List is not full
                            self.clicked_colors.append(color) 
                            move_X=40*len(self.clicked_colors)
                            self.window.blit(small_font.render(f"{color}",True,color),(230+move_X, 240))
                            pygame.display.update()
                            print(move_X)
                            
                            #List is full. drawing new greybox over player options
                            if len(self.clicked_colors)>3:
                                self.check_colors(self.move_y)
                                self.move_y+=30 #Distance between old and new info from Tries box and Color box
                                self.clicked_colors=[]
                                self.window.blit(medium_font.render("Added",True,RED),(320, 180))
                                pygame.draw.rect(self.window,DIM_GREY2,(250,220,200,100))
                                pygame.display.update()
                                

    def check_colors(self,move_y):
        compare_list=[]
        self.font=pygame.font.Font(None,25)
        #Color box split items.
        self.textX=480
        self.textY=20+move_y
        self.correct=0
        #Tries box split items.
        self.listedX=70
        self.listedY=180+move_y

        for i in range(4):
            if self.clicked_colors[i]==self.secret_code[i]:
                compare_list.append('Red')
                self.correct+=1
            elif self.clicked_colors[i] in self.secret_code:
                compare_list.append('White')
            else:
                compare_list.append('Dud')

        if self.correct==4:
                self.window.blit(big_font.render(f"You win!",True,BLACK),(WIDTH/3, HEIGHT/2))
                pygame.display.update()
                while True:
                    for event in pygame.event.get():
                        if event.type== pygame.MOUSEBUTTONDOWN:
                            pygame.quit()
                            exit()
        elif self.tries == 0:
                print("Game over!")
                pygame.quit()
                exit()    
        else:   
                #Drawing colors onto color box.
                compare_list=', '.join(compare_list)
                print(compare_list)
                for i in range(4):
                    pygame.draw.circle(self.window,self.clicked_colors[i],(self.listedX,self.listedY),self.radius)
                    self.listedX+=50

                self.window.blit(self.font.render(f"{compare_list}",True,BLACK),(self.textX, self.textY))
                pygame.display.update()

init=MasterMind()   