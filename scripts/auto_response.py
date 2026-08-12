import json
import subprocess
import time

EVE_LOG = "/var/log/suricata/eve.json"
TARGET_SIGNATURE = "LOCAL TCP SYN SCAN DETECTED"


def block_ip(ip):
    result = subprocess.run(
        ["sudo", "ufw", "deny", "from", ip],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"[BLOCKED] {ip}")
    else:
        print(f"[ERROR] Could not block {ip}: {result.stderr.strip()}")


print("[*] Suricata Automated Response Engine Started")
print(f"[*] Monitoring: {EVE_LOG}")
print(f"[*] Detection: {TARGET_SIGNATURE}")

with open(EVE_LOG, "r") as log:
    log.seek(0, 2)

    while True:
        line = log.readline()

        if not line:
            time.sleep(0.5)
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if event.get("event_type") != "alert":
            continue

        alert = event.get("alert", {})
        signature = alert.get("signature")
        source_ip = event.get("src_ip")

        if signature == TARGET_SIGNATURE and source_ip:
            print(f"[ALERT] {signature}")
            print(f"[ATTACKER] {source_ip}")

            block_ip(source_ip)
