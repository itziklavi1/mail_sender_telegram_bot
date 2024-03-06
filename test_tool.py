from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class BotTester:
    def __init__(self, bot_username):
        """
        Initializes the BotTester class.

        Args:
        - bot_username (str): The username of the bot to be tested.
        """
        self.bot_username = bot_username
        self.driver = webdriver.Chrome()
        self.driver.get(f"https://web.telegram.org/k/#{bot_username}")
        logger.info("Awaiting identity verification ")
        self.wait_until_element_present(By.CLASS_NAME, "bubbles.has-groups.scrolled-down", retries=5, wait_time=10)

    def wait_until_element_present(self, by, value, retries=3, wait_time=5):
        """
        Waits until the element specified by 'by' and 'value' is present.

        Args:
        - by: The By strategy to locate the element.
        - value: The value of the locator.
        - retries (int): Number of retries.
        - wait_time (int): Time to wait before retrying in seconds.
        """
        for _ in range(retries):
            try:
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((by, value)))
                return
            except NoSuchElementException:
                logger.warning(f"Element not found: {value}")
                self.driver.refresh()
                time.sleep(wait_time)
        logger.error(f"Element not found after {retries} retries: {value}")

    def get_file_to_send(self):
        """
        Sends the '/send' command to the bot to initiate file sending.
        """
        input_field = self.find_input_field()
        if input_field:
            input_field.send_keys("/send")
            input_field.send_keys(Keys.ENTER)
            time.sleep(10)

    def send_command(self, command):
        """
        Sends a command to the bot.

        Args:
        - command (str): The command to be sent to the bot.
        """
        input_field = self.find_input_field()
        if input_field:
            input_field.send_keys(f"{command}")
            input_field.send_keys(Keys.ENTER)

    def verify_output(self, expected_result):
        """
        Verifies the output of the bot.

        Args:
        - expected_result (str): The expected output from the bot.

        Returns:
        - bool: True if the expected result matches the last message, False otherwise.
        """
        max_retries = 7  # Maximum number of retries
        retries = 0
        while retries < max_retries:
            try:
                last_message = self.find_last_message()
                if expected_result == last_message:
                    return True
                else:
                    raise ValueError("Expected result does not match last message")
            except ValueError:
                logger.error("Expected result does not match last message. Retrying after 2 seconds.")
                time.sleep(2)
                retries += 1
        logger.info("Reached maximum retries. Could not verify output.")
        return False

    def find_input_field(self):
        """
        Finds and returns the input field for sending messages to the bot.

        Returns:
        - WebElement: The input field element, or None if not found.
        """
        self.wait_until_element_present(By.XPATH,
                                        "//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[8]/div[1]/div[1]")
        try:
            input_field = self.driver.find_element(By.XPATH,
                                                   "//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[8]/div[1]/div[1]")
            return input_field
        except NoSuchElementException:
            logger.error("Input field not found.")
            return None

    def find_last_message(self):
        """
        Finds and returns the last message received from the bot.

        Returns:
        - str: The text of the last message, or None if not found.
        """
        self.wait_until_element_present(By.CLASS_NAME, "message.spoilers-container")
        try:
            all_messages = self.driver.find_elements(By.CLASS_NAME, "message.spoilers-container")
            # Split the message and take only the first line, ignoring message time
            last_message_text = all_messages[-1].text.strip().split('\n')[0]
            return last_message_text
        except NoSuchElementException:
            logger.error("Last message not found.")
            return None

    def extract_element_by_file_name(self, file_name):
        """
        Extracts an element based on the file name.

        Args:
        - file_name (str): The name of the file to extract.

        Returns:
        - WebElement: The extracted element, or None if not found.
        """
        self.wait_until_element_present(By.CLASS_NAME, "message.spoilers-container")
        try:
            all_messages = self.driver.find_elements(By.CLASS_NAME, "message.spoilers-container")
            for msg in all_messages:
                if file_name in msg.text.strip().split('\n')[0]:
                    self.forward_message(msg)
                    return
        except NoSuchElementException:
            logger.error("Message not found.")
            return None

    def forward_message(self, msg):
        """
        Forwards a message.

        Args:
        - msg (WebElement): The message element to forward.
        """
        # wait until Download is Finished
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'preloader-container')))
        # click on file
        time.sleep(2)
        msg.click()
        time.sleep(0.5)
        # find forward button and click
        top_bar = (By.CLASS_NAME, "btn-icon")
        # Wait for the element to be present
        self.wait_until_element_present(top_bar[0], top_bar[1])
        forward_button = self.driver.find_elements(*top_bar)
        # click on foward button
        forward_button[4].click()
        # input filed to search forward msg
        locator = (By.CLASS_NAME, "selector-search-input.i18n")
        # Wait for the element to be present
        self.wait_until_element_present(locator[0], locator[1])
        search_chat_field = self.driver.find_element(*locator)
        search_chat_field.send_keys("mail_sender_bot")
        time.sleep(2)
        # chat search results
        result = self.driver.find_elements(By.CLASS_NAME,
                                           "row.no-wrap.row-with-padding.row-clickable.hover-effect.chatlist-chat.chatlist-chat-abitbigger")

        # click on first result (full bot name)
        result[0].click()
        time.sleep(2)
        input_field = self.find_input_field()
        input_field.send_keys(Keys.ENTER)

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    bot_username = '@Itzik_mail_sender_bot'
    tester = BotTester(bot_username)
    tester.run_tests()
    tester.close()