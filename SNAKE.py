# SNAKE CLONE 1.0 
# by Sebastiano Davide Covone
# MIT License

import sys, random, pygame
from pygame.locals import *

#COLORS RGB
red = [102, 0, 0]
light_red = [255, 0, 0]
white = [255,255,255]
indigo = [25, 0, 51]
dimgrey = [192, 192, 192]

#SCREEN SIZE
width = 640
height = 480

#SIZE OF ONE CELL COMPOSING THE GRID
cell_size = 20

#NUMBER OF HORIZONTAL AND VERTICAL CELLS
xcell = int(width/cell_size)  
ycell = int(height/cell_size) 

#FRAME PER SECOND
FPS = 15

#DIRECTIONAL VALUES
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

#INITIALIZE THE SCREEN
pygame.init()
screen = pygame.display.set_mode((width,height))

#SOME FONTS
scoreFont = pygame.font.Font(None, 30)
menuFont = pygame.font.Font(None, 50)
referenceFont = pygame.font.Font(None, 20)
gameOverFont =  pygame.font.Font(None, 60)
restartFont = pygame.font.Font(None, 40)

def main():

	pygame.display.set_caption("Snake Clone") 
	
	screen.fill(dimgrey)

	setMenu()

	runGame()

	GameOver()


def setMenu():

	menuText = menuFont.render("Snake v. 1.0", 1, indigo)
	option1 = menuFont.render("Press Enter to play",1, indigo)
	option2 = menuFont.render("Press Esc to quit the game", 1, indigo)
	option3 = menuFont.render("Press 'g' to set the grid and play", 1, indigo)
	optionPs = referenceFont.render("Feel free to improve this code :)", 1, red)
	reference = referenceFont.render("Sebastiano Davide Covone, 07/2018", 1, red)

	menu_rect = menuText.get_rect(center=(320, 100))
	option1_rect = option1.get_rect(center = (320, 200))
	option2_rect = option2.get_rect(center = (320, 260))
	option3_rect = option3.get_rect(center = (320, 320))
	optionPs_rect = optionPs.get_rect(center = (320, 380))
	reference_rect = reference.get_rect(center = (520, 460))

	screen.blit(menuText, menu_rect)
	screen.blit(option1, option1_rect)
	screen.blit(option2, option2_rect)
	screen.blit(option3, option3_rect)
	screen.blit(optionPs, optionPs_rect)
	screen.blit(reference, reference_rect)

	pygame.display.update()
	
	pause = True

	i = 0

	while pause:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					terminate()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						terminate()
					elif event.key == K_g:
						i += 1
						runGame(i)
					elif event.key == K_RETURN:
						runGame(i)

def runGame(gridParam):

	fps = pygame.time.Clock()

	xstart = random.randint(12, 24)
	ystart= random.randint(6, 18)
	apple_x = random.randint(1, xcell-1)
	apple_y = random.randint(1, ycell-1)

	global direction
	rectCoor = [{'x' : xstart, 'y': ystart},{'x' : xstart - 1, 'y': ystart}, {'x' : xstart - 2 , 'y': ystart}]
	applesCoor= [{'x': apple_x, 'y': apple_y}]
	direction = LEFT

	#main control flow
	while True:

		pygame.display.update()
		
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()

		if keys[pygame.K_LEFT] and direction != RIGHT:
			direction = LEFT
		elif keys[pygame.K_RIGHT] and direction != LEFT:
			direction = RIGHT
		elif keys[pygame.K_UP] and direction != DOWN:
			direction = UP
		elif keys[pygame.K_DOWN] and direction != UP:
			direction = DOWN

		if direction == LEFT:	
			newHead = {'x' :rectCoor[0]['x'] - 1 ,'y':rectCoor[0]['y']}
		elif direction == RIGHT:
			newHead = {'x' :rectCoor[0]['x'] + 1 ,'y':rectCoor[0]['y'] }
		elif direction == UP:
			newHead = {'x' : rectCoor[0]['x'] ,'y':rectCoor[0]['y'] - 1 }
		elif direction == DOWN:
			newHead = {'x' : rectCoor[0]['x'] ,'y': rectCoor[0]['y'] + 1}
			
		score = len(rectCoor) - 3
		rectCoor.insert(0,newHead)

		if rectCoor[0]['x'] < 0:
			GameOver()
		elif rectCoor[0]['x'] > xcell:
			GameOver()
		elif rectCoor[0]['y'] < 0:
			GameOver()
		elif rectCoor[0]['y'] > ycell:
			GameOver()		

		screen.fill(dimgrey)
		
		if gridParam % 2 != 0:
			draw_grid()
		else:
			pass

		scoreText = scoreFont.render("score: %d" %score, 1,indigo)
		screen.blit(scoreText, (550, 20))
		
		if newHead['x'] == applesCoor[0]['x'] and newHead['y'] == applesCoor[0]['y']:
			applesCoor.append({'x': random.randint(1, xcell-1), 'y': random.randint(1, ycell-1)})
			del applesCoor[0]
		else:
			del rectCoor[-1]

		for i in range (2, len(rectCoor)-1):
			if rectCoor[0]['x'] == rectCoor[i]['x'] and rectCoor[0]['y'] == rectCoor[i]['y']:
				GameOver()
			else:
				pass

		draw_rect(rectCoor, indigo, indigo)
		draw_rect(applesCoor, red, light_red)
		pygame.display.update()
		fps.tick(FPS)

def draw_grid():

	for i in range(xcell+1):
		pygame.draw.line(screen, white, (i*cell_size, 0), (i*cell_size, height), 2)
	for j in range(ycell +1):
		pygame.draw.line(screen, white, (0, j*cell_size), (width, j*cell_size), 2)

def draw_rect(coorLs, color1, color2):

	for coor in coorLs:
		rect = pygame.Rect(coor['x']*cell_size, coor['y']*cell_size, cell_size, cell_size)
		smallRect = pygame.Rect(coor['x']*cell_size + 4, coor['y']*cell_size  +4, cell_size-8, cell_size-8)
		pygame.draw.rect(screen, color1, rect)
		pygame.draw.rect(screen, color2, smallRect)	

def GameOver():

	gameOverText = gameOverFont.render("Game Over!", 1, indigo)
	restartText = restartFont.render("press ENTER to play again", 1, indigo)
	quitText = restartFont.render("press ESC to quit the game", 1, indigo)
	return2M = restartFont.render("press m to go back to the menu", 1, indigo)
	stop = True
	gameOver_rect = gameOverText.get_rect(center=(320, 100))

	while stop:
		screen.blit(gameOverText, gameOver_rect)
		screen.blit(restartText, (150, 160))
		screen.blit(quitText, (150, 220))
		screen.blit(return2M, (150, 270))
		#screen.blit(scoreText, (150, 200))
		#screen.blit(gameOverScoreText,(300, 200) )
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
				elif event.key == K_RETURN:
					runGame(0)
				elif event.key == K_m:
					main()
	
def terminate():
	sys.exit()	
	
if __name__ == "__main__":
	main()   
