# -*- coding: utf-8 -*- 

import socket
import thread
import sys
import random

import pygame, sys
from pygame.locals import *

pygame.init()

id_jogador = sys.argv[3]

displayW = 1100
displayH = 800

# definição de cores
back = (154,255,208)
vermelho = (225, 0, 0)
verde = (0, 190, 0)
azul = (0, 0, 255)
lago = (0, 220, 220)
branco = (255, 255, 255)
cinza = (240, 240, 240)
preto = (0, 0, 0)

f_chat = pygame.font.Font(None, 25)
f_chat2 = pygame.font.SysFont('arial', 25)

casas = [26,88,150,212,274,336,398,460,522,584]
jogo_inicial = [[[' ']*3 for c in range(10)] for d in range (10)]
 # gera matriz quadrada de ordem 10, cada índice com 3 'argumentos'
jogo_atual = [[[' ']*3 for c in range(10)] for d in range (10)]


screen = pygame.display.set_mode((displayW,displayH),0,32)
screen.fill(cinza)

pygame.display.set_caption('combate: jogador 1') if id_jogador == '1' else pygame.display.set_caption('combate: jogador 2')


####################### COMUNICAÇÃO #######################

def recv_data():
    # Recebe dados de outros clientes conectados ao servidor
    while 1:
        try:
            recv_data = client_socket.recv(4096)            
        except:
            # Gerencia quando o processo do servidor termina
            print("O servidor finalizou a conexão.")
            thread.interrupt_main()
            break
        if not recv_data:
            # Recv sem dados, o servidor fecha a conexão
            print("O servidor finalizou a conexão.")
            thread.interrupt_main()
            break
        elif recv_data.split(",")[0] == '1': # código de mensagem
            print("Dado recebido: ", recv_data)
            textsurface = f_chat.render(recv_data.split(",")[1], True, (255, 0, 0))
            screen.blit(textsurface,(710,405))
            #pygame.display.update() # não mostra sem, quebra quando tem
        elif recv_data.split(",")[0] == '2':
            print "turno: ",recv_data.split(",")[1]

def send_data(msg):
    # Envia dados para outros clientes conectados ao servidor
    while 1:
        if msg.split(",")[1] == "q" or msg.split(",")[1] == "Q": # finaliza com q ou Q
            client_socket.send(msg)
            thread.interrupt_main()
            break
        else:
            client_socket.send(msg)
            break

def protocolo(tipo, msg):
    return "%d," %(tipo)+msg

####################### BACK #######################

def mostraMatriz(matriz):
    for i in range(len(matriz)):
        print '|',
        for j in range(len(matriz)):
            print matriz[i][j][0],
        print '|\n'

def cria_matriz_inicial():
    print "id_jogador: ",id_jogador
    pecas = [['F',1],[1,1],[2,8],[3,5],[4,4],[5,4],[6,4],[7,3],[8,2],[9,1],[10,1],['B',6]]
    pecas2 = [['F',1],[1,1],[2,8],[3,5],[4,4],[5,4],[6,4],[7,3],[8,2],[9,1],[10,1],['B',6]]
    if id_jogador == '1':
        for i in range(4):
            for j in range(10):
                a = random.randint(0,len(pecas)-1)
                jogo_inicial[i][j][0] = pecas[a][0] # código da peça
                pecas[a][1] -= 1
                if pecas[a][1] == 0:
                    pecas.remove(pecas[a])
    elif id_jogador == '2':
        for i in range(6,10):
            for j in range(10):
                a = random.randint(0,len(pecas2)-1)
                jogo_inicial[i][j][0] = pecas2[a][0] # código da peça
                pecas2[a][1] -= 1
                if pecas2[a][1] == 0:
                    pecas2.remove(pecas2[a])
    for i in range(4,6):
        for j in range(2,8):
            if j == 2 or j == 3 or j == 6 or j ==7:
                jogo_inicial[i][j][0] = 'X'

    #mostraMatriz(jogo_inicial)
    valores_matriz()

def valores_matriz(): # adicionar posicao do quadrado
    global jogo_atual
    for i in range(10):
        for j in range(10):
            #jogo_inicial[i][j] = {'label':jogo_inicial[i][j],'posX':casas[i],'posY':casas[i]}
            jogo_inicial[i][j][1] = casas[i]
            jogo_inicial[i][j][2] = casas[j]
    print("inicial")
    mostraMatriz(jogo_inicial)
    jogo_atual = jogo_inicial[:]
    #mostraMatriz(jogo_atual)
    ### para testar reiniciar:
    jogo_atual[1][2],jogo_atual[2][1] = jogo_atual[2][1],jogo_atual[1][2]
    #jogo_atual = jogo_atual[:]
    print("atual")
    mostraMatriz(jogo_atual)

