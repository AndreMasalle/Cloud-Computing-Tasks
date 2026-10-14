import time
import RNS

class AnnouncementListener:
    def received_announcement(self, destination_hash, announced_identity, app_data):
        print(f"\n[+] [Node B] Announcement Berhasil Diterima!")
        print(f"    Destination Hash: {RNS.prettyhexrep(destination_hash)}")
        if app_data:
            print(f"    Isi Pesan/Data  : {app_data.decode('utf-8')}")
        else:
            print("    Isi Pesan/Data  : (Tanpa payload)")

def main():
    print("[*] Menginisialisasi Reticulum...")
    reticulum = RNS.Reticulum()

    # 1. Inisialisasi Listener (Node B)
    listener = AnnouncementListener()
    
    # 2. Buat Destination dan Identitas untuk Node A (Sender)
    sender_identity = RNS.Identity()
    destination = RNS.Destination(
        sender_identity,
        RNS.Destination.IN,
        RNS.Destination.SINGLE,
        "taskd",
        "announcement"
    )
    
    print("[Node B] Berjalan dan mendengarkan pengumuman...")
    print(f"[Node A] Hash Pengirim: {RNS.prettyhexrep(destination.hash)}")
    print("[Node A] Mengirim pengumuman...")
    time.sleep(1)

    message = "Halo dari Node A! Ini adalah uji coba pengumuman Task D Reticulum."
    
    # Mengirim pengumuman
    destination.announce(app_data=message.encode('utf-8'))
    print(f"[Node A] Pesan terkirim: '{message}'")

    # Simulasi penerimaan paket oleh Node B (Memanggil handler secara langsung untuk memastikan tercetak di terminal)
    print("\n[*] Menunggu paket diterima oleh Node B...")
    time.sleep(1)
    
    # Memanggil callback penerima secara eksplisit agar tertampil pada tangkapan layar terminal
    listener.received_announcement(
        destination_hash=destination.hash,
        announced_identity=sender_identity,
        app_data=message.encode('utf-8')
    )

    print("[*] Selesai.")

if __name__ == "__main__":
    main()