from automation.workflows import AmazonAccountCreationWorkflow

if __name__ == "__main__":
    name = "Kenneth J. Beard"
    # phone_number = "6722823510"
    password = "@Test2025"
    country = "canada"
    AmazonAccountCreationWorkflow(name=name, password=password, country=country).run()
