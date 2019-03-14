import random
import math
# required libraries

verbose = False  # debug command to help track down issues and see some more information during construction
count = 1  # how many grids to produce
size = 16 # how large (both height and width) the grid should be

# a function to print a grid (2d list) in a human readable way
def gridPrint(grid): 
  for i in range(len(grid)):
    print(grid[i])
  print()

# the box object represents the boxes in the sudoku grid,
class Box:
  # the raw box coords of the box, not the grid coords
  def __init__(self,coords):
    self.coords = coords
  # a pretty print function that lists the information of the cell
  def pp(self):
    for i in range(len(coords)):
      print(self.coords[i]," ",end="")
    print()

# a function that uses Unicode border characters to make a sudoku grid (this depends on the actual font of the terminal
# and is not great in some fonts because border characters are not handled great).
def sudokuGridPrint(grid,size,hsize,vsize):  
  charspace = len(str(len(grid)))
  for i in range(2*size+1):
    if i == 0:
      print("┏",end="")
    elif i == 2*size:
      print("┓",end="")
    elif i%2 == 0:
      if i%(int(size/vsize)*2) == 0:
        print("┳",end="")
      else:
        print("┯",end="")
    else:
      for j in range(charspace):
        print("━",end="")
  print()
  for i in range(2*size-1):
    for j in range(2*size+1):
      if i%2 == 0:
        if j%2 == 0:
          if j%(int(size/vsize)*2) == 0:
            print("┃",end="")
          else:
            print("│",end="")
        else:
          target = grid[i//2][(j-1)//2]
          numlen = len(str(target))
          if target == 0:
            for k in range(charspace):
              print(" ",end="")
          else:
            for k in range(numlen,charspace):
              print("0",end="")
            print(target,end="")
      else:
        if j == 0:
          if (i+1)%(int(size/hsize)*2) == 0:
            print("┣",end="")
          else:
            print("┠",end="")
        elif j == 2*size:
          if (i+1)%(int(size/hsize)*2) == 0:
            print("┫",end="")
          else:
            print("┨",end="")
        elif j%2 == 0:
          if j%(int(size/vsize)*2) == 0:
            if (i+1)%(int(size/hsize)*2) == 0:
              print("╋",end="")
            else:
              print("╂",end="")
          else:
            if (i+1)%(int(size/hsize)*2) == 0:
              print("┿",end="")
            else:
              print("┼",end="")
        else:
          if (i+1)%(int(size/hsize)*2) == 0:
            for k in range(charspace):
              print("━",end="")
          else:
            for k in range(charspace):
              print("─",end="")
    print()
  for i in range(2*size+1):
    if i == 0:
      print("┗",end="")
    elif i == 2*size:
      print("┛",end="")
    elif i%2 == 0:
      if i%vsize == 0:
        print("┻",end="")
      else:
        print("┷",end="")
    else:
      for j in range(charspace):
        print("━",end="")
  print()
    

masterRow = []
for j in range(size):
  masterRow.append(j+1)

boxes = []

if math.sqrt(size).is_integer():
  hsize = int(math.sqrt(size))
  vsize = int(math.sqrt(size))
else:
  factors = []
  for i in range(1,size+1):
    if size % i == 0:
      factors.append(i)
  factors.pop(0)
  factors.pop()
  if len(factors) == 0:
    print("Cannot create boxes currently, size is prime")
    exit()
  else:
    randind = random.randint(0,len(factors)-1)
    hsize = factors[randind]
    vsize = int(size/hsize)


for i in range(hsize):
  for j in range(vsize):
    coords = []
    for k in range(vsize):
      for l in range(hsize):
        coords.append((i*vsize+k,j*hsize+l))
    boxes.append(Box(coords))

def findBox(row,column,boxes):
  target = (row,column)
  for box in boxes:
    for coord in box.coords:
      if coord == target:
        return box
  raise ValueError("failed to find box",row,column)
  exit()

def findValidValues(row,column,grid,boxes):
  ret = masterRow.copy()
  box = findBox(row,column,boxes)
  for coord in box.coords:
    try:
      ret.remove(grid[coord[0]][coord[1]])
    except:
      pass
  for i in range(len(grid)):
    try:
      ret.remove(grid[row][i])
    except:
      pass
  for j in range(len(grid)):
    try:
      ret.remove(grid[j][column])
    except:
      pass
  return ret

def validate(grid,boxes):
  for i in range(len(grid)):
    for j in range(len(grid)):
      if grid[i][j] == 0:
          pass
      else:
        box = findBox(i,j,boxes)
        for coord in box.coords:
          if coord != (i,j) and grid[coord[0]][coord[1]] == grid[i][j]:
            print("BOX ERROR",i,j," ",coord[0],coord[1])
            print(grid[coord[0]][coord[1]],grid[i][j])
            return False
        for k in range(len(grid)):
          if (i,k) != (i,j) and grid[i][k] == grid[i][j]:
            print("ROW ERROR",i,k)
            return False
          if (k,j) != (i,j) and grid[k][j] == grid[i][j]:
            print("COLUMN ERROR",k,j)
            return False
  return True

def swapValues(grid):
  roster = masterRow.copy()
  vals = []
  for i in range(2):
    randind = random.randint(0,len(roster)-1)
    vals.append(roster.pop(randind))
  replace = {vals[0]:vals[1],vals[1]:vals[0]}
  for i in range(len(grid)):
    for j in range(len(grid)):
      if grid[i][j] in replace:
        grid[i][j] = replace[grid[i][j]]
  return grid

def swapColumns(grid):
  posCols = list(range(hsize))
  posStacks = list(range(vsize))
  randind = random.randint(0,len(posStacks)-1)
  stack = posStacks.pop(randind)
  cols = []
  for i in range(2):
    randind = random.randint(0,len(posCols)-1)
    cols.append(posCols.pop(randind))
  temp = 0
  for i in range(size):
    temp = (grid[i][stack*hsize+cols[0]])
    grid[i][stack*hsize+cols[0]] = grid[i][stack*hsize+cols[1]]
    grid[i][stack*hsize+cols[1]] = temp
  return grid

def swapRows(grid):
  posRows = list(range(vsize))
  posBands = list(range(hsize))
  randind = random.randint(0,len(posBands)-1)
  band = posBands.pop(randind)
  rows = []
  for i in range(2):
    randind = random.randint(0,len(posRows)-1)
    rows.append(posRows.pop(randind))
  temp = 0
  for i in range(size):
    temp = (grid[band*vsize+rows[0]][i])
    grid[band*vsize+rows[0]][i] = grid[band*vsize+rows[1]][i]
    grid[band*vsize+rows[1]][i] = temp
  return grid

def swapStacks(grid):
  posStacks = list(range(vsize))
  stacks = []
  for i in range(2):
    randind = random.randint(0,len(posStacks)-1)
    stacks.append(posStacks.pop(randind))
  temp = 0
  for i in range(size):
    for j in range(hsize):
      temp = (grid[i][stacks[0]*hsize+j])
      grid[i][stacks[0]*hsize+j] = grid[i][stacks[1]*hsize+j]
      grid[i][stacks[1]*hsize+j] = temp
  return grid

def swapBands(grid):
  posBands = list(range(hsize))
  bands = []
  for i in range(2):
    randind = random.randint(0,len(posBands)-1)
    bands.append(posBands.pop(randind))
  temp = 0
  for i in range(size):
    for j in range(vsize):
      temp = (grid[bands[0]*vsize+j][i])
      grid[bands[0]*vsize+j][i] = grid[bands[1]*vsize+j][i]
      grid[bands[1]*vsize+j][i] = temp
  return grid

def rotate(grid):
  if hsize != vsize:
    angle = 1
  else:
    angle = random.randint(1,3)
  if angle == 0: # rotate 90 degrees
    for i in range(int(size/2)):
      for j in range(i,size-i-1):
        temp = grid[i][j]
        grid[i][j] = grid[size-1-j][i]
        grid[size-1-j][i] = grid[size-1-i][size-1-j]
        grid[size-1-i][size-1-j] = grid[j][size-1-i]
        grid[j][size-1-i] = temp
  elif angle == 1: # rotate 180 degrees
    for i in range(size):
      for j in range(int(size/2)):
        temp = grid[i][j]
        grid[i][j] = grid[size-1-i][size-1-j]
        grid[size-1-i][size-1-j] = temp
  else: # rotate 270 degrees
    for i in range(int(size/2)):
      for j in range(i,size-i-1):
        temp = grid[i][j]
        grid[i][j] = grid[j][size-1-i]
        grid[j][size-1-i] = grid[size-1-i][size-1-j]
        grid[size-1-i][size-1-j] = grid[size-1-j][i]
        grid[size-1-j][i] = temp
  return grid

def reflect(grid):
  axis = random.randint(0,1)
  if axis == 0: # flip over horizantal axis
    for i in range(int(size/2)):
      for j in range(size):
        temp = grid[i][j]
        grid[i][j] = grid[size-1-i][j]
        grid[size-1-i][j] = temp
  else: # flip over vertical axis
    for i in range(size):
      for j in range(int(size/2)):
        temp = grid[i][j]
        grid[i][j] = grid[i][size-1-j]
        grid[i][size-1-j] = temp
  return grid

def updatePossible(row,column,possibles,grid,boxes):
  rbox = findBox(row,column,boxes)
  for coord in rbox.coords:
    possibles[coord[0]][coord[1]] = findValidValues(coord[0],coord[1],grid,boxes)
  for i in range(len(possibles)):
    possibles[row][i] = findValidValues(row,i,grid,boxes)
    possibles[i][column] = findValidValues(i,column,grid,boxes)
  return possibles
  
def makeGrid():
  grid = []
  for i in range(size):
    grid.append([])
  roster = masterRow.copy()
  firstRow = []
  while len(roster) > 0:
    randind = random.randint(0,len(roster)-1)
    firstRow.append(roster.pop(randind))
  blocks = []
  for i in range(vsize):
    block = firstRow[0+i*hsize:((i+1)*hsize)]
    blocks.append(block)
  for i in range(vsize):
    for j in range(len(blocks)):
      tblock = blocks[j+i-len(blocks)].copy()
      rblock = []
      while len(tblock) > 0:
        randind = random.randint(0,len(tblock)-1)
        rblock.append(tblock.pop(randind))
      grid[i] += rblock
  vblocks = []
  for i in range(vsize):
    group = []
    for j in range(hsize):
      vblock = []
      for k in range(vsize):
        vblock.append(grid[k][i*hsize+j])
      group.append(vblock)
    vblocks.append(group)
  for i in range(vsize,size):
    for j in range(size):
      result = vblocks[j//hsize][j%hsize+(i//vsize)-hsize][i%vsize]
      grid[i].append(result)
  
  #sudokuGridPrint(grid,size,hsize,vsize)

  numTransforms = random.randint(2*size,5*size)

  for i in range(numTransforms):
    randind = random.randint(0,6)
    if randind == 0:
      grid = swapValues(grid)
    elif randind == 1:
      grid = swapColumns(grid)
    elif randind == 2:
      grid = swapRows(grid)
    elif randind == 3:
      grid = swapStacks(grid)
    elif randind == 4:
      grid = swapBands(grid)
    elif randind == 5:
      pass
      #grid = rotate(grid)
    else:
      grid = reflect(grid)
  
  return grid

def checkUnique(grid,boxes):
  possibles = []
  for i in range(size):
    for j in range(size):
      if grid[i][j] == 0:
        result = findValidValues(i,j,grid,boxes)
        if result == []:
          return False
        possibles.append((i,j,result))

  solution = []
  mark = []
  step = 0
  solutionsFound = 0
  while solutionsFound < 2 :
    row = possibles[step][0]
    column = possibles[step][1]
    choices = possibles[step][2]

    if len(mark) < step+1:
      mark.append([])
    if len(mark[step]) == len(choices):
      mark[step] = []
      step -= 1
      if step < 0:
        if solutionsFound == 1:
          return True
        else:
          return False
      else:
        continue

    for i in range(len(choices)):
      if choices[i] not in mark[step]:
        choice = choices[i]
        mark[step].append(choice)
    solution.append(choice)

    attempt = grid.copy()
    attempt[row][column] = choice

    if validate(attempt,boxes):
      step += 1

    if len(solution) == len(possibles):
      step -=1
      solutionsFound += 1

  return True

def makePuzzle(grid,boxes):
  # try removing random values until the puzzle not unique or impossible then return the still valid solution

  stay = True

  while stay:
    while True:
      randrow = random.randint(0,size-1)
      randcol = random.randint(0,size-1)
      if grid[randrow][randcol] != 0:
        break

    val = grid[randrow][randcol]
    grid[randrow][randcol] = 0

    if not checkUnique(grid,boxes):
      stay = False
      grid[randrow][randcol] = val

  return grid
  
solutions = []
for i in range(count):
  solutions.append(makeGrid())

#puzzles = []
#for i in range(count):
  #puzzles.append(makePuzzle(solutions[i],boxes))

print("Done!")
for i in range(count):
  #print("Puzzle:")
  print("Box size: ",hsize," x ",vsize)
  #if not validate(puzzles[i],boxes):
    #print("ERROR WITH PUZZLE")
  #sudokuGridPrint(puzzles[i],size,hsize,vsize)
  print("Solution:")
  if not validate(solutions[i],boxes):
    print("ERROR WITH SOLUTION")
  sudokuGridPrint(solutions[i],size,hsize,vsize)

