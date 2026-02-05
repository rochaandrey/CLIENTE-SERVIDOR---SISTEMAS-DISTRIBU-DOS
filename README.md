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

---

## ATIVIDADE II - RPC (REMOTE PROCEDURE CALL) COM RPYC

### DESCRIÇÃO:

#### Servidor:
- Utiliza a biblioteca **RPyC** para expor um serviço de consulta de horário.
- Em vez de gerenciar bytes e buffers manualmente, ele disponibiliza um método que pode ser chamado remotamente como uma função comum.

#### Cliente:
- Conecta-se ao servidor via protocolo RPC.
- Invoca a função de horário do servidor, recebe o dado processado e encerra a conexão.

### EXPLICAÇÃO DO CÓDIGO (COM COMENTÁRIOS):

#### Servidor (`server.py`)
No modelo RPC, definimos um **Serviço** que agrupa as funções que queremos disponibilizar na rede.

        class TimeService(rpyc.Service):
            # 'exposed_' é uma regra do RPyC: apenas métodos com esse nome podem ser chamados pelo cliente

            def exposed_get_time(self):
                # retorna o horário atual formatado. 
                # o RPC converte essa string em bytes para o envio.
                return datetime.now().strftime("%H:%M:%S")

        # ThreadedServer permite que o server aceite múltiplas conexões simultâneas, criando uma thread para cada nova chamada.

        server = ThreadedServer(TimeService, port=18812)
        server.start()



#### Cliente (`client.py`)
A principal vantagem é a **transparência**: o código do cliente não precisa saber detalhes de rede (sockets) para obter o dado.

        # rpyc.connect estabelece a conexão (o "stub") com o servidor na porta 18812.
        conn = rpyc.connect("localhost", 18812)
        
        # 'conn.root' acessa o serviço remoto. 
        # Chamamos get_time() como se fosse uma função local do meu script.
        horario = conn.root.get_time() 
        
        # Exibe o resultado e encerra a sessão RPC.
        print(f"Horário recebido do servidor: {horario}")
        conn.close()

### DIFERENÇAS EM RELAÇÃO AO SOCKET (ATIVIDADE I):

* **Abstração de Dados**: Não é necessário usar `.encode()`, `.decode()` ou definir `recv(1024)`. O RPyC lida com a serialização dos dados automaticamente.
* **Foco na Função**: No Socket, o servidor precisa interpretar o texto recebido para saber o que fazer. No RPC, o cliente escolhe diretamente a função que deseja executar no servidor.
* **Gerenciamento de Conexão**: O RPyC abstrai o controle de fluxo, garantindo que a chamada de função retorne o valor esperado de forma síncrona.