import socket
import time
import threading

# Константы
HOST = '127.0.0.1'  # Адрес сервера
PORT = 65432         # Порт сервера

flag = True
def stop():
    global flag
    while flag:
        command = input()
        if command.strip().lower() == "stop":
            flag = False
            print("Отключение клиента...")
        else: 
            print("Неверная команда")

# Создание сокета
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))  # Подключение к серверу
            print(f"Подключено к серверу {HOST}:{PORT}")
            
            # Запуск потока для отслеживания команды "стоп"
            stop_thread = threading.Thread(target=stop, daemon=True)
            stop_thread.start()

            message = "pong"
            while flag:  # Пинг-понг цикл
                if (message == "pong"):
                    message = "ping"
                else:
                    message = "pong"
                print(f"Отправка: {message}")
                s.sendall(message.encode())  # Отправка сообщения серверу
                
                data = s.recv(1024)  # Получение ответа от сервера
                print(f"Получено: {data.decode()}")
                
                time.sleep(2)  # Пауза между отправками сообщений

        except ConnectionRefusedError:
            print(f"Не удалось подключиться к серверу {HOST}:{PORT}. Сервер может быть выключен.")
        except socket.error as e:
            print(f"Ошибка сокета: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка при работе с сервером: {e}")
        except flag == False:
                print("Отключение от сервера...")
        finally:
            print("Отключено от сервера.")
            
except PermissionError:
    print("Ошибка: недостаточно прав для подключения к серверу. Попробуйте запустить клиент с правами администратора.")
except Exception as e:
    print(f"Ошибка при запуске клиента: {e}")
