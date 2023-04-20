D_FROM = 9051
D_TO = 19050
D_PROTO = "socks5"
D_IP = "127.0.0.1"
D_OUTPUT = "proxy.txt"

FROM = input(f"[FROM]({D_FROM}): ")
if FROM: D_FROM = FROM
TO = input(f"[TO]({D_TO}): ")
if TO: D_TO = TO
PROTO = input(f"[PROTO]({D_PROTO}): ") # protocol (socks4, socks5, http, https, ssh, ftp, sftp)
if PROTO: D_PROTO = PROTO
IP = input(f"[IP]({D_IP}): ")
if IP: D_IP = IP
PASSWORD = input("[PASSWORD]: ")
OUTPUT = input(f"[OUTPUT]({D_OUTPUT}): ")
if OUTPUT: D_OUTPUT = OUTPUT

lines = []
for port in range(D_FROM, D_TO):
    line = f"{D_PROTO}:{D_IP}:{port} {PASSWORD}"
    lines.append(line)

with open(D_OUTPUT, "w") as pFile:
    pFile.write('\n'.join(lines))
pFile.close()