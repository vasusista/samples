"""
The first player is selected randomly. The user simply has to press the corresponding column number in order to place his counter in that column.
Player 2 represents the AI player, and his token is always represented by an O whereas the player token is represented by X

Inspired by some code from Ahmet Topal
"""


import sys
import random

class Connect4(object):
  def __init__ (self):
    self.rows = 6
    self.cols = 7
    self.empty = '---'
    self.exit = 'exit'
    self.clear = self.rows * self.cols
    self.pos = {
            'n'     : - self.cols,
            'no'    : - (self.cols - 1),
            'o'     : + 1,
            'so'    : + (self.cols + 1),
            's'     : + self.cols,
            'sw'    : + (self.cols - 1),
            'w'     : - 1,
            'nw'    : - (self.cols + 1)
        }
    self.player         = {
            1: {
                
                'counter'    : 'X'
            },
            2: {
                
                'counter'    : 'O'
            }
        }
    self.turn = random.randint(1, 2)
    self.game = []
    self.cols_filled = []
    self.latest = {}
    
  def play(self):
    print("Welcome to Connect 4\n")
    print('You are Player 1 and computer is Player 2.\n')
    print("Your counter is represented by X and the computer's by O")
    for i in range(0, (self.rows * self.cols)):
      self.game.append(self.empty)
    self.startRound()

  def startRound(self):
    #Clearing screen with new lines
    for i in range(0, 50):
      print('\n')
    self.printField()
    if(self.winner()):
      self.nextRound(True)
    if (len(self.cols_filled) == self.cols):
      self.nextRound(False)
    if (self.turn == 2): #Computer's turn
      step = self.makeMove()
    else:
      step = input('-> ')
      while((step.isnumeric() == False) or (step.isnumeric() and (int(step) > self.cols)) or (step.isnumeric() and (int(step) in self.cols_filled))):
        print('Please enter a valid input')
        step = input('-> ')
    step = int(step)
    position = len(self.game) - (self.cols - (step-1))        
    while self.game[position] != self.empty:
      position -= self.cols
    else: #Column is filled
      if position < self.cols:
        self.cols_filled.append(step)           
      self.game[position] = self.player[self.turn]['counter']
    self.latest['player'] = self.turn
    self.latest['position'] = position
    self.changeTurn()
    self.startRound()
      
  def winner(self, latest = {}):
    if len(latest) == 0:
      latest = self.latest
            
    if len(latest) != 2:
      return False
        
        # d1 = diagonal left top to right bottom
        # d2 = diagonal right top to left bottom
        # h = horizontal
        # v = vertical
    possible = {
            'd1'    : {'is': 1, 'check': [self.pos['nw'], self.pos['so']]},
            'd2'    : {'is': 1, 'check': [self.pos['no'], self.pos['sw']]},
            'h'     : {'is': 1, 'check': [self.pos['o'], self.pos['w']]},
            'v'     : {'is': 1, 'check': [self.pos['n'], self.pos['s']]}
        }
    counter = self.player[latest['player']]['counter']
    start = latest['position']
        
    for p in possible:
      for i in possible[p]['check']:
        pos = start + i
        while pos != False and pos >= 0 and pos <= len(self.game)-1 and self.game[pos] == counter:
          possible[p]['is'] += 1
          if p in ['d1', 'd2']:                        
            if (pos+1) % self.cols == 0 or pos % self.cols == 0 or pos >= len(self.game)-self.cols or pos <= self.cols:
              pos = False
            else:
              pos += i
          elif p == 'h':
            if (pos+1) % self.cols == 0 or pos % self.cols == 0:
              pos = False
            else:
              pos += i
          elif p == 'v':
            if pos >= len(self.game)-self.cols or pos <= self.cols:
              pos = False
            else:
              pos += i
               
        if possible[p]['is'] >= 4:
          return True
        
    return False
    
  def makeMove(self):
    percentage_comp = {}
    percentage_player = {}
    for i in range(1, self.cols+1):
      percentage_comp[i] = 0
      percentage_player[i] = 0
      
    if len(self.latest) != 2:
      return (self.cols+1) // 2
        
    win_comp = False
    win_player = False
        
    for step in range(1, self.cols+1):
      if step not in self.cols_filled:
        latest_comp = {}
        latest_player = {}
        position = len(self.game) - (self.cols - (step-1))
        while self.game[position] != self.empty:
          if self.game[position] == self.player[1]['counter']:
            percentage_player[step] += 1
          elif self.game[position] == self.player[2]['counter']:
            percentage_comp[step] += 1
          position -= self.cols
            
        latest_comp['player'] = 2
        latest_comp['position'] = position
        latest_player['player'] = 1
        latest_player['position'] = position
        if self.winner(latest_comp):
          win_comp = step
        if self.winner(latest_player):
          win_player = step
        
    if win_comp != False:
      return win_comp
    if win_player != False:
      return win_player
    sorted_comp = sorted(percentage_comp.items(), key=lambda item: item[1], reverse = True)
    sorted_player = sorted(percentage_player.items(), key=lambda item: item[1], reverse = True)
        
    if sorted_comp[0][1] > sorted_player[0][1]:
      return sorted_comp[0][0]
    elif sorted_comp[0][1] < sorted_player[0][1]:
      return sorted_player[0][0]
    elif sorted_comp[0][1] == sorted_player[0][1]:
      if sorted_comp[0][1] == 0:
        rand = random.randint(1, self.cols)
        while rand in self.cols_filled:
          rand = random.randint(1, self.cols)
        return rand
      else:
        return sorted_comp[0][0]
  
  def changeTurn(self):
    if(self.turn == 1):
      self.turn = 2
    else:
      self.turn = 1
      
      
  def printField(self):        
    line = '|'
    for i in range(0, len(self.game)):
      line += '{0}|'.format(self.game[i].center(len(self.empty), ' '))
      if (i+1) % self.cols == 0:
        print(line)
        line = '|'
        
    cols = '|';
    for i in range(1, self.cols+1):
      cols += '{0}|'.format(str(i).center(len(self.empty), ' '))
        
    print(cols)

  def nextRound(self, winner = False):
    print('---')
    if winner:
      #print('Congrats player {0}, you have won!'.format(self.player[self.latest['player']]['counter']))
      print('Congrats player {0}, you have won!'.format(self.latest['player']))
      sys.exit('Thanks for playing!')
    else:
      print('The round has ended in a tie.')
      sys.exit('Thanks for playing!')
  
a = Connect4()
a.play()