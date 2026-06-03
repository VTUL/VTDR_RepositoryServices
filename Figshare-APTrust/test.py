from figshare import Figshare
import configparser
import json
import os

config = configparser.ConfigParser()
config.read("configurations.ini")

token = config["FigshareSettings"]["token"]

article_id = 31448899
fversion = None

fs = Figshare(token=token, private=False, version=fversion)

print(f"Testing metadata download for article: {article_id}")

metadata = fs.get_article_details(article_id, version=fversion)

out_file = f"{article_id}_metadata_test.json"

with open(out_file, "w") as f:
    json.dump(metadata, f, indent=4)

print(f"Success! Metadata JSON saved to: {os.path.abspath(out_file)}")