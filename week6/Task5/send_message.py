"""Send a message from a Reticulum Node A to a listening Node B."""

import argparse
import threading
import time

import RNS


APP_NAME = "task5"
DESTINATION_ASPECT = "messaging"
ANNOUNCE_INTERVAL = 15
DISCOVERY_TIMEOUT = 60
MESSAGE_TIMEOUT = 60


def parse_destination_hash(value: str) -> bytes:
    try:
        destination_hash = bytes.fromhex(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "destination hash harus berupa nilai hexadecimal"
        ) from error

    expected_length = RNS.Reticulum.TRUNCATED_HASHLENGTH // 8
    if len(destination_hash) != expected_length:
        raise argparse.ArgumentTypeError(
            f"destination hash harus sepanjang {expected_length * 2} karakter hexadecimal"
        )

    return destination_hash


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mengirim pesan langsung antara Node A dan Node B melalui Reticulum."
    )
    subparsers = parser.add_subparsers(dest="role", required=True)

    subparsers.add_parser(
        "node-b",
        help="jalankan penerima dan tampilkan destination hash",
    )

    sender_parser = subparsers.add_parser(
        "node-a",
        help="kirim pesan ke destination hash milik Node B",
    )
    sender_parser.add_argument(
        "destination_hash",
        type=parse_destination_hash,
        help="destination hash yang ditampilkan Node B",
    )
    sender_parser.add_argument(
        "--message",
        default="Halo dari Node A! Pesan ini dikirim melalui Reticulum.",
        help="isi pesan yang akan dikirim",
    )
    return parser


def run_node_b() -> None:
    reticulum = RNS.Reticulum()
    identity = RNS.Identity()
    destination = RNS.Destination(
        identity,
        RNS.Destination.IN,
        RNS.Destination.SINGLE,
        APP_NAME,
        DESTINATION_ASPECT,
    )

    def receive_message(
        _path, data, _request_id, _link_id, remote_identity, _requested_at
    ):
        message = data.decode("utf-8")
        print("\n[Node B] Pesan diterima!")
        print(f"[Node B] Dari identity: {RNS.hexrep(remote_identity.hash())}")
        print(f"[Node B] Isi pesan: {message}")
        return b"Pesan berhasil diterima oleh Node B."

    destination.register_request_handler(
        "message",
        response_generator=receive_message,
        allow=RNS.Destination.ALLOW_ALL,
    )

    print("[Node B] Siap menerima pesan melalui Reticulum.")
    print(f"[Node B] Identity hash: {RNS.hexrep(identity.hash)}")
    print(f"[Node B] Destination hash: {destination.hash.hex()}")
    destination.announce(app_data=b"Node B siap menerima pesan")

    try:
        while True:
            time.sleep(ANNOUNCE_INTERVAL)
            destination.announce(app_data=b"Node B siap menerima pesan")
    except KeyboardInterrupt:
        print("\n[Node B] Penerima dihentikan.")


def run_node_a(destination_hash: bytes, message: str) -> None:
    reticulum = RNS.Reticulum()
    print(f"[Node A] Mencari Node B: {destination_hash.hex()}")
    RNS.Transport.request_path(destination_hash)

    deadline = time.monotonic() + DISCOVERY_TIMEOUT
    identity = None
    next_path_request = time.monotonic() + 10

    while time.monotonic() < deadline:
        identity = RNS.Identity.recall(destination_hash)
        if identity is not None:
            break

        if time.monotonic() >= next_path_request:
            RNS.Transport.request_path(destination_hash)
            next_path_request = time.monotonic() + 10
        time.sleep(1)

    if identity is None:
        raise TimeoutError(
            "Node B tidak ditemukan. Pastikan Node B berjalan dan kedua node "
            "terhubung ke jaringan Reticulum yang sama."
        )

    print(f"[Node A] Identity Node B: {RNS.hexrep(identity.hash)}")
    destination = RNS.Destination(
        identity,
        RNS.Destination.OUT,
        RNS.Destination.SINGLE,
        APP_NAME,
        DESTINATION_ASPECT,
    )
    completed = threading.Event()
    succeeded = False

    def on_response(receipt) -> None:
        nonlocal succeeded
        response = receipt.get_response()
        if response is None:
            print("[Node A] Node B tidak mengirim konfirmasi.")
        else:
            print(f"[Node A] Konfirmasi: {response.decode('utf-8')}")
            succeeded = True
        completed.set()

    def on_failure(_receipt) -> None:
        print("[Node A] Pengiriman gagal atau melewati batas waktu.")
        completed.set()

    def on_link_established(link) -> None:
        print("[Node A] Link ke Node B berhasil dibuat.")
        print(f"[Node A] Mengirim pesan: {message}")
        receipt = link.request(
            "message",
            data=message.encode("utf-8"),
            response_callback=on_response,
            failed_callback=on_failure,
            timeout=MESSAGE_TIMEOUT,
        )
        if receipt is False:
            print("[Node A] Reticulum menolak request pengiriman.")
            completed.set()

    link = RNS.Link(destination, established_callback=on_link_established)

    if not completed.wait(MESSAGE_TIMEOUT):
        raise TimeoutError(
            "Tidak menerima konfirmasi dari Node B dalam batas waktu."
        )

    if not succeeded:
        raise RuntimeError("Pesan belum berhasil dikonfirmasi oleh Node B.")

    print("[Node A] Pesan berhasil dikirim.")


def main() -> None:
    args = create_parser().parse_args()

    if args.role == "node-b":
        run_node_b()
    else:
        run_node_a(args.destination_hash, args.message)


if __name__ == "__main__":
    main()