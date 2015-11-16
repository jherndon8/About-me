import curses
import time
import random

screen = curses.initscr()
dims = screen.getmaxyx()
screen.nodelay(1)

def game():
  row = [0]*dims[1]
  grid = []
  for z in range(dims[0]):
    grid.append(row[:])
  gameover = False
  pl1right = True
  pl1left, pl1up, pl1down = False, False, False
  pl2left = True
  pl2right, pl2up, pl2down = False, False, False
  head1 = [0, 0]
  head2 = [dims[1]-1, dims[0]-2]
  len1, len2 = 5, 5
  pl1act = []
  pl2act = []
  apple1made, apple2made = False, False
  apple1, apple2 = [0, 0], [0, 0]
  while not gameover:
    act = [screen.getch(), screen.getch(), screen.getch(), screen.getch()]
    if ord('\n') in act:
      gameover = True
    for z in act:
      if z == ord('a') or z == ord('s') or z == ord('d') or z == ord('w'):
        pl1act.append(z)
      elif z == ord('j') or z == ord('k') or z == ord('l') or z == ord('i'):
        pl2act.append(z)
    if len(pl1act) > 0:
      if ord('a') == pl1act[0]:
        if not pl1right:
          pl1up, pl1down, pl1right, pl1left = False, False, False, True
        pl1act.remove(pl1act[0])
      elif ord('s') == pl1act[0]:
        if not pl1up:
          pl1up, pl1down, pl1right, pl1left = False, True, False, False
        pl1act.remove(pl1act[0])
      elif ord('d') == pl1act[0]:
        if not pl1left:
          pl1up, pl1down, pl1right, pl1left = False, False, True, False
        pl1act.remove(pl1act[0])
      elif ord('w') == pl1act[0]:
        if not pl1down:
          pl1up, pl1down, pl1right, pl1left = True, False, False, False
        pl1act.remove(pl1act[0])
    if len(pl2act)>0:
      if ord('j') == pl2act[0]:
        if not pl2right:
          pl2up, pl2down, pl2right, pl2left = False, False, False, True
        pl2act.remove(pl2act[0])
      elif ord('k') == pl2act[0]:
        if not pl2up:
          pl2up, pl2down, pl2right, pl2left = False, True, False, False
        pl2act.remove(pl2act[0])
      elif ord('l') == pl2act[0]:
        if not pl2left:
          pl2up, pl2down, pl2right, pl2left = False, False, True, False
        pl2act.remove(pl2act[0])
      elif ord('i') == pl2act[0]:
        if not pl2down:
          pl2up, pl2down, pl2right, pl2left = True, False, False, False
        pl2act.remove(pl2act[0])

    while not apple1made:
      apple1 = [random.randrange(dims[1]), random.randrange(dims[0]-1)]
      if not grid[apple1[1]][apple1[0]]:
        apple1made = True
        grid[apple1[1]][apple1[0]] = -1
    while not apple2made:
      apple2 = [random.randrange(dims[1]), random.randrange(dims[0]-1)]
      if not grid[apple2[1]][apple2[0]]:
        apple2made = True
        grid[apple2[1]][apple2[0]] = -2

    grid[head1[1]][head1[0]]=len1*2-1
    grid[head2[1]][head2[0]]=len2*2
    screen.clear()
    for y in range(dims[0]-1):
      for x in range(dims[1]):
        if grid[y][x] > 0:
          if grid[y][x] % 2:
            screen.addch(y, x, ord('X'))
          else:
            screen.addch(y, x, ord('O'))
          if grid[y][x] == 1:
            grid[y][x] -= 1
          else:
            grid[y][x] -= 2
        elif grid[y][x] < 0:
          if grid[y][x] %2:
            screen.addch(y, x, ord('x'))
          else:
            screen.addch(y, x, ord('o'))
    if pl1right:
      head1[0] += 1
    elif pl1left:
      head1[0] -= 1
    elif pl1up:
      head1[1] -= 1
    elif pl1down:
      head1[1] += 1

    if pl2right:
      head2[0] += 1
    elif pl2left:
      head2[0] -= 1
    elif pl2up:
      head2[1] -= 1
    elif pl2down:
      head2[1] += 1

    if head1[0]<0 or head1[1]<0:
      gameover = True
    if head2[0]<0 or head2[1]<0:
      gameover = True
    if head1[0]>dims[1]-1 or head1[1]>=dims[0]-1:
      gameover = True
    if head2[0]>dims[1]-1 or head2[1]>=dims[0]-1:
      gameover = True
    if not gameover:
      if grid[head1[1]][head1[0]] > 0:
        gameover = True
      if grid[head2[1]][head2[0]] > 0:
        gameover = True
      if grid[head1[1]][head1[0]] == -1:
        apple1made = False
        len1 += 3
      elif grid[head2[1]][head2[0]] == -1:
        apple1made = False
        len2 += 1
      if grid[head1[1]][head1[0]] == -2:
        apple2made = False
        len1 += 1
      elif grid[head2[1]][head2[0]] == -2:
        apple2made = False
        len2 += 3
    screen.refresh()
    time.sleep(0.2)
    


print game()
curses.endwin()