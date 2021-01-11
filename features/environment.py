from behave import use_fixture
from fixtures import base_config, set_appdata_dir, crossclave_config,\
    kill_all_clients, generate_license_key, set_sig_kill_term
import logging

logging.basicConfig(filename=f'test.log', filemode='w',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')


def before_all(context):
    """ Write config for ALL tests.
    This includes: CIF URLs, account IDs, random string generation for things
    like space name, team name, user names, etc. Everything set here is used
    in ALL tests."""
    use_fixture(base_config, context)


def before_scenario(context, feature):
    """ For each testing scenario, yield a new instance of CrossClave
    This means that each testing scenario will start in either the Login screen
    or the Welcome screen, in case we were already logged in."""
    use_fixture(crossclave_config, context)


# If we find an Alice or Bob tag, switch the AppData dir
def before_tag(context, tag):
    if tag in ["Alice", "Bob"]:
        logging.debug(f"Found tag {tag}")
        use_fixture(set_appdata_dir, context, tag)
    elif tag in ["CreateTeam"]:
        logging.debug("Generating License Key...")
        use_fixture(generate_license_key, context)
    elif tag in ["SIGKILL"]:
        use_fixture(set_sig_kill_term, context)


# Kill all lingering processes when we are done
def after_all(context):
    kill_all_clients()
