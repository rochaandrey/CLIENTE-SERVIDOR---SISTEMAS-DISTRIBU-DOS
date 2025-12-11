import socket

def main():
    meuCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    meuCliente.connect(("localhost", 8000))

    mensagem = "Olá mundo distribuído"
    meuCliente.sendall((mensagem + "\n").encode())

    resposta = meuCliente.recv(1024).decode()
    print("Resposta do servidor:", resposta)

    meuCliente.close()


if __name__ == "__main__":
    main()
