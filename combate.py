# -*- coding: utf-8 -*- 

import socket
import thread
import sys

import pygame, sys
from pygame.locals import *

pygame.init()

displayW = 1100
displayH = 900

cinza = (240, 240, 240)
preto = (0, 0, 0)

font = pygame.font.Font(None, 25)
myfont = pygame.font.SysFont('arial', 25)

screen = pygame.display.set_mode((displayW,displayH),0,32)
screen.fill(cinza)

#teste = pygame.display.set_mode((600,705),0,8)
#teste.fill((255,0,0))

pygame.display.set_caption('combate')

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
            textsurface = myfont.render(recv_data.split(",")[1], True, (255, 0, 0))
            screen.blit(textsurface,(710,405))

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

def desenha_chat(dist, bordaSup, tam):
    pygame.draw.rect(screen, cinza, (dist,bordaSup,tam*3/2,tam))
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*3/2,tam),1)

def protocolo(tipo, msg):
    return "%d," %(tipo)+msg

       
if __name__ == "__main__":
    '''
    sys.argv[1] ip
    sys.argv[2] porta
    '''
    print("Conectando ao servidor em %s:%s"%(sys.argv[1],sys.argv[2]))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((sys.argv[1], int(sys.argv[2])))

    print("Conectado ao servidor em %s:%s"%(sys.argv[1],sys.argv[2]))

    thread.start_new_thread(recv_data,())
    thread.start_new_thread(send_data,())

    name = ""

    #desenha_tabuleiro(25,25,62)
    #desenha_caixa(705,25,62)
    #desenha_botoes(675,590,60)
    #desenha_chat(705,400,248)
    #chat()
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                print("X E Y ",x,y)
                #descobre_peca(x,y)
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

        screen.fill(cinza)
        desenha_chat(705,400,248)
        block = font.render(name, True, (0, 0, 0))
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

