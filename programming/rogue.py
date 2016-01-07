#!/usr/bin/python
import curses
import random
import time

screen = curses.initscr()
curses.start_color()
for i in range(1, 8):
  curses.init_pair(i, i, curses.COLOR_BLACK)
screen.keypad(1)
score = 0
hunger = 50
potions = 1
char=ord('@')
charcolor = 0
steps = 0
d = screen.getmaxyx()
dims = [d[0], d[1]]
dims[0]-=1
curses.noecho()
def makeroom(dims, array, roomsmade, stime):
  d = False
  if roomsmade == 0:
    while not d:
      x, y, h, w = random.randrange(dims[1]-8), random.randrange(dims[0]-5), random.randrange(5, 15), random.randrange(4, 8)
      if x + w <dims[1] and y+h <dims[0]:
        d = True
        for z in range(x+1, x+w):
          for q in range(y+1, y+h):
            array[q][z]=1
        for z in range(x, x+w+1):
          array[y][z]=2
          array[y+h][z]=2
        for q in range(y, y+h):
          array[q][x] = 2
          array[q][x+w] = 2
       
        print x, y, h, w
  else:
    while not d:
      if time.time()-stime>0.25:return None
      spotfound = False
      while not spotfound:
        if time.time()-stime>0.25:return None
        x, y = random.randrange(dims[1]), random.randrange(dims[0])
        if array[y][x] not in [0, 2]:
          spotfound = True
      direction = random.randrange(4)
      spotworks = False
      if direction == 0: #right
        while array[y][x]!=0 and x<dims[1]-1:
          x += 1
        if x<dims[1]-7:
          spotworks = True
      elif direction == 1: #left
        while array[y][x]!=0 and x>0:
          x -= 1
        if x>6:
          spotworks = True
      elif direction ==2: #up
        while array[y][x]!=0 and y>0:
          y -= 1
        if y>4:
          spotworks = True
      elif direction==3:
        while array[y][x]!=0 and y<dims[0]-1:
          y += 1
        if y<dims[0]-10:
          spotworks = True
      if spotworks:
        moved = random.randrange(4, 10)
        for i in range(moved):
          if direction == 0:
            if x<dims[1]-1: x+=1
            else: spotworks=False; break;
          elif direction == 1:
            if x>0: x-=1
            else: spotworks = False;break
          elif direction == 3:
            if y<dims[1]-1: y+=1
            else: spotworks=False;break
          elif direction == 2:
            if y>0: y-=1
            else: spotworks = False;break
          if array[y][x] not in [0, 3]: spotworks=False; break
      if spotworks:
        if direction<2:
          yp = random.randrange(2, 6)
          ym = random.randrange(2, 6)
          xp = random.randrange(4, 20)*(-2*(direction)+1)
          if xp<0: xm=-xp; xp=0
          else: xm=0
          for q in range(y-ym-1, y+yp+1):
            if spotworks==False: break
            for z in range(x-xm, x+xp+1):
              if q in range(dims[0])[1:-1] and z in range(dims[1])[5:-5]:
                if array[q][z]!=0: spotworks=False
		break
              else:
                spotworks = False
                break
        else:
          xp = random.randrange(2, 10)
          xm = random.randrange(2, 10)
          yp = random.randrange(4, 10)*(2*(direction-2)-1)
          if yp<0: ym=-yp; yp=0
          else: ym = 0
          for q in range(y-ym, y+yp+1):
            if spotworks==False: break
            for z in range(x-xm, x+xp+5):
              if q in range(dims[0])[5:-5] and z in range(dims[1])[5:-5]:
                if array[q][z]!=0: spotworks=False
		break
              else:
                spotworks = False
                break
        for z in range(x-xm-1, x+xp+2):
          if z not in range(dims[1]): spotworks = False
      if spotworks:
        for z in range(x-xm, x+xp+1):
          if not spotworks: break
          for q in range(y-ym, y+yp+1):
            if array[q][z]!=0: spotworks=False; break
      if spotworks:
        print x, xm, xp, y, ym, yp
        for z in range(x-xm+1, x+xp):
          for q in range(y-ym+1, y+yp):
            try:
              array[q][z]=1
            except: print q, z 
        for z in range(x-xm, x+xp):
          array[y-ym][z]=2
          array[y+yp][z]=2
        for q in range(y-ym, y+yp):
          array[q][x-xm] = 2
          array[q][x+xp] = 2
        array[y+yp][x+xp]= 2
        for q in range(moved+2):
          if direction==0:
            array[y][x-q]=3
          elif direction==1:
            array[y][x+q]=3
          elif direction == 2:
            array[y+q][x]=3
          else:
            array[y-q][x]=3
        d=True
  return array
        

  

