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
        else:
            print("Dado recebido: ", recv_data)

def send_data(msg):
    # Envia dados para outros clientes conectados ao servidor
    while 1:
        if msg == "q" or msg == "Q": # finaliza com q ou Q
            client_socket.send(msg)
            thread.interrupt_main()
            break
        else:
            client_socket.send(msg)
            break

def desenha_chat(dist, bordaSup, tam):
    pygame.draw.rect(screen, cinza, (dist,bordaSup,tam*3/2,tam))
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*3/2,tam),1)

       
if __name__ == "__main__":

    print("Conectando ao servidor em 127.0.0.1:5000")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5000))

    print("Conectado ao servidor em 127.0.0.1:5000")

    thread.start_new_thread(recv_data,())
    thread.start_new_thread(send_data,())

    font = pygame.font.Font(None, 25)
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
                    print(name)
                    send_data(name)
                    name = ""
                elif event.key == K_SPACE:
                    name += " "

        screen.fill (cinza)
        desenha_chat(705,400,248)
        block = font.render(name, True, (0, 0, 0))
        rect = block.get_rect()
        #rect.center = screen.get_rect().center
        rect.center = (905,500)
        screen.blit(block, rect)
        pygame.display.flip()
        #pygame.display.update()

    try:
        while 1:
            continue
    except:
        print("Programa do jogador encerrado")
        client_socket.close()        

