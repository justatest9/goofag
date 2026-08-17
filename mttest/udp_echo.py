#!/usr/bin/env python3
import socket
import struct
import sys
import argparse

def main():
    # Настраиваем злой парсер аргументов командной строки
    parser = argparse.ArgumentParser(
        description="UDP-SOCKS5 checker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-p", "--proxy-ip", default="127.0.0.1", help="IP твоего SOCKS5 прокси (sing-box)")
    parser.add_argument("-P", "--proxy-port", type=int, default=1080, help="Порт твоего SOCKS5 прокси")
    parser.add_argument("-t", "--target-ip", default="65.21.106.102", help="IP публичного UDP/Эхо сервера")
    parser.add_argument("-T", "--target-port", type=int, default=8080, help="Порт публичного UDP/Эхо сервера")
    parser.add_argument("-m", "--message", default="Hey sup", help="Текст сообщения для отправки")
    parser.add_argument("-w", "--timeout", type=float, default=2.0, help="Таймаут ожидания ответа в секундах")
    
    args = parser.parse_args()

    # 1. Открываем TCP-солид сокет до локального SOCKS5
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)
    
    try:
        s.connect((args.proxy_ip, args.proxy_port))
        
        # Хэндшейк SOCKS5 (Метод \x00 — без авторизации)
        s.sendall(b"\x05\x01\x00")
        if s.recv(2) != b"\x05\x00":
            print(f"❌ Ошибка: Прокси {args.proxy_ip}:{args.proxy_port} требует авторизацию или сломан!")
            sys.exit(1)
        
        # Запрашиваем команду UDP Associate (\x03)
        s.sendall(b"\x05\x03\x00\x01\x00\x00\x00\x00\x00\x00")
        resp = s.recv(10)
        
        if not resp or resp[1] != 0:
            print("❌ Ошибка: sing-box отклонил UDP-ассоциацию! Проверь флаговые инбаунды.")
            sys.exit(1)
        
        # Вытаскиваем динамический UDP-порт, который прокси открыл для нас на localhost
        p_port = struct.unpack(">H", resp[8:10])[0]
        
        # 2. Переходим на чистокровный UDP
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.settimeout(args.timeout)
        
        # Собираем заголовок SOCKS5 UDP (RSV=0000, FRAG=00, ATYP=01 [IPv4])
        try:
            target_bytes = socket.inet_aton(args.target_ip)
        except socket.error:
            print(f"❌ Ошибка: Неверный формат целевого IP-адреса: {args.target_ip}")
            sys.exit(1)
            
        socks5_header = b"\x00\x00\x00\x01" + target_bytes + struct.pack(">H", args.target_port)
        payload = args.message.encode("utf-8", errors="ignore")
        
        # Стреляем пакетом прямиком в sing-box на выделенный UDP-порт
        udp.sendto(socks5_header + payload, (args.proxy_ip, p_port))
        
        # Ловим ответный пакет
        data, addr = udp.recvfrom(2048)
        
        # Отрезаем заголовок SOCKS5 от прилетевших данных (первые 10 байт)
        if len(data) > 10:
            server_reply = data[10:].decode("utf-8", errors="ignore")
            print(f"\n🔥 Responded: {server_reply}")
            sys.exit(0) # Возвращаем 0 в Баш (Успех!)
        else:
            print("⚠ Прилетела какая-то пустая залупа короче 10 байт.")
            sys.exit(1)
            
    except socket.timeout:
        print(f"\n❌ ТАЙМАУТ ({args.timeout}с)! Пакет ушел, но ответа от {args.target_ip}:{args.target_port} нет. МТС глушит UDP!")
        sys.exit(1) # Возвращаем 1 в Баш (Ошибка/Таймаут)
    except Exception as e:
        print(f"\n❌ Критическая ошибка сети: {e}")
        sys.exit(1)
    finally:
        s.close()

if __name__ == "__main__":
    main()

