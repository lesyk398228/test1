import socket
import os

BUFFER_SIZE = 2048
SERVER_PORT = 55000
SERVER_HOST = 'localhost'

def upload(sock, file_path):
    try:
        with open(file_path, mode="rb") as file:
            data = file.read(BUFFER_SIZE)
            while data:
                sock.send(data)
                data = file.read(BUFFER_SIZE)
        print("Вивантаження файлу завершено.")
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
    except Exception as e:
        print(f"Сталася помилка при вивантаженні файлу: {e}")

def download(sock, file_path):
    try:
        with open(os.path.basename(file_path), mode="wb") as file:
            while True:
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
        print("Завантаження завершено.")
    except Exception as e:
        print(f"Сталася помилка при завантаженні файлу: {e}")

def handle_command(command, sock):
    words = command.split(' ')
    if words[0].lower() == 'upload':
        if len(words) > 1:
            file_path = ' '.join(words[1:])
            print(f"Пошуковий запит: {file_path}")
            sock.send(bytes(command, 'utf-8'))
            upload(sock, file_path)
        else:
            print("Пошуковий запит не вказано.")
    elif words[0].lower() == 'download':
        if len(words) > 1:
            file_path = ' '.join(words[1:])
            print(f"Пошуковий запит: {file_path}")
            sock.send(bytes(command, 'utf-8'))
            download(sock, file_path)
        else:
            print("Пошуковий запит не вказано.")
    else:
        print("Невідома команда.")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
        while True:
            command = input(">>> ")
            handle_command(command, sock)
    except ConnectionError:
        print("Не вдалося підключитися до сервера.")
    except Exception as e:
        print(f"Сталася помилка: {e}")
    finally:
        sock.close()
