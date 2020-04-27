import subprocess

def enable_port_fwd():
        """
        Enables port forwarding through controller machine.
        """
        print("[+] Enabling port forwarding.")
        ip_fwd_cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
        # test_cmd = "echo 1 >> hello.txt"
        proc = subprocess.Popen(ip_fwd_cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0]),