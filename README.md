# Network Intrusion Detection and Automated Response using Suricata

## 📌 Project Overview

This project implements a lightweight **Network Intrusion Detection and Automated Response System** using **Suricata IDS**, **Python**, and **UFW Firewall**.

The system monitors network traffic, detects suspicious activities such as ICMP traffic and TCP SYN scans, generates security alerts through Suricata, and automatically blocks the detected attacker's IP address using UFW.

The project was designed as a lightweight cybersecurity project without requiring resource-heavy platforms such as Elasticsearch, TheHive, or other large SIEM/SOAR platforms.

---

## 🎯 Objectives

- Monitor network traffic using Suricata.
- Detect suspicious ICMP traffic.
- Detect TCP SYN scanning/Nmap activity.
- Generate alerts using custom Suricata rules.
- Store security events in `eve.json`.
- Automatically extract the attacker's IP address.
- Automatically block malicious IP addresses using UFW.
- Demonstrate an end-to-end intrusion detection and automated response workflow.

---


## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Ubuntu | IDS and automated response server |
| Kali Linux | Attack simulation |
| Suricata 6.0.4 | Network Intrusion Detection |
| Python 3 | Automated response |
| UFW | Firewall and IP blocking |
| Nmap | TCP SYN scan simulation |
| tcpdump | Network traffic verification |
| GitHub | Project documentation |

---

## Environmental setup
 Network Configuration

### Ubuntu

```text
IP Address: X.X.X.X
Interface: enp0s3
Role: Suricata IDS and Automated Response Server
```

### Kali Linux

```text
IP Address: X.X.X.X
Role: Attack Simulation Machine
```

The two machines were connected to the same network and tested using ICMP ping.

---

# 🔧 Suricata Installation

Update Ubuntu packages:

```bash
sudo apt update
```

Install Suricata:

```bash
sudo apt install suricata -y
```

Check the installed version:

```bash
suricata --build-info
```

---

# 🔍 Network Interface

Check network interfaces:

```bash
ip addr
```

The interface used in this project was:

```text
enp0s3
```

Check the IP address:

```bash
ip addr show enp0s3
```

---

# ⚙️ Suricata Configuration

The main Suricata configuration file is:

```text
/etc/suricata/suricata.yaml
```

Open the configuration:

```bash
sudo nano /etc/suricata/suricata.yaml
```

The configured network uses:

```text
HOME_NET
```

The project used:

```text
192.168.0.0/16
```

This network range includes the laboratory machines used for testing.

---

# 📜 Custom Suricata Rules

Custom rules were stored in:

```text
/var/lib/suricata/rules/local.rules
```

Open the rules file:

```bash
sudo nano /var/lib/suricata/rules/local.rules
```

## ICMP Detection Rule

The ICMP detection rule used was:

```text
alert icmp any any -> $HOME_NET any (msg:"LOCAL ICMP TEST DETECTED"; sid:1000002; rev:1;)
```

This rule generates an alert when ICMP traffic is detected.

---

## TCP SYN Detection Rule

The TCP SYN detection rule used was:

```text
alert tcp any any -> $HOME_NET any (msg:"LOCAL TCP SYN DETECTED"; flags:S; sid:1000003; rev:1;)
```

This rule detects TCP SYN packets and was used to identify Nmap SYN scanning activity.

---

# 🧪 Testing Suricata Configuration

Before starting Suricata, the configuration was tested using:

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml
```

A successful configuration produces:

```text
Configuration provided was successfully loaded. Exiting.
```

---

# ▶️ Starting Suricata

Restart Suricata:

```bash
sudo systemctl restart suricata
```

Check its status:

```bash
sudo systemctl status suricata --no-pager
```

Expected:

```text
Active: active (running)
```

---

# 🌐 Network Traffic Verification

The network interface was monitored using `tcpdump`.

For ICMP traffic:

```bash
sudo tcpdump -ni enp0s3 icmp
```

For TCP SYN traffic:

```bash
sudo tcpdump -ni enp0s3 'tcp[tcpflags] & tcp-syn != 0'
```

This verified that attack traffic from Kali was reaching the Ubuntu IDS interface.

---

# 🚨 ICMP Attack Detection

From Kali Linux:

```bash
ping -c 5 X.X.X.X
```

Suricata generated an alert in:

```text
/var/log/suricata/eve.json
```

To view the alert:

```bash
sudo grep 'LOCAL ICMP TEST DETECTED' /var/log/suricata/eve.json | tail -n 5 | jq .
```

The alert contains information such as:

```text
Source IP
Destination IP
Protocol
Alert signature
Severity
Timestamp
Network interface
```

---

# 🔥 Nmap TCP SYN Scan Detection

Nmap was used from Kali Linux to simulate a TCP SYN scan.

Command:

```bash
sudo nmap -sS -T3 -p 1-1000 X.X.X.X
```

The scan generated TCP SYN traffic that was detected by Suricata.

To view the Suricata alert:

```bash
sudo grep 'LOCAL TCP SYN DETECTED' /var/log/suricata/eve.json | tail -n 10 | jq .
```

The resulting alert identifies the attacker's IP address.

Example:

```text
Source IP: X.X.X.X
Destination IP: X.X.X.X
Protocol: TCP
Signature: LOCAL TCP SYN DETECTED
```

---

# 🤖 Automated Response

A Python script was developed to monitor Suricata's `eve.json` file.

The script:

1. Monitors Suricata alerts.
2. Identifies the TCP SYN detection signature.
3. Extracts the source IP address.
4. Sends the IP to UFW.
5. Blocks the attacker automatically.

Python script:

```text
scripts/auto_response.py
```

Run the response engine:

```bash
python3 ~/auto_response.py
```

Expected output:

```text
[*] Suricata Automated Response Engine Started
[*] Monitoring: /var/log/suricata/eve.json
[*] Detection: LOCAL TCP SYN DETECTED

[ALERT] LOCAL TCP SYN DETECTED
[ATTACKER] X.X.X.X
[BLOCKED] X.X.X.X
```

---

# 🛡️ UFW Firewall Response

Check UFW status:

```bash
sudo ufw status
```

Check numbered firewall rules:

```bash
sudo ufw status numbered
```

After automated response, the attacker IP was blocked:

```text
Status: active

[1] Anywhere    DENY IN    X.X.X.X
```

This demonstrates the automated response component of the project.


