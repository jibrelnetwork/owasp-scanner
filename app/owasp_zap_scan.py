#!/usr/bin/env python3

import os
import time
import json
import slack

# sites_list = ["jibrel.com", "jwallet.network"]
local_zap_folder = "/tmp/zap"
docker_zap_folder = "/zap/wrk"
zap_file_names = {}
# slack_token = "xoxb-186470154240-786121597206-FVYtm6RW1utaQGEQZ5xCrEq7"
slack_channel_index = "C014P63V8L8"
site_list_file = "/app/sites_list.txt"
slack_token = os.getenv('SLACK_TOKEN')

with open(site_list_file) as f:
    sites_list = f.read().splitlines()


def make_zap_filenames():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    for site in sites_list:
        zap_file_names[site] = "{}-{}".format(site, timestamp)


def run_tests():
    for site in sites_list:
        zap_command = "zap-baseline.py -t https://{} -j -a -m 1 -r {}.html -J {}.json".format(site,
                                                                                                 zap_file_names[site],
                                                                                                 zap_file_names[site])
        print(zap_file_names[site])
        print("starting docker")
        try:
            os.system(zap_command)
        except:
            pass


def analise_test_results():
    print("start test analyse")
    for site in sites_list:
        zap_file = "{}/{}.json".format(docker_zap_folder, zap_file_names[site])
        with open(zap_file) as json_file:
            json_data = json.load(json_file)
            result = ""
            emoji = ":tada:"
            for v in sorted(json_data['site'][0]['alerts'], key=lambda i: (i['riskcode'], i['confidence']), reverse=True):
                if "High (High)" in v["riskdesc"]:
                    emoji = ":name_badge:"
                result = result + v["riskdesc"] + "   |   " + v["alert"] + "\n"
            send_slack_notify(slack_client, site, result, emoji)


def send_slack_notify(slack_client, site, message, emoji):
    slack_client.chat_postMessage(
        channel=slack_channel_index,
        text="{} Site {} scan report: \n {}".format(emoji, site, message),
    )


slack_client = slack.WebClient(slack_token)
make_zap_filenames()
run_tests()
analise_test_results()
