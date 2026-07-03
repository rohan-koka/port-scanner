import streamlit as st
import socket
import concurrent.futures
from datetime import datetime

st.set_page_config(page_title="Port Scanner", layout="centered")

st.title("🔍 Port Scanner")
st.write("Scan a host to discover open ports and services.")

target = st.text_input("Enter target hostname or IP (e.g. scanme.nmap.org)")

col1, col2 = st.columns(2)
start_port = col1.number_input("Start Port", min_value=1, max_value=65535, value=1)
end_port = col2.number_input("End Port", min_value=1, max_value=65535, value=1024)

timeout = st.slider("Timeout per port (seconds)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

common_services = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}

def scan_port(host, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return port if result == 0 else None
    except:
        return None

if st.button("Start Scan"):
    if not target:
        st.error("Please enter a target host.")
    elif start_port > end_port:
        st.error("Start port must be less than end port.")
    else:
        try:
            ip = socket.gethostbyname(target)
            st.info(f"Scanning {target} ({ip}) — ports {int(start_port)} to {int(end_port)}")

            start_time = datetime.now()
            open_ports = []
            port_range = range(int(start_port), int(end_port) + 1)

            progress = st.progress(0)
            status = st.empty()

            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(scan_port, ip, port, timeout): port for port in port_range}
                completed = 0
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        open_ports.append(result)
                    completed += 1
                    progress.progress(completed / len(port_range))
                    status.text(f"Scanning... {completed}/{len(port_range)} ports checked")

            end_time = datetime.now()
            duration = (end_time - start_time).seconds

            st.success(f"Scan complete in {duration} seconds")

            if open_ports:
                open_ports.sort()
                st.markdown("### Open Ports")
                for port in open_ports:
                    service = common_services.get(port, "Unknown")
                    st.markdown(f"- **Port {port}** — {service}")
            else:
                st.warning("No open ports found in the specified range.")

        except socket.gaierror:
            st.error("Could not resolve hostname. Please check the target and try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.caption("⚠️ Only scan hosts you own or have permission to scan. Unauthorized scanning is illegal.")