def get_rand_dungeon(dims):
  num_of_rooms = random.randrange(6, 9)
  #num_of_rooms=3
  row = [0]*dims[1]
  array = []
  for r in range(dims[0]):
    array.append(row[:])
  roomsmade = 0
  while roomsmade < num_of_rooms:
    array = makeroom(dims, array, roomsmade, time.time())
    if array == None:
      return get_rand_dungeon(dims)
    roomsmade += 1
  return array


def playlevel():
  global steps, potions, hunger, score
  batteries = 10
  message = ' '*20
  screen.clear()
  screen.addstr(dims[0]/2, dims[1]/2-5, 'Loading...')
  screen.refresh()
  level = get_rand_dungeon(dims)
  coins = random.randrange(15, 25)
  qblock = random.randrange(3, 8)
  nobatteries = random.randrange(2)
  nojackpot = random.randrange(5)
  nopotion = random.randrange(10)
  c = 0
  pmade, jmade, bmade, cmade, emade = False, False, False, False, False
  if nobatteries: bmade = 1
  if nojackpot: jmade = 1
  if nopotion: pmade = 1
  c1 = []
  c2 = []
  for y in range(dims[0]):
    for x in range(dims[1]):
      if level[y][x] == 1:
        c1.append([y, x])
      elif level[y][x] == 2:
        c2.append([y, x])
  bac =  c1
  for i in range(coins):
    a = c1[random.randrange( len(c1) )]
    level[a[0]][a[1]] = 5
    c1.remove(a)
  for i in range(qblock):
    b = random.randrange(4)
    a = c1[random.randrange( len(c1) )]
    if not b: level[a[0]][a[1]]=10
    else: level[a[0]][a[1]]=9
  if not pmade:
    a = c1[random.randrange(len(c1))]
    level[a[0]][a[1]] = 6
    c1.remove(a)
  if not jmade:
    a = c1[random.randrange(len(c1))]
    level[a[0]][a[1]] = 7
    c1.remove(a)
  if not bmade:
    a = c1[random.randrange(len(c1))]
    level[a[0]][a[1]] = 8
    c1.remove(a)
  while not emade:
    trial = c2[random.randrange(len(c2))]
    t = []
    if trial[0]>0:t.append(level[trial[0]-1][trial[1]])
    if trial[0]<dims[0]-1: t.append(level[trial[0]+1][trial[1]])
    if trial[1]>0:t.append(level[trial[0]][trial[1]-1])
    if trial[1]<dims[1]-1: t.append(level[trial[0]][trial[1]+1])
    if 1 in t: level[trial[0]][trial[1]] = 4; emade = True
    else: c2.remove(trial)
  graphics = [ord(' '), ord('.'), ord('#'), ord('+'), ord('E')|curses.color_pair(curses.COLOR_RED)|curses.A_BOLD, ord('o')|curses.color_pair(curses.COLOR_YELLOW)|curses.A_BOLD, ord('Y')|curses.color_pair(curses.COLOR_CYAN), ord('$')|curses.color_pair(curses.COLOR_GREEN), ord('B')|curses.color_pair(curses.COLOR_BLUE), ord('?'), ord('?')]
  action = -1
  place = [0,0]
  while level[place[0]][place[1]]!=1:
    place = c1[random.randrange(len(c1))]
  screen.clear()
  gameover=False

  while action not in [ord('q'), ord('n'), 27, ord('m')]:


    if not batteries: screen.clear()
    movement = False
    for i in [[place[0]-1, place[1]-1],[place[0]-1, place[1]], [place[0]-1, place[1]+1], [place[0], place[1]-1], [place[0], place[1]+1], [place[0]+1, place[1]-1], [place[0]+1, place[1]], [place[0]+1, place[1]+1]]:
      if i[0] in range(dims[0]) and i[1] in range(dims[1]):
        screen.addch(i[0], i[1], graphics[level[i[0]][i[1]]])
    screen.addch(place[0], place[1], char, curses.color_pair(charcolor))
    screen.addstr(dims[0], 0, 'Score: '+str(score))
    for i in range(3):
      if potions>i:
        screen.addch(dims[0], 13+i, ord('Y')|curses.color_pair(curses.COLOR_CYAN))
      else:
        screen.addch(dims[0], 13+i, ord(' '))
    screen.addstr(dims[0], 16, 'Battery')
    for i in range(10):
      if batteries > i:
        screen.addch(dims[0], 23+i, ord(' ') | curses.A_REVERSE)
      else:
        screen.addch(dims[0], 23+i, ord(' '))
    if hunger<=5: hungercolor=curses.COLOR_RED
    else: hungercolor = 0
    screen.addstr(dims[0], 35, 'Hunger:' + str(hunger)+' '*2, curses.color_pair(hungercolor))
    while len(message)<32: message+=' '
    screen.addstr(dims[0], dims[1]-33, message)
    if gameover:
      for r in range(dims[0]):
        for y in range(dims[1]):
          if r<dims[0]-1 or y<dims[1]-1:
            screen.addch(r, y, graphics[level[r][y]])
      screen.addstr(dims[0]/2-1, dims[1]/2-13, 'Press M to go to the menu', curses.A_REVERSE)
      screen.addstr(dims[0]/2+1, dims[1]/2-8, 'Press Q to quit', curses.A_REVERSE)
    screen.move(dims[0], dims[1]-1)
    screen.refresh()
    message = ' '*32


    action = screen.getch()
    if gameover:
      while action not in [ord('m'), ord('q')]:
        action = screen.getch()
    if action in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
      screen.addch(place[0], place[1], graphics[level[place[0]][place[1]]])
    if action == curses.KEY_UP and level[place[0]-1][place[1]] in [1, 3, 4, 5, 6, 7, 8, 9, 10]:
      place[0] -= 1; steps +=1;movement=True
    elif action == curses.KEY_DOWN and level[place[0]+1][place[1]] in [1, 3, 4, 5, 6, 7, 8, 9, 10]:
      place[0] += 1; steps +=1; movement=True
    elif action == curses.KEY_LEFT and level[place[0]][place[1]-1] in [1, 3, 4, 5, 6, 7, 8, 9, 10]:
      place[1] -= 1; steps +=1; movement= True
    elif action == curses.KEY_RIGHT and level[place[0]][place[1]+1] in [1, 3, 4, 5, 6, 7, 8, 9, 10]:
      place[1] += 1; steps +=1;movement=True
    elif action == ord('l'):
      if potions>0:
        for r in range(dims[0]):
          for y in range(dims[1]):
            if r<dims[0]-1 or y<dims[1]-1:
              screen.addch(r, y, graphics[level[r][y]])
        potions -= 1
        batteries = 1000
    elif action == ord('n'):
      if level[place[0]][place[1]]!=4:
        action = -1
    if level[place[0]][place[1]] == 4:
      message = 'Press n to go to the next level'
    elif level[place[0]][place[1]] == 5:
      level[place[0]][place[1]] = 1
      score += 10
    elif level[place[0]][place[1]] == 6:
      level[place[0]][place[1]] = 1
      if potions<3: potions+=1
    elif level[place[0]][place[1]] == 7:
      level[place[0]][place[1]] = 1
      score += 500
    elif level[place[0]][place[1]] == 8:
      level[place[0]][place[1]] = 1
      batteries += 10
    elif level[place[0]][place[1]] == 9:
      message = 'Press Space to eat ?'
      if action == ord(' '):
        level[place[0]][place[1]] = 1
        hunger += 5
        message = '5 hunger restored'
    elif level[place[0]][place[1]] == 10:
      message = 'Press Space to eat ?'
      if action == ord(' '):
        level[place[0]][place[1]] = 1
        message = 'You died of poison'
        gameover=True
    if movement and not steps%20 and batteries>0: batteries -= 1
    if movement and not steps%13: hunger -= 1
    if hunger<=0: gameover=True; message = 'You died of hunger'
        
  if action ==ord('n'): playlevel()
  elif action == ord('m'): menu()

