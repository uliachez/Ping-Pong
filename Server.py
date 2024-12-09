import socket
import threading
import os

# Константы
HOST = '127.0.0.1'  # Локальный хост
PORT = 65432         # Порт для связи

# Обработчик клиента
def handle_client(conn, addr):
    try:
        with conn:
            print(f"Подключено к {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break  # Прекратить работу, если данные не получены
                
                print(f"Получено от клиента {addr}: {data.decode()}")
                
                if data.decode() == "ping":
                    response = "pong"  # Ответ на ping
                    conn.sendall(response.encode())  # Отправка ответа клиенту
                elif data.decode() == "pong":
                    response = "ping"  # Ответ на pong
                    conn.sendall(response.encode())  # Отправка ответа
    except Exception as e:
        print(f"Ошибка при обработке клиента {addr}: {e}")

# Создание сокета
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))  # Привязка сокета к адресу и порту
            s.listen()  # Ожидание подключения
            print(f"Сервер запущен, ожидание подключения на {HOST}:{PORT}")
            
            while True:
                try:
                    conn, addr = s.accept()  # Принятие подключения от клиента
                    print(f"Подключение от клиента: {addr}")
                    
                    # Создаем новый поток для обработки клиента
                    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                    client_thread.start()
                except Exception as e:
                    print(f"Ошибка при подключении клиента: {e}")
        
        except PermissionError:
            print("Ошибка: недостаточно прав для привязки сокета. Попробуйте запустить сервер с правами администратора.")
        except OSError as e:
            print(f"Ошибка при привязке сокета: {e}")
except Exception as e:
    print(f"Ошибка при запуске сервера: {e}")
