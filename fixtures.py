from behave import fixture
#from selenium import webdriver
from poetry.console.commands import self

from web import Web
from appium import webdriver
import random
import psutil
import os
import logging
import signal
import requests
import platform

logging.basicConfig(filename=f'test.log', filemode='a',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

ALICE_APPDATA = "share2-autotest-Alice"
BOB_APPDATA = "share2-autotest-Bob"


def is_windows():
    return platform.system() == 'Windows'


def is_osx():
    return platform.system() == 'Darwin'


class TestConfig:
    def __init__(self):
        # assign a 10 hex random ID to this test run
        # it will be used across the different tests
        self.test_id = "%010x" % random.randrange(16 ** 10)

        self.space_name = "space-%s" % self.test_id
        self.space2_name = "space2-%s" % self.test_id
        self.team_name = "Test-Automation-%s" % self.test_id
        self.team2_name = "Test2-Automation-%s" % self.test_id
        self.admin_user = "Alice-%s" % self.test_id
        self.non_admin_user = "Bob-%s" % self.test_id

        self.alice_text_to_bob = f"Hello {self.non_admin_user}"
        self.bob_text_to_alice = f"Hello {self.admin_user}"

        # Hardcode CIF URL to Staging URL
        self.cif_url = "https://flow-block-staging.cloud.spideroak.com/9fc2df2aa06a9822c4c7e4aa7b669300691e42985611512f91f3bc3d3858a913"
        self.del_cif_url = "https://flow-block-staging.cloud.spideroak.com/9fc2df2aa06a9822c4c7e4aa7b669300691e42985611512f91f3bc3d3858a9"
        self.incorrect_cif_url = "https://flow-block-staging.cloud.spideroak.com/9fc2df2aa06a9822c4c7e4aa7b669300691e42985611512f91f3bc3d3858a912"

        # This credentials are used in order to generate a License Key for team creation
        self.license_generation_url = "https://flow-staging.cloud.spideroak-inc.com/license-service/licenses"
        self.license_generation_user = "spideroak"
        self.license_generation_pass = "2dpC9kbTIufs"

        # self.license_key = None


        # Default to Alice appdata_dir
        # this will be updated each time we find an @Alice or @Bob tag
        self.appdata_dir = ALICE_APPDATA

        # signal used to terminate a process (different signals are available per OS)
        #self.process_kill_signal = signal.SIGTERM if is_windows() else signal.SIGKILL


def proc_names():
    return [p for p in psutil.process_iter()]


def search_procs_by_name(name):
    # Search for PIDs for processes by name
    pids = []
    for p in psutil.process_iter():
        if is_cc_process(p, name):
            pids.append(p.pid)
    return pids


def is_argument(cmdline, appdata):
    # Searches for the AppData string in ALL arguments of a process
    for arg in cmdline:
        if (arg.find(appdata)) >= 0:
            return True
    return False


def is_cc_process(process, appdata_str):
    # Returns True if the Process is a CrossClave or Backend process
    # using the given appdata
    try:
        cmdline = process.cmdline()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        cmdline = []

    if cmdline:
        return is_argument(cmdline, appdata_str)


# Kill all processes that match a given name
def kill_process_by_name(process_name, signal_code):
    for p in search_procs_by_name(process_name):
        try:
            logging.debug(f"Killing {p}")
            os.kill(p, signal_code)
        except ProcessLookupError:
            # The process was waterfall-killed by a previous kill command
            pass


def kill_all_clients(signal_code=signal.SIGTERM):
    kill_process_by_name("SpiderOak CrossClave", signal_code)
    kill_process_by_name("crossclave-backend", signal_code)


@fixture
def base_config(context, timeout=30, **kwargs):
    context.config = TestConfig()
    yield context.config


@fixture
def set_appdata_dir(context, tag):
    # This method switches the CrossClave appdata dir so we can test using
    # different accounts.
    context.config.appdata_dir = f"share2-autotest-{tag}"
    logging.debug(f"Switching appdata to {context.config.appdata_dir}")
    yield context.config


def create_process_options(appdata_dir):
    logging.debug(f"Creating options for {appdata_dir}")
    # set arguments for CrossClave here
    options = webdriver.ChromeOptions
    options.add_argument('--ignore-locking')
    options.add_argument('--no-sandbox')
    options.add_argument("--remote-debugging-port=12209")
    options.add_argument(f'--data-folder-name {appdata_dir}')
    # We would normally override the Chrome binary with CrossClave binary
    # However, because: a) we need to pass the --data-folder-name argument and
    # b) Selenium orders the args by alphabetical order and
    # c) we cannot use --data-folder-name=PATH, but need to put a space,
    # we have to use a hackish bash script to pass the args correctly.
    if is_osx():
        options.binary_location = './launch_cc_osx.sh'
    else:
        options.binary_location = 'c:\\Program Files\\SpiderOak CrossClave\\SpiderOak CrossClave.exe'
    return options


def appdata_toggle(appdata):
    if appdata == ALICE_APPDATA:
        return BOB_APPDATA
    return ALICE_APPDATA


@fixture
# Prepare a basic driver + CrossClave config
def crossclave_config(context, **kwargs):
    options = context.config.appdata_dir
    # Kill previous clients
    # kill_all_clients(context.config.process_kill_signal)

    # create driver and yield it
    # We don't use any now, but if we want to pass arguments *to the driver*
    # (not to CrossClave), we can use the service_args parameter.
    # driver_path = 'tools/chromedriver-84.exe' if is_windows() else 'tools/chromedriver-84_osx'

    desired_cap = {
        "deviceName": "Android Emulator",
        "platformName": "Android",
        "app": os.path.abspath(
            '/Users/rodrigosanmiguel/Desktop/SpiderOak/testing-automation-mobile/tools/CrossClave.apk')
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_cap)
    driver.implicitly_wait(60)
    web = Web(driver)
    web._web_driver = driver
    context.web = web



    # FIXME.... or not?
    # HACK WARNING: we create a second driver with the alternative appdata
    # We launch this process but do not yield the driver
    # This is because we need the other account to get the shared keys and stay
    # up to date; otherwise changes never arrive in time
    #options_alternative = create_process_options(appdata_toggle(context.config.appdata_dir))
    #driver = webdriver.Chrome(executable_path=driver_path, options=options_alternative)

    yield context.web
    # close driver when done
    # if __name__ == '__main__':
    #  webdriver.Remote.close(self)



@fixture
def generate_license_key(context):
    # Generate a License Key in order to create a team
    logging.debug(
        f"Sending POST to get License Key, creds: user={context.config.license_generation_user}, pass={context.config.license_generation_pass}")
    r = requests.post(context.config.license_generation_url,
                      auth=(context.config.license_generation_user,
                            context.config.license_generation_pass))

    # Make sure the License Request worked

    assert r.status_code == 200
    # Save the License Key
    logging.debug("Got license key.")
    context.config.license_key = r.json()['key']
    context.config = TestConfig
    yield context.config


@fixture
def set_sig_kill_term(context):
    context.config.process_kill_signal = signal.SIGTERM if is_windows() else signal.SIGKILL
    yield context.config
