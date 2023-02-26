import requests
import json

import pandas as pd


INSTANCES_URL = "https://api.joinmastodon.org/servers?language=en&category=&region=&ownership=&registrations="
INSTANCE_DETAIL_URL = "https://{domain}/api/v2/instance"


instances_response = requests.get(INSTANCES_URL)
instances = json.loads(instances_response.text)

rules = {}
for instance in instances:
    domain = instance["domain"]
    instance_response = requests.get(INSTANCE_DETAIL_URL.format(domain=domain))
    try:
        instance = json.loads(instance_response.text)
        monthly_active_users = instance["usage"]["users"]["active_month"]
        instance_rules = []
        for rule in instance["rules"]:
            instance_rules.append(rule["text"])
        rules[f"{domain} ({monthly_active_users})"] = pd.Series(instance_rules)
    except json.decoder.JSONDecodeError:
        print(domain)

rules_df = pd.DataFrame(rules)
rules_df.to_csv("instance-rules.csv")
