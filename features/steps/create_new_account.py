from behave import step
from web import ensure_click
import time
from appium import webdriver




@step("I click on the Sign Up button")
def click_on_sign_up(context):
    sign_up_button = context.web.find_button_by_android_text("Sign Up")
    ensure_click(sign_up_button)
    # context.web.wait_for_spinner()


@step("I see I am on the 'Save Your Recovery Phrase' screen")
def confirm_on_recovery_phrase_page(context):
    header = context.web.find_button_by_android_text('Save Your Recovery Phrase')
    assert header is not None


@step("I copy the recovery key")
def click_on_copy_icon(context):
    copy_button = context.web.find_button_by_android_text("Copy")
    ensure_click(copy_button)
    time.sleep(.2)


@step("I click Continue")
def click_continue(context):
    button = context.web.find_button_by_android_text('Continue')
    ensure_click(button)



@step("I see the 'Are you sure you saved your Recovery Phrase' screen")
def confirm_on_saved_recovery_phrase_page(context):
    header = context.web.find_by_android_text("Are you sure you saved your Recovery Phrase?")
    assert header is not None


@step("I click on the 'Yes, I saved it' option")
def click_saved_recovery_phrase(context):
    button = context.web.find_button_by_android_text("Yes, I saved it")
    assert button is not None
    ensure_click(button)


@step("I am on the Add/Create team start page")
def confirm_add_create_page(context):
    assert context.web.find_by_android_text("Add Team") is not None
    assert context.web.find_by_android_text("Create Team") is not None
    assert context.web.find_by_android_text_input("example.crossclave") is not None