#playlevel()

def menu():
  global hunger, score, potions
  hunger = 50
  score = 0
  potions = 1
  screen.clear()
  selection = -1
  option = 0
  options = ['Play', 'Select Character', 'Instructions', 'Quit']
  screen.addstr(0, dims[1]/2-4, 'Roguelike')
  screen.addstr(1, dims[1]/2-6, 'By JT Herndon')
  while selection<0:
    graphics = [0]*len(options)
    graphics[option] = curses.A_BOLD
    for i in range(len(options)):
      screen.addstr(dims[0]/2-len(options)/2+i, dims[1]/2-len(options[i])/2, options[i], graphics[i])
    screen.refresh()
    action = screen.getch()
    if action == curses.KEY_UP:
      option = (option-1)%len(options)
    elif action == curses.KEY_DOWN:
      option = (option+1)%len(options)
    elif action == ord('\n'):
      selection = option
  if selection == 0:
    playlevel()
  elif selection == 1:
    getchar()

def getchar():
  global char, charcolor
  selection=-1
  option1=0
  option2=0
  screen.clear()
  while selection<2:
    screen.addch(dims[0]/2-4, dims[1]/2, char, curses.color_pair(charcolor))
    characters = [ord('@'), ord('&'), ord('O'), ord('X'), ord('*'), ord('8'), ord('|'), ord('Q')]
    screen.addstr(dims[0]/2-2, dims[1]/2-2, 'Icon:')
    for i in range(len(characters)):
      if option1==0 and option2==i:
        screen.addch(dims[0]/2-1, dims[1]/2-len(characters)/2+i, characters[i], curses.color_pair(charcolor)|curses.A_BOLD)
      else:
        screen.addch(dims[0]/2-1, dims[1]/2-len(characters)/2+i, characters[i], curses.color_pair(charcolor))
    screen.addstr(dims[0]/2+1, dims[1]/2-3, 'Color:')
    for i in range(7):
      if option1==1 and option2==i:
        screen.addch(dims[0]/2+2, dims[1]/2-3+i, char, curses.color_pair(i)|curses.A_BOLD)
      else:
        screen.addch(dims[0]/2+2, dims[1]/2-3+i, char, curses.color_pair(i))
    if option1==2:
      screen.addstr(dims[0]/2+4, dims[1]/2-2, 'Back', curses.A_BOLD)
    else:
      screen.addstr(dims[0]/2+4, dims[1]/2-2, 'Back')
    screen.refresh()
    action = screen.getch()
    if action == curses.KEY_UP:
      option1= (option1-1)%3
    elif action == curses.KEY_DOWN:
      option1 = (option1+1)%3
    elif action == curses.KEY_LEFT:
      if option1==0:
        option2=(option2-1)%8
      elif option1==1:
        option2=(option2-1)%7
    elif action == curses.KEY_RIGHT:
      if option1==0:
        option2=(option2+1)%8
      elif option1==1:
        option2=(option2+1)%7
    elif action == ord('\n'):
      selection = option1
    if option1==1 and option2>=7: option2=6
    if selection==0:
      selection=-1
      char = characters[option2]
    elif selection==1:
      selection=-1
      charcolor=option2    
  menu()

menu()
curses.endwin()

