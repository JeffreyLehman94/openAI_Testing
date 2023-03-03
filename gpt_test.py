from selenium import webdriver
import time
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_auto_update import check_driver
from myconfig import *
import pyautogui

check_driver(r'C:\Users\Jeff\Desktop\Python\PRAW_GPT')
prompt_header_gpt = 'Create a response to the following comment from r/aww. Do not mention you are an ai. ' \
                    'Make the response sound like it came from an old person born in 1950s.'


def close_driver(driver):
    driver.close()
    driver.quit()


def request_gpt(reddit_reply_praw):
    def clickerc(e, wait=20):
        element = WebDriverWait(driver, wait).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, e)))
        element.click()
        return element

    # Launch a new Chrome browser window
    driver = uc.Chrome()

    # Navigate to the OpenAI chat app
    driver.get("https://chat.openai.com/chat")

    # Wait for the login form to load
    # time.sleep(100)

    # ADD TRY ACCEPT FOR AREW YOU A BOT CLICK

    # Fill in the login form and submit it
    try:
        clickerc(
            '#__next > div.w-full.h-full.flex.justify-center.items-center.flex-col.bg-gray-50.dark\:bg-gray-800 > div '
            '> div.flex.flex-row.gap-3 > button:nth-child(1)')

        clickerc('#username').send_keys(EMAIL)
        clickerc('body > main > section > div > div > div > form > div.ca4ba6ae0 > button')
        clickerc('#password').send_keys(EMAIL_PASSWORD)
        clickerc('body > main > section > div > div > div > form > div.ca4ba6ae0 > button')
    except:
        print('couldnt log in - trying again')
        request_gpt(prompt_header_gpt, reddit_reply_praw)

    # click thru initial popups:

    clickerc('#headlessui-dialog-panel-\:r1\: > div.prose.dark\:prose-invert > div.flex.gap-4.mt-6 > button')
    clickerc('#headlessui-dialog-panel-\:r1\: > div.prose.dark\:prose-invert > div.flex.gap-4.mt-6 > '
             'button.btn.flex.justify-center.gap-2.btn-neutral.ml-auto')
    clickerc(
        '#headlessui-dialog-panel-\:r1\: > div.prose.dark\:prose-invert > div.flex.gap-4.mt-6 > '
        'button.btn.flex.justify-center.gap-2.btn-primary.ml-auto')

    clickerc('#__next > div.overflow-hidden.w-full.h-full.relative > '
             'div.dark.hidden.bg-gray-900.md\:fixed.md\:inset-y-0.md\:flex.md\:w-\[260px\].md\:flex-col > div > div > '
             'nav > a:nth-child(4)')

    time.sleep(3)
    # buy plan option
    try:
        # clickerc('#headlessui-dialog-panel-\:r3\: > div.flex.h-full.flex-col.items-center.justify-start > div > div
        # > div.flex.w-full.flex-row.items-center.justify-between.border-b.py-3.px-4.dark\:border-gray-700 > button >
        # svg')
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
    except:
        print('No plan options to click thru')
    # Find the chat input box and type a message
    clickerc('#__next > div.overflow-hidden.w-full.h-full.relative > div.flex.h-full.flex-1.flex-col.md\:pl-\[260px\] '
             '> main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border'
             '-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md'
             '\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient > form > div > '
             'div.flex.flex-col.w-full.py-2.flex-grow.md\:py-3.md\:pl-4.relative.border.border-black\/10.bg-white'
             '.dark\:border-gray-900\/50.dark\:text-white.dark\:bg-gray-700.rounded-md.shadow-\[0_0_10px_rgba\(0\,0\,'
             '0\,0\.10\)\].dark\:shadow-\[0_0_15px_rgba\(0\,0\,0\,0\.10\)\] > textarea').send_keys(
        prompt_header_gpt + reddit_reply_praw)
    clickerc('#__next > div.overflow-hidden.w-full.h-full.relative > div.flex.h-full.flex-1.flex-col.md\:pl-\[260px\] '
             '> main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border'
             '-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md'
             '\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient > form > div > '
             'div.flex.flex-col.w-full.py-2.flex-grow.md\:py-3.md\:pl-4.relative.border.border-black\/10.bg-white'
             '.dark\:border-gray-900\/50.dark\:text-white.dark\:bg-gray-700.rounded-md.shadow-\[0_0_10px_rgba\(0\,0\,'
             '0\,0\.10\)\].dark\:shadow-\[0_0_15px_rgba\(0\,0\,0\,0\.10\)\] > button')

    # time.sleep (1000)
    # Submit the message by pressing enter
    # chat_input.submit()

    # Wait for the reply from ChatGPT
    time.sleep(10)

    # while True:
    #     chat_messages = driver.find_elements(".message")
    #     latest_message = chat_messages[-1]
    #     if latest_message.get_attribute("data-source") == "gpt":
    #         gpt_reply = latest_message.find_element_by_css_selector(".message-body").text
    #         break
    #     time.sleep(1)

    # Print the ChatGPT reply
    reply_sel = clickerc('#__next > div.overflow-hidden.w-full.h-full.relative > '
                         'div.flex.h-full.flex-1.flex-col.md\:pl-\[260px\] > main > div.flex-1.overflow-hidden > div '
                         '> div > div > div.w-full.border-b.border-black\/10.dark\:border-gray-900\/50.text-gray-800'
                         '.dark\:text-gray-100.group.bg-gray-50.dark\:bg-\[\#444654\]')
    reply_from_gpt = reply_sel.text
    print(reply_from_gpt)
    driver.close()
    return reply_from_gpt

# request_gpt()

### TODO: add filter for "as an AI language model" and other bullshit responses. - this should be done in python after receiving reply_from_gpt reply
### TODO: make it so that we don't have to open chatgpt for every reply. Have it pull the bottom reply every time and keep the window open. Probably can just increment the one integer value in the css - need to double check this
