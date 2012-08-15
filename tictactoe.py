#!/usr/bin/python

import random
import sys
import time
import os

def _input(bla=''):
    if sys.version_info[0] == 2:
        return raw_input(bla)
    return input(bla)
    
def draw_game(board):
    clear()
    draw_board(board)

def draw_board(b):
    print ' ' +  b[7] + ' | ' + b[8] + ' | ' + b[9]
    print '---|---|---'
    print ' ' + b[4] + ' | ' + b[5] + ' | ' + b[6]
    print '---|---|---'
    print ' ' + b[1] + ' | ' + b[2] + ' | ' + b[3]

def ask_yes(enter_means_yes = True):
    answer = _input()
    if len(answer) == 0 and enter_means_yes:
        return True
    return answer.lower().startswith('y')


def ask_player_letter():
    letter = _input()
    if len(letter) != 1:
        return False
    return letter

def get_first_player():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def ask_player_move(board):
    while True:
        player_move = _input("What is your move? > ")

        if not player_move.isdigit():
            print "This won't work: please pick an available number: ", get_board_empty_slots(board)
        else:
            player_move = int(player_move)
            if player_move in get_board_empty_slots(board):
                return player_move
            print "This space is not free... please pick an available number: ", get_board_empty_slots(board)

def get_board_empty_slots(board):
    slots = []
    i = 0
    for b in board[1:]:
        i += 1
        if b == ' ':
            slots.append(i)
    return slots
        
def is_full(board):
    return len(get_board_empty_slots(board)) == 0

def write_move(board, letter, move):
    board[int(move)] = letter

def is_winner(board, letter):
    b = board
    l = letter
    return ((b[7] == l and b[8] == l and b[9] == l) or  # top
    (b[4] == l and b[5] == l and b[6] == l) or # middle hor.
    (b[1] == l and b[2] == l and b[3] == l) or # bottom
    (b[7] == l and b[4] == l and b[1] == l) or # left
    (b[8] == l and b[5] == l and b[2] == l) or # middle vert.
    (b[9] == l and b[6] == l and b[3] == l) or # right
    (b[1] == l and b[5] == l and b[9] == l) or # cross (slash)
    (b[3] == l and b[5] == l and b[7] == l))   # cross (backslash)

def clear():
    os.system(['clear','cls'][os.name == 'nt'])

def get_comp_move(board, comp_letter, player_letter):

    # can I win?
    empty_slots = get_board_empty_slots(board)

    # can I win?
    for slot in empty_slots:
        testboard = list(board)
        write_move(testboard, comp_letter, slot)
        if is_winner(testboard, comp_letter):
            return slot

    # can I block the oppononent to win?
    for slot in empty_slots:
        testboard = list(board)
        write_move(testboard, player_letter, slot)
        if is_winner(testboard, player_letter):
            return slot

    # try in the corners
    corners = [1, 3, 7, 9]
    random.shuffle(corners)
    for c in corners:
        if c in empty_slots:
            return c

    # try in the center
    if 5 in empty_slots:
        return 5

    # try on the sides
    sides = [2, 4, 6, 8]
    random.shuffle(sides)
    for s in sides:
        if s in empty_slots:
            return s

    sys.stderr.write("I DON'T KNOW WHAT TO DO !")
    return False
    

clear()
print "Welcome to tic tac toe!"
print "-----------------------"

while True:
    print 'What is your letter? X or O (or else?)'
    player_letter = ask_player_letter()
    if player_letter:
        break
    else:
        print "Please, I need a letter..."

if player_letter.lower() == 'o' or \
   player_letter == '0':
    comp_letter = 'X'
else:
    comp_letter = 'O'

print "Computer letter is " + comp_letter
print "Your letter is " + player_letter


while True:

    board = [' '] * 10
    clear()


    # determine who starts first
    if get_first_player() == 'computer':
        turn = 'computer'
        turn = 'player'
    else:
        turn = 'player'

    print ("I decide that %s begins." % turn)
    game_is_running = True
    draw_game(board)
    while game_is_running:

        if is_full(board):
            print "The board is full! It's a tie!"
            game_is_running = False
            break

        if turn == 'player':

            player_move = ask_player_move(board)
            write_move(board, player_letter, player_move)

            draw_game(board)
            print "You decide position " + str(player_move) + ". Nice move!"

            if is_winner(board, player_letter):
                comments.append("You WIN!")
                draw_game(board)
                game_is_running = False
            else:
                turn = 'computer'
        else:
            """ computer's turn"""
            comp_move = get_comp_move(board, comp_letter, player_letter)
            write_move(board, comp_letter, comp_move)

            # pretend the computer had hard time to move
            time.sleep(1)

            draw_game(board)
            print "I decide position " + str(comp_move)

            if is_winner(board, comp_letter):
                print "You loose!"
                game_is_running = False
            else:
                turn = 'player'

    print "Play again? y/n"
    if not ask_yes():
        break
