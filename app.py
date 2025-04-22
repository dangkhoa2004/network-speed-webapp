from flask import Flask, render_template, jsonify
import speedtest
import time
import socket
import psutil
import os

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")
import requests

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
        st = speedtest.Speedtest(secure=True)
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        total_time = time.time() - start_time
        return jsonify({
            "ping": ping,
            "download": download,
            "upload": upload,
            "test_duration": total_time
        })
    except speedtest.SpeedtestException as e:
        return jsonify({"error": f"Lỗi Speedtest: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {e}"}), 500

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
                    elif "temporary" in str(addr):  # Windows không có tag rõ ràng
                        info["Temporary IPv6"] = addr.address
                    else:
                        info["IPv6"] = addr.address

        net_io = psutil.net_if_stats()
        interfaces = list(net_io.keys())
        if interfaces:
            stats = psutil.net_if_addrs().get(interfaces[0], [])
            for addr in stats:
                if addr.family == socket.AF_INET:
                    info["Default Gateway"] = ".".join(addr.address.split(".")[:-1] + ["1"])
                    break

        dns_servers = []
        if os.name != 'nt':  # Trên Linux/macOS
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
    app.run(debug=True)
