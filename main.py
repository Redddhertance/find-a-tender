import os
import json
import requests
from dotenv import load_dotenv
from dantic import Releases
from utility import contract_hash, process_contract, get_sync_time, update_sync_time
from jinja import send_alert
from datetime import datetime

load_dotenv()

def run_pipeline():
    user_email = os.getenv("USER_EMAIL")
    updated_from = get_sync_time()
    now = datetime.now()
    updated_to = now.strftime('%Y-%m-%dT%H:%M:%S')
    url = 'https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages'
    parameters = {
        'updatedFrom': updated_from,
        'updatedTo': updated_to,
        'limit': 100
    }

    print('Fetching data from Find a Tender API...')
    print("Syncing window: {} to {}".format(updated_from, updated_to))


    response = requests.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()
    with open('tenders.json', 'w') as f:
        json.dump(data, f, indent=4)
    with open('tenders.json', 'r') as f:
        raw_data = json.load(f)
    print('Success')
    releases_data = raw_data.get("releases", [])
    searched_releases = []
    for dictrelease in releases_data:
        try:
            release_object = Releases(**dictrelease)
            if release_object.tender is not None:
                title = release_object.tender.title if release_object.tender.title else None
                status = release_object.tender.status if release_object.tender.status else None
            else:
                title = None
                status = None

            if release_object.tender and release_object.tender.value:
                value_amount = release_object.tender.value.amount if release_object.tender.value.amount else None
                value_currency = release_object.tender.value.currency if release_object.tender.value.currency else None
            else:
                value_amount = None
                value_currency = None
            if release_object.tender and release_object.tender.tenderPeriod:
                end_date = release_object.tender.tenderPeriod.endDate if release_object.tender.tenderPeriod.endDate else None
            else:
                end_date = None
            buyer_name = release_object.buyer.name if release_object.buyer else None

            json_string = release_object.model_dump_json()
            contracthash=contract_hash(title, status, value_amount, end_date)

            dbaction = process_contract(
                ocid=release_object.ocid,
                publish_date=release_object.date.isoformat(),
                title=title,
                status=status,
                value_amount=value_amount,
                value_currency=value_currency,
                buyer_name=buyer_name,
                raw_json=json_string,
                contract_hash=contracthash
            )
            print("Contract {} processed with action: {}".format(release_object.ocid, dbaction))
            if dbaction in ('NEW', 'UPDATED'):
                send_alert(title, value_amount, buyer_name)
            searched_releases.append(release_object)
            print("Parsed release:", release_object.ocid)
        except Exception as exception:
            print(f"Error parsing release: {exception}")
    update_sync_time(updated_to)
    print('Pipline synced')

if __name__ == "__main__":
    run_pipeline()