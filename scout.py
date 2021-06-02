import subprocess
from datetime import datetime 
from discord_webhook import DiscordEmbed, DiscordWebhook 
import io 


def send_alert(webhook_url, offline_device, offline_ip, offline_mac):
    embed = DiscordEmbed(title=f"⚠️ Lost Contact with {offline_device}", color="1ca1ed")
    webhook_object = DiscordWebhook(url=webhook_url)

    embed.add_embed_field(name="Device IP", value=f"{offline_ip}")
    embed.add_embed_field(name="Device MAC", value=f"{offline_mac}")

    webhook_object.add_embed(embed)
    response = webhook_object.execute()

def fetch_devices():
    network_data = {
        "device_name": [],
        "ip_address": [],
        "mac_address": []
    }

    process = subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE)
    arp_resp = [line.strip() for line in io.TextIOWrapper(process.stdout, encoding='utf-8')]

    for name in arp_resp:
        network_data["device_name"].append(name.split()[0])

    for ip in arp_resp:
        network_data["ip_address"].append(ip.split()[1])

    for mac in arp_resp:
        network_data["mac_address"].append(mac.split()[3])

    return network_data

def monitor():
    network_patch = fetch_devices()
    for name, ip, mac in zip(network_patch["device_name"], network_patch["ip_address"], network_patch["mac_address"]):
        print(name, ip, mac) # check each trio and if any ping does not respond then call the send_alert() method and pass the trio's info inside of that method

monitor()
    
