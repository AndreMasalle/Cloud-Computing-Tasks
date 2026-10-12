import zmq
import time

ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)

# Bind ke port 1666 (sesuai ilustrasi di PDF)
pub.bind("tcp://*:1666")

# ==========================================
# GANTI BAGIAN INI DENGAN DATA KELOMPOKMU
# ==========================================
members = [
    {"topic": "103012580060-Adrian", "name": "Adrian Maulana", "game": "Call of Duty"},
    {"topic": "103012580057-Rizki", "name": "Muhammad Rizki Anshari", "game": "Dota 2"},
    {"topic": "103012580015-Dhafa", "name": "Muhammad Dhafa Ramadhani", "game": "Mobile Legend"},
    {"topic": "103012580019-Andre", "name": "Andre Fransiscus Masalle", "game": "Where Winds Meet"},
]


time.sleep(2)

for m in members:
    msg = f"Hey, I got a new message for '{m['name']}' - It is from {m['game']}"

    # Kirim multipart: [topik, pesan]
    pub.send_multipart([m["topic"].encode(), msg.encode()])

    print(f"Publisher mengirim ke {m['topic']}: {msg}")
    time.sleep(0.5)

print("Selesai mengirim semua pesan.")
time.sleep(2)

pub.close()
ctx.term()