import rpyc
from datetime import datetime
from rpyc.utils.server import ThreadedServer

class TimeService(rpyc.Service):

    def exposed_get_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"Pedido de horário recebido às {now}")
        return now

if __name__ == "__main__":
    server = ThreadedServer(TimeService, port=18812)
    print("Servidor RPC de horario rodando...")
    server.start()