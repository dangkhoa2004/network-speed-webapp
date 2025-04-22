from flask import Flask, render_template, jsonify, request
import time
import socket
import psutil
import os
import subprocess
import json
import requests

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

def get_network_info():
    info = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                info.append({
                    "interface": interface,
                    "ip": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast,
                })
    return info

for i in get_network_info():
    print(i)

@app.route("/api/publicip")
def get_public_ip_info():
    try:
        ip_api_url = "http://ip-api.com/json/"
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
        if not (
            client_ip.startswith("127.") or
            client_ip.startswith("192.168.") or
            client_ip.startswith("10.") or
            client_ip == "localhost"
        ):
            ip_api_url = f"http://ip-api.com/json/{client_ip}"

        res = requests.get(ip_api_url)
        data = res.json()

        return jsonify({
            "ip": data.get("query"),
            "isp": data.get("isp"),
            "asn": data.get("as"),
            "org": data.get("org"),
            "hostname": data.get("reverse"),
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/speedtest")
def speed_test():
    start_time = time.time()
    try:
        result = subprocess.run(["speedtest-cli", "--json"], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({"error": "Không thể thực hiện speedtest."}), 500

        data = json.loads(result.stdout)
        total_time = time.time() - start_time
        return jsonify({
            "ping": data.get("ping"),
            "download": data.get("download", 0) / 1_000_000,
            "upload": data.get("upload", 0) / 1_000_000,
            "test_duration": total_time
        })
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {str(e)}"}), 500
@app.route("/api/networkinfo")
def network_info():
    try:
        info = {
            "interfaces": []
        }

        for name, addrs in psutil.net_if_addrs().items():
            iface = {
                "interface": name,
                "ipv4": None,
                "ipv6": [],
                "netmask": None
            }

            for addr in addrs:
                # IPv4
                if addr.family == socket.AF_INET:
                    ip = addr.address
                    if ip.startswith(("127.", "169.", "26.")):  # loại IP loopback, APIPA, VPN
                        continue
                    iface["ipv4"] = ip
                    iface["netmask"] = addr.netmask

                # IPv6
                elif addr.family == socket.AF_INET6:
                    ipv6 = addr.address
                    if ipv6.startswith("fe80"):  # link-local IPv6
                        continue
                    iface["ipv6"].append(ipv6)

            # Chỉ thêm nếu có địa chỉ hợp lệ
            if iface["ipv4"] or iface["ipv6"]:
                info["interfaces"].append(iface)

        # Tìm Default Gateway dựa trên IP đầu tiên
        for iface in info["interfaces"]:
            if iface["ipv4"]:
                info["default_gateway"] = ".".join(iface["ipv4"].split(".")[:-1] + ["1"])
                break

        # DNS fallback
        if os.name != 'nt':
            dns_servers = []
            try:
                with open("/etc/resolv.conf") as f:
                    for line in f:
                        if line.startswith("nameserver"):
                            dns_servers.append(line.strip().split()[1])
            except:
                pass
        else:
            dns_servers = ["8.8.8.8", "8.8.4.4"]

        info["dns_servers"] = dns_servers

        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)