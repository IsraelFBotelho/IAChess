import chess as c
from chessboard import display
import pygame as p
import time

board = c.Board('8/1P6/8/5k2/8/3K4/7p/8 w - - 0 1')
display.start(board.fen())
running = True
Move = 'a'
custom = True
runningpromo = True

while running:
    nonError = True
    display.checkForQuit()
    if board.is_game_over():
        result = board.result()
        if 'w' in board.fen():
            if result == "0-1":
                display.start('8/8/2kkkk2/2kqqk2/2kqqk2/2kkkk2/8/8 b - - 0 1')
                time.sleep(4)
            else:
                display.start('8/8/2QqQq2/2qkKQ2/2QKkq2/2qQqQ2/8/8 w - - 0 1')
                time.sleep(4)
        elif 'b' in board.fen():
            if result == "1-0":
                display.start('8/8/2KKKK2/2KQQK2/2KQQK2/2KKKK2/8/8 w - - 0 1')
                time.sleep(4)
            else:
                display.start('8/8/2QqQq2/2qkKQ2/2QKkq2/2qQqQ2/8/8 w - - 0 1')
                time.sleep(4)
        board = c.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        display.start(board.fen())
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False
            display.terminate()
        elif e.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos()
            LocationX = ((location[0]//((400)//8)) - 1)
            LocationY = (location[1]//((400)//8)) - 1

            aux = 8
            for k in range(1,9):
                if LocationY == k:
                    LocationY = aux
                    break
                aux = aux - 1

            letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            aux = 1
            for k in letras:
                if LocationX == aux:
                    LocationX = k
                    nonError = True
                    break
                aux = aux + 1
                nonError = False

            if (LocationY < 1) or (LocationY > 8):
                nonError = False

            if nonError:
                if Move == 'a':
                    Move = LocationX + str(LocationY)
                elif Move != LocationX + str(LocationY):
                    MoveTest = Move + LocationX + str(LocationY)
                    MoveTest = c.Move.from_uci(MoveTest)
                    if MoveTest in board.legal_moves:
                        Move = Move + LocationX + str(LocationY)
                        MoveReg = c.Move.from_uci(Move)
                        board.push(MoveReg)
                        display.start(board.fen())
                        Move = 'a'
                    else:
                        try:
                            MoveReg = Move + LocationX + str(LocationY) + 'q'
                            MoveReg = c.Move.from_uci(MoveReg)
                        except:
                            MoveReg = Move + LocationX + str(LocationY)
                            MoveReg = c.Move.from_uci(MoveReg)
                        else:
                            display.start('7k/8/8/3QB3/3RN3/8/8/K7 w - - 0 1')
                            while runningpromo:
                                if MoveReg in board.legal_moves:
                                    for k in p.event.get():
                                        if k.type == p.MOUSEBUTTONDOWN:
                                            location = p.mouse.get_pos()
                                            LocationX_p = ((location[0] // ((400) // 8)) - 1)
                                            LocationY_p = ((location[1] // ((400) // 8)) - 1)
                                            runningpromo = False
                                            promo_which = str(LocationX_p) + str(LocationY_p)
                                            if promo_which == '44':
                                                MoveReg = Move + LocationX + str(LocationY) + 'q'
                                                MoveReg = c.Move.from_uci(MoveReg)
                                            elif promo_which == '45':
                                                MoveReg = Move + LocationX + str(LocationY) + 'r'
                                                MoveReg = c.Move.from_uci(MoveReg)
                                            elif promo_which == '54':
                                                MoveReg = Move + LocationX + str(LocationY) + 'b'
                                                MoveReg = c.Move.from_uci(MoveReg)
                                            elif promo_which == '55':
                                                MoveReg = Move + LocationX + str(LocationY) + 'n'
                                                MoveReg = c.Move.from_uci(MoveReg)
                                            else:
                                                runningpromo = True
                                else:
                                    runningpromo = False
                        finally:
                            if MoveReg in board.legal_moves:
                                board.push(MoveReg)
                            display.start(board.fen())
                            runningpromo = True

                        Move = 'a'