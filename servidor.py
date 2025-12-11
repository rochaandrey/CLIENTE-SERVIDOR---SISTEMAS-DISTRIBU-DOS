import socket
import threading

def inverter_string(var):
    return var[::-1]

def handle_client(conn, addr):
    print("Nova conexão: {}".format(addr))

    data = conn.recv(1024).decode()
    data = data.rstrip("\n")
    print("Recebido do cliente: {}".format(data))

    resposta = inverter_string(data)
    conn.sendall((resposta + "\n").encode())

    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8000))
    server.listen()

    print("Servidor rodando na porta 8000...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()