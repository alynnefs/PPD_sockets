# -*- coding: utf-8 -*- 
import socket
import select
import string
 
def broadcast_data (sock, message):

    # Envia mensagem broadcast para todos os outros clientes para cada dado recebido
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:            
            socket.send(message)

if __name__ == "__main__":

    # Lista para manter a trajetoria dos descritores de socket
    CONNECTION_LIST=[]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen(10)

    # Adiciona o socket do servidor na lista de conexoes legiveis
    CONNECTION_LIST.append(server_socket)

    print("Processo de chat iniciado")

    while 1:
        # Obtem a lista de sockets que estao prontos para serem lidos
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:
            if sock == server_socket: # nova conexao 
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Cliente (%s, %s) conectado" % addr)
                broadcast_data(sockfd, "Cliente (%s, %s) conectado" % addr)

            else:
                # Processa dado recebido por cliente
                try:
                    data = sock.recv(4096)
                except:
                    broadcast_data(sock, "Cliente (%s, %s) esta offline" % addr)
                    print("Cliente (%s, %s) esta offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

                if data:
                    # Processa dados validos de cliente
                    if data == "q" or data == "Q": # finaliza com q ou Q
                        broadcast_data(sock, "Cliente (%s, %s) saiu" % addr)
                        print("Cliente (%s, %s) saiu" % addr)
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                    else:
                        broadcast_data(sock, data)                       
                
    server_socket.close()	

