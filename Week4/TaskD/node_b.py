import RNS
import time

class AnnouncementHandler:
    def __init__(self):
        pass

    def received_announcement(self, destination_hash, announced_identity, app_data):
        print("\n[Node B] Menerima Pengumuman!")
        print(f"  - Destination Hash: {RNS.hexrepr(destination_hash)}")
        print(f"  - Identity Hash:    {RNS.hexrepr(announced_identity.hash())}")
        if app_data:
            print(f"  - App Data:         {app_data.decode('utf-8')}")

def main():
    rns = RNS.Reticulum()
    print("[Node B] Menunggu pengumuman di jaringan Reticulum...")

    handler = AnnouncementHandler()
    # Perbaikan menggunakan register_announce_handler
    RNS.Transport.register_announce_handler(handler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Node B] Dihentikan.")

if __name__ == "__main__":
    main()