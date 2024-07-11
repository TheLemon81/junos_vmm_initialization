import subprocess
import environ
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError

PASSWORD = env.str["PASSWORD"]

cmd = "vmm ip | grep \"RE\"| awk -F \"[ _]\" '{print $3}'"
output_bytes_list = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.splitlines()
vmm_node_list = [i.decode() for i in output_bytes_list]

conf_file = 'configs/default-vmm-router-config.conf'

for VM in vmm_node_list:
    conf_file = 'configs/default-vmm-router-config.conf'
    print("Working on node " + VM)
    def main():
        dev = Device(host=VM, user='root', password=PASSWORD)
        # open a connection with the device and start a NETCONF session
        try:
            dev.open()
        except ConnectError as err:
            print ("Cannot connect to device: {0}".format(err))
            return

        dev.bind(cu=Config)

        # Lock the configuration, load configuration changes, and commit
        print ("Locking the configuration on $VM")
        try:
            dev.cu.lock()
        except LockError as err:
            print ("Unable to lock configuration: {0}".format(err))
            dev.close()
            return

        print ("Loading configuration changes")
        try:
            dev.cu.load(path=conf_file, merge=True)
        except (ConfigLoadError, Exception) as err:
            print ("Unable to load configuration changes: {0}".format(err))
            print ("Unlocking the configuration")
            try:
                dev.cu.unlock()
            except UnlockError:
                print ("Unable to unlock configuration: {0}".format(err))
            dev.close()
            return

        print ("Committing the configuration")
        try:
            dev.cu.commit(comment='Loaded by example.')
        except CommitError as err:
            print ("Unable to commit configuration: {0}".format(err))
            print ("Unlocking the configuration")
            try:
                dev.cu.unlock()
            except UnlockError as err:
                print ("Unable to unlock configuration: {0}".format(err))
            dev.close()
            return

        print ("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError as err:
            print ("Unable to unlock configuration: {0}".format(err))

        # End the NETCONF session and close the connection
        dev.close()

    if __name__ == "__main__":
        main()
