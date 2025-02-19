from automation.workflows import AmazonAccountCreationWorkflow
from utils.logger import logger
from utils.utils import write_to_csv

if __name__ == "__main__":
    number_of_accounts = input("How many accounts would you like to create?\n")

    try:
        number_of_accounts = int(number_of_accounts)
    except ValueError:
        logger.error("Please enter an integer")

    if number_of_accounts <= 0:
        logger.error("Please enter a number greater than 0")

    logger.info("Starting amazon account creation workflow")
    for i in range(1, number_of_accounts+1):
        logger.info(f"Creating account number {i}")

        amazon_account_creation_flow = AmazonAccountCreationWorkflow()

        try:
            name, phone_number, password, totp = amazon_account_creation_flow.run()
        except Exception as e:
            amazon_account_creation_flow.cleanup()
            logger.error("Something went wrong while creating the Amazon account")
            logger.debug(e)
            continue

        try:
            write_to_csv(name, phone_number, password, totp)
            logger.info(f"Finished Amazon Account with the name {name} phone number {phone_number}!!")

        except Exception as e:
            logger.error(
                "Something went wrong while writing the Amazon account details to csv. "
                "Please ensure the csv file is not open"
            )
            logger.info(f"Here is the created data, please add it manually. {name}, {phone_number}, {password}, {totp}")
            logger.debug(e)
