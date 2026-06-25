from cryptography.fernet import Fernet as fernet, InvalidToken
import hashlib
import base64
import socket 
import threading

def enkrip(text, key):
    return key.encrypt(text.encode()).decode()


def dekrip(text, key):
    return key.decrypt(text.encode()).decode()

def buat_kunci_fernet(password_user: str):
    password_bytes = password_user.encode()
    sha256_hash = hashlib.sha256(password_bytes).digest()
    kunci_final = base64.urlsafe_b64encode(sha256_hash)
    return kunci_final

def mengambil_address_port():
    while True:
        try:
            alamat_server = input("masukan ip address dan port dengan format ({address}:{port}): ").replace(" ", "")
            pemisah = alamat_server.find(":")

            address = alamat_server[:pemisah]
            port = int(alamat_server[pemisah:].replace(":", ""))
            break
        except ValueError:
            print("[-] format tidak dapat diterima")

    return address, port

key = ""

def terima_pesan(bebas):
    while True:
        try:
            data = bebas.recv(1024).decode()

            if not data:
                print("\n[Sistem] Koneksi ditutup.")
                break
            # Cetak pesan dari lawan bicara
            print(f"\t\t{dekrip(data, key)}")
            print(end="", flush=True) 
        except Exception as e:
            print(e)
            break
    print("\n[Sistem] Thread penerima berhenti. Tekan Enter untuk keluar.\n")

while True:
    mode = input("server/client: ").lower()

    if mode not in ["server", "client", "1", "2"]:
        print("[-] input tidak tersedia")
    else:
        break
# -------------------------------------------------------------------------------------
if mode in ["server","1"]:
    print("membuat server")

    while True:
        address, port = mengambil_address_port()

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((address, port))

            print(f"[+] server berhasil di host di ip {address} dengan port {port}")
            break

        except (socket.gaierror, OSError) as e:
            print("[-] ip address tidak dapat diterima sebagai server\n", e)

    password = input("buat password room: ")
    password_fernet = buat_kunci_fernet(password)
    key = fernet(password_fernet)
    server.listen()

    client_socket, address = server.accept()
    while True:
        try:
            tes_pass_client = client_socket.recv(1024).decode()

            if dekrip(tes_pass_client, key) == "tes_koneksi":
                client_socket.send(b"masuk")
                print("[+] client berhasil masuk")
                break

        except InvalidToken:
            client_socket.send(b"g")
            print("[+] client mengirim password yang salah")

    thread_terima = threading.Thread(target=terima_pesan, args=(client_socket,))
    thread_terima.daemon = True
    thread_terima.start()

    print("\n--- Mulai Chatting (Ketik 'exit' untuk keluar) ---")
    while True:
        try:
            pesan = input("")
            if pesan.lower().strip() == 'exit':
                break

            if not pesan.strip():
                continue

            client_socket.send(enkrip(pesan, key).encode())
        except (KeyboardInterrupt, EOFError):
            break

    print("\n-- Server dimatikan --")
    server.close()

# -------------------------------------------------------------------------------
elif mode in ["client","2"]:

    while True:
        address, port = mengambil_address_port()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.connect((address, port))
            break
        except (ConnectionRefusedError, KeyboardInterrupt, OSError):
            print("[-] gagal menyambung dengan server")

    while True:
        passw = input("masukan password untuk masuk ke room: ")
        client_pass = fernet(buat_kunci_fernet(passw))
        client.send(enkrip("tes_koneksi", client_pass).encode())

        kode_server = client.recv(1024).decode()

        if kode_server == "masuk":
            print("[+] berhasil masuk")
            key = client_pass
            break

        else:
            print("[-] password salah")

    thread_terima = threading.Thread(target=terima_pesan, args=(client,))
    thread_terima.daemon = True
    thread_terima.start()

    print("\n--- Mulai Chatting (Ketik 'exit' untuk keluar) ---")
    while True:
        try:
            pesan = input("")
            if pesan.lower().strip() == 'exit':
                break

            if not pesan.strip():
                continue

            client.send(enkrip(pesan, key).encode())
        except (KeyboardInterrupt, EOFError):
            break

    print("\n-- Keluar dari panggilan --")
    client.close()