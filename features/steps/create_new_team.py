from behave import step
from web import ensure_click
from fixtures import TestConfig



@step('I enter the License Key')
def write_setup_url(context):
    input_box = context.web.find_by_android_text_input()
    input_box.send_keys(context.config.license_key)


@step('I click the Create Team button')
def click_create_team_button(context):
    button = context.web.find_button_by_text("Create Team")
    assert button is not None
    ensure_click(button)


@step('I enter the valid team name and check the continue button becomes active')
def write_team_name(context):
    input_box = context.web.find_text_input("Team Name")
    input_box.send_keys(context.config.team_name)


@step('I enter the name for the user and check the Continue button becomes active')
def write_user_name(context):
    input_box = context.web.find_text_input("Alice Thompson")
    input_box.send_keys(context.config.admin_user)


@step('I see the team name in the Team Selector')
def in_team_name_screen(context):
    print('Creating team ' + context.config.team_name)
    team_name = context.web.find_by_text(context.config.team_name)
    assert team_name is not None
