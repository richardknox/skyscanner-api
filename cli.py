from api import Api
import yaml

if __name__ == "__main__":

    with open("config.yml", "r") as ymlfile:
        config = yaml.full_load(ymlfile)

    api = Api(config['api_key'])
    res = api.fetch_quotes("US", "EUR", "en-US", "SFO-sky", "LHR-sky", "2019-10-01")
    print(res)
