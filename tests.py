import logging
from test_tool import BotTester
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an instance of BotTester
bot_tester_instance = BotTester(bot_username='@Itzik_mail_sender_bot')


# Test functions
def test_end_to_end():
    logger.info("Running end-to-end test...")
    try:
        bot_tester_instance.get_file_to_send()
        bot_tester_instance.send_command('/start')
        assert bot_tester_instance.verify_output('Please enter email')
        bot_tester_instance.send_command('itzikla1988@gmail.com')
        assert bot_tester_instance.verify_output("What's your file?")
        file_name = '11.png'
        bot_tester_instance.extract_element_by_file_name(file_name)
        assert bot_tester_instance.verify_output('Success')
        logger.info(Fore.GREEN + "End-to-end test passed successfully." + Style.RESET_ALL)
        return True
    except AssertionError as e:
        logger.error(Fore.RED + "End-to-end test failed: %s" % e + Style.RESET_ALL)
        return False


def test_negative_wrong_file():
    logger.info("Running negative test: wrong file...")
    try:
        bot_tester_instance.send_command('/start')
        assert bot_tester_instance.verify_output('Please enter email')
        bot_tester_instance.send_command('itzikla1988@gmail.com')
        assert bot_tester_instance.verify_output("What's your file?")
        bot_tester_instance.send_command('file_name.png')
        assert bot_tester_instance.verify_output("Please send a file.")
        logger.info(Fore.GREEN + "Negative test: wrong file passed." + Style.RESET_ALL)
        return True
    except AssertionError as e:
        logger.error(Fore.RED + "Negative test: wrong file failed: %s" % e + Style.RESET_ALL)
        return False

def test_negative_malformed_mail_address():
    logger.info("Running negative test: malformed mail address...")
    try:
        bot_tester_instance.send_command('/start')
        assert bot_tester_instance.verify_output('Please enter email')
        bot_tester_instance.send_command('invalid_mail.com')
        assert bot_tester_instance.verify_output("Email address is not valid. Try again with /start command.")
        logger.info(Fore.GREEN + "Negative test: malformed mail address passed." + Style.RESET_ALL)
        return True
    except AssertionError as e:
        logger.error(Fore.RED + "Negative test: malformed mail address failed: %s" % e + Style.RESET_ALL)
        return False


def end_of_tests(test_results):
    bot_tester_instance.close()
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    logger.info(f"Summary: {passed_tests} tests passed out of {total_tests}.")
    if passed_tests == total_tests:
        logger.info(Fore.GREEN + "All tests passed successfully." + Style.RESET_ALL)
    else:
        logger.info(Fore.RED + f"{total_tests - passed_tests} tests failed." + Style.RESET_ALL)


# Run tests
if __name__ == "__main__":
    test_results = []
    test_results.append(test_end_to_end())
    test_results.append(test_negative_wrong_file())
    test_results.append(test_negative_malformed_mail_address())
    end_of_tests(test_results)
