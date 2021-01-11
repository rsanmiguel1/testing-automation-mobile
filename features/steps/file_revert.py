import hashlib
from behave import step
import time
import glob
import os
from pathlib import Path
from web import ensure_click
import platform


original_hash = None
modified_hash = None
reverted_hash = None
checked_files = []


def get_next_file_version(appdata_dir):
    global checked_files
    # save current working dir
    previous_dir = os.getcwd()
    # move to the appdata_dir
    if platform.system() == 'Darwin':
        path_to_blob = os.path.join(Path.home(), "Library", 'Application Support', appdata_dir, "flow", "blob")
    else:
        path_to_blob = os.path.join(Path.home(), "AppData","Local", appdata_dir, "flow", "blob")

    os.chdir(path_to_blob)

    # check all python files two dirs below here
    for f in glob.glob("./*/*/*.py"):
        if f not in checked_files:
            # add the new file to the checked_list
            checked_files.append(f)
            os.chdir(previous_dir)

            # return the full path of the file
            return os.path.join(path_to_blob, f)


def get_hash(file_path):
    buffer_size = 65536
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            md5_hash.update(data)

    return md5_hash.hexdigest()


@step("I get the hash of the original file")
def get_orig_hash(context):
    global original_hash
    path = get_next_file_version(context.config.appdata_dir)
    original_hash = get_hash(path)


@step("I modify the file")
def modify_file(context):
    with open('features/steps/file_upload_steps.py', 'a') as f:
        f.write("\n")


@step("I click the plus button")
def click_plus_button(context):
    plus = context.web.find_by_QA_id("plus-button")
    ensure_click(plus)


@step("I get the hash of the modified file, and assert it is not the same")
def get_modified_hash(context):
    global modified_hash
    path = get_next_file_version(context.config.appdata_dir)
    modified_hash = get_hash(path)
    assert original_hash is not modified_hash


@step("I click on the revert icon")
def click_on_revert_icon(context):
    revert = context.web.find_by_QA_icon_type("revert")
    ensure_click(revert)
    time.sleep(.25)


@step("I confirm I am on the revert file modal")
def confirm_revert_file_modal(context):
    warning = context.web.find_by_text("Revert File")
    assert warning is not None


@step("I click on the 'No, go back' option")
def click_go_back_option(context):
    no_back = context.web.find_button_by_android_text("No, go back")
    ensure_click(no_back)
    time.sleep(.5)


@step("I click on the 'Revert File' option")
def click_revert_file_option(context):
    revert = context.web.find_button_by_text("Revert File")
    ensure_click(revert)
    context.web.wait_for_spinner()


@step("I get the hash of the reverted file")
def get_reverted_hash(context):
    global reverted_hash
    path = get_next_file_version(context.config.appdata_dir)
    reverted_hash = get_hash(path)


@step("I confirm the reverted file hash is the same as the original file")
def confirm_hash_is_same(context):
    assert (reverted_hash == original_hash)
