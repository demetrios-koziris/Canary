import codecs
import configparser

# Currency
import decimal


class Parser:
    def __init__(self):
        self.configfile = './config/config.ini'

        config = configparser.ConfigParser()
        config.read_file(codecs.open(self.configfile, "r", "utf-8-sig"))

        self.discord_key = config['Discord']['Key']

        self.welcome = config['Greetings']['Welcome'].split('\n')
        self.goodbye = config['Greetings']['Goodbye'].split('\n')

        self.db_path = config['DB']['Path']

        # Below lies currency configuration

        currency_precision = int(config["Currency"]["Precision"])

        income_tb = zip(
            [x.strip() for x in config["IncomeTax"]["Brackets"].split(",")],
            [x.strip() for x in config["IncomeTax"]["Amounts"].split(",")])

        asset_tb = zip(
            [x.strip() for x in config["AssetTax"]["Brackets"].split(",")],
            [x.strip() for x in config["AssetTax"]["Amounts"].split(",")])

        br_cases = zip(
            [x.strip() for x in config["Betting"]["RollCases"].split(",")],
            [x.strip() for x in config["Betting"]["RollReturns"].split(",")])

        self.currency = {
            "name":
            config["Currency"]["Name"],
            "symbol":
            config["Currency"]["Symbol"],
            "precision":
            currency_precision,
            "initial_amount":
            decimal.Decimal(config["Currency"]["Initial"]),
            "salary_base":
            decimal.Decimal(config["Currency"]["SalaryBase"]),
            "inflation":
            decimal.Decimal(config["Currency"]["Inflation"]),
            "income_tax": {decimal.Decimal(b): float(a)
                           for b, a in income_tb},
            "asset_tax": {decimal.Decimal(b): float(a)
                          for b, a in asset_tb},
            "transaction_tax":
            float(config["OtherTax"]["TransactionTax"]),
            "bet_roll_cases":
            sorted(
                [(int(c), decimal.Decimal(a)) for c, a in br_cases],
                key=lambda c: c[0])
        }
