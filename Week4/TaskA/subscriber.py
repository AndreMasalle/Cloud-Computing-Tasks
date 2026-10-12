import zmq
import sys
import datetime

if len(sys.argv) < 2:
    print("Error: Masukkan topik!")
    sys.exit(1)

topic = sys.argv[1]

ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)
sub.connect("tcp://localhost:1666")
sub.setsockopt_string(zmq.SUBSCRIBE, topic)

print(f"Subscriber untuk topik '{topic}' sudah jalan...")
print("Menunggu pesan...\n")

sub.setsockopt(zmq.RCVTIMEO, 30000)  # 30000 ms = 30 detik

try:
    topic_b, msg = sub.recv_multipart()
    waktu = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{waktu}] [{topic}] Terima pesan: {msg.decode()}")
except zmq.Again:
    print(f"[{topic}] Tidak ada pesan masuk dalam 30 detik. Program berhenti.")

sub.close()
ctx.term()
print("Subscriber selesai.")