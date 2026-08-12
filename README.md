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
Technology	Purpose
Ubuntu	IDS and response server
Kali Linux	Attack simulation
Suricata 6.0.4	Network Intrusion Detection
Python 3	Automated response
UFW	Firewall and IP blocking
Nmap	TCP SYN scan simulation
tcpdump	Network traffic verification
GitHub	Project documentation

---