def descobre_quadrado(x,y):
    global jogo_atual
    a = x - ((x-25)%62) + 1
    b = y - ((y-25)%62) + 1
    print "a=",a
    print "b=",b
    if a >= 646 and a <= 832 and b >= 26 and b <= 88: # desistir
        print "desistir"
        send_data('3,q') # tipo comando
    elif a >= 894 and a <= 1018 and b >= 26 and b <= 88: # reiniciar
        print "reiniciar"
        '''
        jogo_atual = jogo_inicial[:]
        desenha_tabuleiro(25,25,62)
        mostraMatriz(jogo_atual)
        #pygame.display.flip()
        '''
    elif a > 25 and a < 585 and b > 25 and b < 585:
        movimentacao(a,b)

peca = ''
def movimentacao(a,b): # ainda nao funciona
    global jogo_atual
    global peca
    pxarray = pygame.PixelArray(screen)
    mostraMatriz(jogo_atual)

    peca = jogo_atual[casas.index(b)][casas.index(a)]# x e y estao invertidos
    print "peça ",peca

    if id_jogador == '1' and b > 25 and b < 213:
        print "territorio preto"
        if pxarray[a, b+60] == 48640 or pxarray[a, b+60] == 15790320:
            print("para baixo")
        
    elif id_jogador == '2' and b > 397 and b < 585:
        print "territorio verde"

####################### INTERFACE #######################

def desenha_chat(dist, bordaSup, tam):
    pygame.draw.rect(screen, cinza, (dist,bordaSup,tam*3/2,tam))
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*3/2,tam),1)

def cor_quadrado(i,j):
    if j < 4:
        return preto
    elif j > 5:
        return verde
    elif j > 3 and j < 6 and i > 1 and i < 4  or i > 5 and i < 8:
        return lago
    else:
        return cinza

def desenha_tabuleiro(dist, bordaSup, tam):
    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, cor_quadrado(i,j), (dist+tam*i,bordaSup+tam*j,tam,tam))
            pygame.draw.rect(screen, branco, (dist+tam*i,bordaSup+tam*j,tam,tam),1)
            #a = jogo_atual[i][j][0]
            cor = branco if id_jogador == '1' else preto
            textsurface = f_chat.render(str(jogo_inicial[j][i][0]), True, cor) # por algum motivo está invertendo
            screen.blit(textsurface,(dist+tam*i+tam/2,bordaSup+tam*j+tam/2))

def desenha_desistir(dist, bordaSup, tam):
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*2,tam),1)
    textsurface = f_chat.render("desistir", True, preto)
    screen.blit(textsurface,(dist+tam/2,bordaSup+tam/2-5))

def desenha_reiniciar(dist, bordaSup, tam):
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*2,tam),1)
    textsurface = f_chat.render("reiniciar", True, preto)
    screen.blit(textsurface,(dist+tam/2,bordaSup+tam/2-5))

####################### MAIN ####################### 
       
if __name__ == "__main__":
    '''
    sys.argv[1] IP
    sys.argv[2] porta
    sys.argv[3] ID
    '''
    print("Conectando ao servidor em %s:%s"%(sys.argv[1],sys.argv[2]))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((sys.argv[1], int(sys.argv[2])))

    print("Conectado ao servidor em %s:%s"%(sys.argv[1],sys.argv[2]))

    thread.start_new_thread(recv_data,())
    thread.start_new_thread(send_data,())

    
    name = ""
    cria_matriz_inicial()
    desenha_tabuleiro(25,25,62)
    desenha_desistir(700,25,75)
    desenha_reiniciar(925,25,75)
    while True:
        key=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                print("X E Y ",x,y)
                descobre_quadrado(x,y)
            elif event.type == KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_RETURN:
                    name = protocolo(1,name) # 1 significa 'tipo mensagem'
                    send_data(name)
                    name = ""
                elif event.key == K_SPACE:
                    name += " "
            elif key[pygame.K_DOWN]:
                print "DOWN"
                '''
                if peca != '' and verifica_baixo():
                    move_baixo()
                '''
            elif key[pygame.K_UP]:
                print "UP"
                '''
                if peca != '' and verifica_cima():
                    move_cima()
                '''
            elif key[pygame.K_LEFT]:
                print "LEFT"
                '''
                if peca != '' and verifica_esquerda():
                    move_esquerda()
                '''
            elif key[pygame.K_RIGHT]:
                print "RIGHT"
                '''
                if peca != '' and verifica_direita():
                    move_direita()
                '''
        pygame.display.update()
        desenha_chat(705,400,248)
        block = f_chat.render(name, True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (905,500)
        screen.blit(block, rect)
        pygame.display.flip()


    try:
        while 1:
            continue
    except:
        print("Programa do jogador encerrado")
        client_socket.close()        

