import subprocess
from datetime import datetime 
from discord_webhook import DiscordEmbed, DiscordWebhook 
import time 
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

    while True:
        active_patch = fetch_devices()

        for name, ip, mac in zip(network_patch["device_name"], network_patch["ip_address"], network_patch["mac_address"]):
            if name in active_patch["device_name"]:
                print(f"[+] {name} is online...Swinging back for another run")
                time.sleep(2.5)
                continue 

            else:
                send_alert("DISCORD-WEBHOOK-URL", name, ip, mac)
                time.sleep(1.5)
                continue 

if __name__ == "__main__":
    monitor()
    
