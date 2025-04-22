from flask import Flask, render_template, jsonify
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

@app.route("/api/publicip")
def get_public_ip_info():
    try:
        res = requests.get("http://ip-api.com/json/")
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
        info = {}
        for name, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    info["IPv4"] = addr.address
                    info["Subnet Mask"] = addr.netmask
                elif addr.family == socket.AF_INET6:
                    if addr.address.startswith("fe80"):
                        info["Link-local IPv6"] = addr.address
                    elif "temporary" in str(addr):
                        info["Temporary IPv6"] = addr.address
                    else:
                        info["IPv6"] = addr.address

        interfaces = list(psutil.net_if_stats().keys())
        if interfaces:
            stats = psutil.net_if_addrs().get(interfaces[0], [])
            for addr in stats:
                if addr.family == socket.AF_INET:
                    info["Default Gateway"] = ".".join(addr.address.split(".")[:-1] + ["1"])
                    break

        dns_servers = []
        if os.name != 'nt':  # Linux/macOS
            try:
                with open("/etc/resolv.conf") as f:
                    for line in f:
                        if line.startswith("nameserver"):
                            dns_servers.append(line.strip().split()[1])
            except:
                pass

        if dns_servers:
            info["DNS Servers"] = dns_servers

        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)