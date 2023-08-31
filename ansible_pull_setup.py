import argparse
import configparser
import logging
import random
import sys


class AnsibleSetupScript:
    def __init__(self):
        self.hosts = []
        self.args = self.parse_args()
        self.inventory_file = self.args.inventory_file
        self.playbook_enable = "ansible_pull_setup.yaml"
        self.playbook_disable = "ansible_pull_uninstall.yaml"
        self.configure_logging()

    def configure_logging(self):
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    def read_inventory(self):
        config = configparser.ConfigParser()
        config.read(self.inventory_file)

        for section in config.sections():
            if not section.startswith("_"):
                self.hosts.append(section)

    def generate_random_hour(self):
        # Generate a random hour between 23 and 5 and wrap around
        return (random.randint(0, 5) + 23) % 24

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Ansible Pull Setup")
        parser.add_argument("--enable", action="store_true", help="Enable setup")
        parser.add_argument("--disable", action="store_true", help="Disable setup")
        parser.add_argument(
            "--inventory-file",
            default="inventory.ini",
            help="Path to override the inventory file",
        )
        return parser.parse_args()

    def run(self):
        if not self.args.enable and not self.args.disable:
            logging.error(
                "Please provide either --enable or --disable parameter to proceed."
            )
            return

        self.read_inventory()

        print("Available hosts:")
        for index, host in enumerate(self.hosts, start=1):
            print(f"{index}. {host}")
        print(f"{len(self.hosts) + 1}. all")

        selected_hosts_input = input("Select hosts (comma-separated or 'all'): ")

        if selected_hosts_input.lower() == "all":
            selected_host_indices = list(range(len(self.hosts)))  # Select all hosts
        else:
            selected_host_indices = [
                int(index.strip()) - 1 for index in selected_hosts_input.split(",")
            ]

        selected_hostnames = [self.hosts[index] for index in selected_host_indices]
        selected_hosts_str = ",".join(selected_hostnames)

        for host in selected_hostnames:
            if self.args.enable:
                random_hour = self.generate_random_hour()
                command = (
                    f"ansible-playbook -i {self.inventory_file} -l {host} "
                    f"-e 'random_hour={random_hour}' {self.playbook_enable}"
                )
                logging.info(
                    f"Running the following command for host {host}:\n{command}"
                )

                # Uncomment the next lines to actually run the command
                import os

                os.system(command)
            elif self.args.disable:
                command = (
                    f"ansible-playbook -i {self.inventory_file} -l {host} "
                    f"{self.playbook_disable}"
                )
                logging.info(
                    f"Running the following command for host {host}:\n{command}"
                )

                # Uncomment the next lines to actually run the command
                import os

                os.system(command)
            print()  # Add a line break after each execution


if __name__ == "__main__":
    ansible_script = AnsibleSetupScript()
    ansible_script.run()
