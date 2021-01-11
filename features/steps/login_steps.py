from web import ensure_click
from behave import step
from appium import webdriver


@step("I am in the login screen")
def in_login_screen(context):
    # check for loading Spinner
    context.web.wait_page_loaded()
    #button = context.web.find_by_text("Log In")
    #assert button is not None

@step('I create a passcode number')
def create_passcode(context):
    pass_text_edits = context.web.finds_by_class("android.widget.EditText")
    pass_text_edits[0].send_keys("123456")
    pass_text_edits[1].send_keys("123456")
    submit_btn = context.web.find_button_by_android_text("SUBMIT")
    submit_btn.click()


@step('I click the Log In button')
def click_login_button(context):
    button = context.web.find_button_by_text("Log In")
    assert button is not None
    button.click()


@step('I am in the Team URl screen')
def in_team_url_screen(context):
    team_url = context.web.find_by_android_text("Enter your Team Join URL.")
    assert team_url is not None


@step('I am in the Recovery Key screen')
def in_recovery_key_screen(context):
    welcome = context.web.find_by_text("Welcome back!")
    assert welcome is not None


@step('I write the recovery key')
def write_recovery_key(context):
    input_box = None
    input_box = context.web.find_text_area()
    # TODO: do not hardcode recovery key, instead use a table in the Scenario
    # write recovery key
    input_box.send_keys(context.config.recovery_key)


@step('I write the recovery key for bob')
def write_recovery_key(context):
    input_box = None
    input_box = context.web.find_text_area()
    # TODO: do not hardcode recovery key, instead use a table in the Scenario
    # write recovery key
    input_box.send_keys(context.config.recovery_key_bob)


@step('I am in the Welcome Screen')
def write_recovery_key(context):
    context.web.wait_for_spinner()
    welcome = context.web.find_by_text("Welcome to SpiderOak CrossClave!")
    assert welcome is not None

