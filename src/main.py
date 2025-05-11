from automation.workflows import AmazonAccountCreationWorkflow
from utils.logger import logger
from utils.utils import read_from_excel, write_to_excel


if __name__ == "__main__":
    df = read_from_excel()
    df = df[df['status'].notnull()]
    if df.empty:
        logger.info("No new accounts to create")
        exit(0)

    logger.info(f"Found {df.shape[0]} new outlook accounts in the excel file")
    for idx, row in df.iterrows():
        logger.info(f"Creating account for {row['outlook_email']} at row no {idx}")

        amazon_account_creation_flow = AmazonAccountCreationWorkflow(
            email=row['outlook_email'], outlook_password=row['outlook_password']
        )

        try:
            name, phone_number, password, totp = amazon_account_creation_flow.run()
            amazon_account_creation_flow.cleanup()
        except Exception as e:
            write_to_excel(index=idx, status="failed")
            amazon_account_creation_flow.cleanup()
            logger.error("Something went wrong while creating the Amazon account")
            logger.debug(e)
            continue

        try:
            write_to_excel(index=idx, name=name, password=password, totp=totp, status="created")
            logger.info(f"Finished Amazon Account with the name {name} phone number {phone_number}")

        except Exception as e:
            logger.error(
                "Something went wrong while writing the Amazon account details to csv. "
                "Please ensure the csv file is not open"
            )
            logger.info(f"Here is the created data, please add it manually. {name}, {password}, {totp}")
            logger.debug(e)
