import rpyc

def main():
    try:
        conn = rpyc.connect("localhost", 18812)
        
        horario = conn.root.get_time()
        
        print(f"Horario recebido do servidor: {horario}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    main()