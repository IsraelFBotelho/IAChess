import chess as c
from chessboard import display
import pygame as p
import time


#    Na primeira parte do código temos além de declarações de variaveis que serão usadas para os 'whiles' temos
#    também o inicio do tabuleiro com o 'c.Board', esse tabuleiro e as variações da biblioteca de onde ele vem,
#    retorna um valor de FEN(Forsyth–Edwards Notation),que por vez é 'printado' com o display.start


board = c.Board()
display.start(board.fen())
running = True
Move = 'a'
custom = True
runningpromo = True


#    'running', essa variavel faz basicamente o que ela propões, ela é o que mantem o jogo em laço, portanto pra fecha o jogo,
#    basicamente tem um evento pra 'QUIT' que se for verdade fecha, da mesma forma tem um outro momento onde o jogo é verdade
#    que é no evento de clicar com o mouse ele entra no 'MOUSEBUTTONDOWN' e com isso ele pega a posição do mouse e entrega um valor
#    dividido por 400 que é o tamanho da tela do jogo.

#    Além dessa parte fundamental esse começo tem uma parte conclusiva, claro que inicialmente não é ativa mas, que define o fim da rodada do jogo,
#    então ela que 'identifica' o 'game over'


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


#    Bom, agora temos em numeros onde o mouse foi clicado certo? Mas e se ele clicar fora do grid, ou se ele clicar no grid
#    como ver a posição em coordenadas de xadrez (UCI), bom, então o mais facil, o Z do mouse ja é um numero tanto no UCI tanto
#    no 'input', ou seja só invertelo, afinal um 8 no input por conta de ser uma visão das brancas, é 1 e o 1 é 8, sim ele conta
#    de cima pra baixo, depois disso só resta o X, eu coloco uma lista de letras e faço um contador, quando o contador chega no valor,
#    ele troca pela letra atual.
    
#    Mas também tem o caso de e se ele clicar fora do board, o mouse ainda pega e pode complicar não?
#    Bem... Sim, e é por isso que nos 2 casos, se ele nao entrar nos for que organizam a variavel 'nonError' age, se ele nao passa
#    pelos pontos de organização ela fica falsa e para a proxima parte nem mesmo entra.


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


#    Bom agora que temos a coordenada do quadrado do tabuleiro, nos resta cuidar de vericar se tem um movimento, se ele é
#    possivel e se for, mover. Para isso sabemos que um codigo UCI completo não possui apenas uma unica coordenada, ele possui
#    uma casa de saida, uma ída e se for promoção uma letra a mais que indica a peça que se tornará, então clicando uma unica vez
#    não tem por que verificar se tem movimento, afinal ele só foi feito parcialmente, entra também nesse caso, se o movimento vai
#    de uma casa pra ela mesma.
#    Ok, não é o primeiro 'click' e não é para a mesma casa, nesse caso vamos verificar se ele existe com o 'board.legal_moves',
#    assim como o nome indica ele vai ver se numa biblioteca de movimentos a partir dali tem como se mover, isso claro levando
#    em conta todos as condições do tabuleiro, inclusive se está sobre 'check'

#    Uma breve explicação sobre as variaveis aqui:
#    -Move: ela armazena a primeira coordenada, ou seja de onde ta vindo a peça, caso ainda não tenha nada porquê o codigo acabou de começa
#    ou porquê o codigo acabou de realizar um movimento, ela vai estar com a letra 'a', que serve apenas para não entrar na parte que realiza o movimento
#    -MoveTes e MoveReg: Meio identicos, mas um pega o Move e as coordenadas novas e testa, enquanto o outro se o teste for valido realiza a jogada
#    -Variaveis promo ou _p: Fazem o mesmo que fora no codigo completo, mas que somente funcionam ali e é exclusivo para identificar a transformação da peça


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


#    Hmm, ok, o movimento aparentemente não existe, certo? mas ainda assim, queria testa um caso em específico
#    em codigo UCI, o movimento de um peão que vai para a promoção é invalido apenas com os numeros da casa, então e se esse movimento
#    invalido na verdade for um peão indo a promoção, nesse caso só nos resta testar
#    uma estrutura 'try' 'except' vai nos fornecer isso, claro junto com o texte nos 'legal_moves'


                    else:
                        try:
                            MoveReg = Move + LocationX + str(LocationY) + 'q'
                            MoveReg = c.Move.from_uci(MoveReg)
                        except:
                            MoveReg = Move + LocationX + str(LocationY)
                            MoveReg = c.Move.from_uci(MoveReg)
                        else:


#    A promoção então existe, afinal passou pelo 'try', beleza, então vamos ver qual peça o usuario quer.
#    Para isso vamos colocar uma tela somente com as 4 possibilidades na tela e fazer ele clicar lá, quando isso acontecer
#    o mouse vai nos retornar valores de X e Y, e com a mesma logica anterior, so que sem converter para UCI vamos ver qual é.

#    Tendo a coordenada, e ela sendo uma das que é uma opção da promoção, entao o loop se encerra e vamos ao 'Finally'


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


#    Sendo possivel ou não o codigo passa por aqui e se os clicks finais com a promoção forem possiveis, então ele é realizado
#    Caso não o codigo somente reseta e volta pro começo do 'while running'


                            if MoveReg in board.legal_moves:
                                board.push(MoveReg)
                            display.start(board.fen())
                            runningpromo = True

                        Move = 'a'