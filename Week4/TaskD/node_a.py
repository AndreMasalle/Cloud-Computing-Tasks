import RNS
import time

def main():
    # Inisialisasi Reticulum
    rns = RNS.Reticulum()

    # Membuat Identity baru untuk Node A
    identity = RNS.Identity()

    print("[Node A] Reticulum diinisialisasi.")
    print(f"[Node A] Hash Identitas: {RNS.hexrep(identity.hash)}")

    # Membuat Destination bertipe SINGLE dengan nama aplikasi (misal: "taskd" dan aspek "node_a")
    app_name = "taskd"
    destination = RNS.Destination(
        identity,
        RNS.Destination.IN,
        RNS.Destination.SINGLE,
        app_name,
        "node_a"
    )

    print(f"[Node A] Destination Hash: {RNS.hexrep(destination.hash)}")

    # Mengirim pengumuman (Announcement) melalui objek Destination
    print("[Node A] Mengirim pengumuman...")
    destination.announce(app_data=b"Halo dari Node A!")

    # Beri waktu sejenak agar paket terkirim
    time.sleep(3)
    print("[Node A] Selesai.")

if __name__ == "__main__":
    main()