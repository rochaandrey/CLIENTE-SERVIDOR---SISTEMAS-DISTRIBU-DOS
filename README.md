# CLIENTE-SERVIDOR - SISTEMAS-DISTRIBUÍDOS

### DESCRIÇÃO:

#### Servidor: 
- Escuta a porta 8000 e aceita conexões de clientes. 
- Para cada cliente, cria uma thread que recebe uma mensagem e inverte o texto
- Envia essa resposta de volta ao cliente.

#### Cliente:
- Conecta-se ao servidor na porta 8000
- Envia uma mensagem de texto e exibe a resposta recebida pelo servidor

### EXPLICAÇÃO ESPECÍFICA:

- Aqui eu crio um soquete TCP/IP com as informações necessárias: AF_INET significa usar endereços IPV4 como localhost, e SOCK_STREAM significa que é do tipo TCP (garante a entrega das mensagens).
- O servidor está escutando (esperando conexões) na porta 8080

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 8000))
        server.listen()

- O server.accept() bloqueia o trânsito de arquivos até que alguém se conecte ao servidor, retornando o socket e o endereço ip do cliente.

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

- inverter_string(var) inverte a string recebida como se fosse um for do fim da string para o início (essa implementação é mais eficiente e resumida)

        def inverter_string(var):
            return var[::-1]

- Sobre a thread para os clientes, eu crio uma thread separada para cada cliente, ou seja, o servidor aceita uma nova conexão sem a antiga terminar, aceitando até 1024 Bytes de conteúdo. Os itens ".decode()" e ".strip()" formatam a mensagem enquando o "sendall()" garante o envio completo da mensagem.

        def handle_client(conn, addr):
            print("Nova conexão: {}".format(addr))

            data = conn.recv(1024).decode().strip()
            print("Recebido do cliente: {}".format(data))

            resposta = inverter_string(data)
            conn.sendall(resposta.encode())

            conn.close()

- O cliente se conecta ao "localhost":8080, envia (.sendall) e recebe a mensagem de volta (.recv) salvando na variável resposta para imprimir posteriormente.

        def main():
            meuCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            meuCliente.connect(("localhost", 8000))

            mensagem = "Olá mundo distribuído"
            meuCliente.sendall(mensagem.encode())

            resposta = meuCliente.recv(1024).decode()
            print("Resposta do servidor:", resposta)

            meuCliente.close()