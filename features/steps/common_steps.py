from behave import step

import time

from web import ensure_click


@step('I am on the Welcome Screen')
def in_welcome_screen(context):
    context.web.find_by_text("Welcome to SpiderOak CrossClave!")
    context.web.wait_for_spinner()


@step('I click on the hamburger dropdown menu')
def click_recent_spaces_button(context):
    time.sleep(3)
    button = context.web.find_by_QA_id("TeamSwitcherButton")
    assert button is not None
    ensure_click(button)


@step('I click the Continue button')
def click_continue_button(context):
    button = context.web.find_button_by_android_text("Continue")
    assert button is not None
    ensure_click(button)
    # context.web.wait_for_spinner()


@step('I Select the lock icon on top right')
def click_lock_icon_button(context):
    time.sleep(1)
    button = context.web.find_by_QA_id("lock-menu")
    assert button is not None
    ensure_click(button)
    time.sleep(1)


@step('I Select the lock icon on top right for the space')
def click_lock_icon_button(context):
    button = context.web.find_by_QA_id("lock-menu")
    assert button is not None
    ensure_click(button)


@step('I choose my team')
def click_teams_button(context):
    team = context.web.find_team_by_text(context.config.team_name)
    assert team is not None
    ensure_click(team)


@step('I click on the Peoples tab')
def click_people_button(context):
    button = context.web.find_by_text("People")
    assert button is not None
    ensure_click(button)


@step('Back in the application,I click on the "Close" button')
def click_space_button(context):
    button = context.web.find_by_text("Close")
    assert button is not None
    ensure_click(button)


@step('I write the Team URL')
def write_team_url(context):
    input_box = context.web.find_by_android_text_input()
    # send the CIF URL
    input_box.send_keys(context.config.cif_url)
    context.web.hide_keyword()


@step('I click the Add Team button')
def click_create_team_button(context):
    button = context.web.find_button_by_text("Add Team")
    assert button is not None
    ensure_click(button)


@step('I am on the Peoples Tab and the space members list become visible')
def in_space_screen(context):
    people = context.web.find_by_text("People")


@step('I select Bob from the list of people and The member screen appears')
def click_select_user_button(context):
    print(context.config.non_admin_user)
    button = context.web.find_by_text(context.config.non_admin_user)
    assert button is not None
    ensure_click(button)


@step('I click on one of the spaces created')
def click_space_button(context):
    button = context.web.find_space(context.config.space_name)
    assert button is not None
    ensure_click(button)


@step('I Open a files (...) dropdown menu')
def click_open_file_dropdown_button(context):
    button = context.web.find_by_QA_id("file-menu-button")
    assert button is not None
    ensure_click(button)


@step('I click on Version History')
def click_version_history_button(context):
    button = context.web.find_by_text("Version History")
    assert button is not None
    ensure_click(button)


@step('I Select the back arrow in the top left')
def click_back_button(context):
    button = context.web.find_by_QA_icon_type("arrow-left")
    assert button is not None
    ensure_click(button)


@step('I click on Delete File')
def click_delete_file_button(context):
    button = context.web.find_by_text("Delete File")
    assert button is not None
    ensure_click(button)


@step('The Delete File pop up option becomes visible')
def in_delete_file_pop_up_screen(context):
    delete = context.web.find_by_text("Are you sure you want to delete this file?")
    assert delete is not None


@step('I select the Cancel option from the pop up')
def click_cancel_button(context):
    button = context.web.find_button_by_text("Cancel")
    assert button is not None
    ensure_click(button)


@step('I am returned to the previous screen, the space view')
def in_space_view_screen(context):
    sview = context.web.find_by_text(context.config.space_name)
    assert sview is not None


@step('I click on File details')
def click_version_history_button(context):
    time.sleep(2)
    button = context.web.find_by_text("File Details")
    assert button is not None
    time.sleep(2)
    ensure_click(button)


@step("I see the uploaded file")
def see_uploaded_file(context):
    # File names are split in half in twi different components in
    # CrossClave (to make sure the last part of the file name and the
    # extension is not truncated. So we search for half of this file's
    # filename to see if it's in the space
    file = context.web.find_by_text("file_upload_ste")
    assert file is not None


@step('The "applying changes" spinner briefly appears. When it goes away, you are returned to the user profile and it will display the "Space Administrator" text')
def in_profile_options_screen(context):
    star = context.web.find_by_text("Space Administrator")
    assert star is not None


@step('I Choose settings option')
def click_settings_button(context):
    button = context.web.find_by_text("Settings")
    assert button is not None
    ensure_click(button)


@step('I choose the team I am an admin of')
def click_team_button(context):
    print('Selected team ' + context.config.team_name)
    button = context.web.find_team_in_settings(context.config.team_name)
    assert button is not None
    ensure_click(button)