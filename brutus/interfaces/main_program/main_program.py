"""Main program frontend
"""
import inquirer  # type: ignore

from brutus.interfaces.mac_address.inquirer import run as run_macaddr
from brutus.interfaces.utils.inquirer_utils import destructure
from brutus.models.BaseBrutusModule import BaseBrutusModule
from brutus.models.MainBrutusProcessManager import MainBrutusProcessManager

from .opt_config import confirm, modules, questions


def run_main_ui():
    """Run the main UI routine"""
    main = MainBrutusProcessManager(confirm_fn=confirm)

    # begin CLI menu / prompt
    while True:
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        selected_option, selected_tool, selected_util = destructure(
            answers, 'selected_option', 'selected_tool', 'selected_util'
        )

        if 'back' in answers.values():
            continue

        if selected_option == 'exit':
            break

        if selected_util == 'downgrade_https':
            main.downgrade_ssl()
        elif selected_util == 'port_fwd':
            main.enable_portfwd()
        elif selected_util == 'monitor_mode':
            interface = inquirer.list_input(
                message='Enter the name of a wireless interface to configure',
                choices=BaseBrutusModule.get_interfaces(),
            )

            main.enable_monitor_mode(interface)

        elif selected_util == 'mac_address':
            run_macaddr()

        # run any necessary pretask routines
        if selected_tool:
            main.pretask_routine(modules[selected_tool])

            main.run_module(modules[selected_tool])
