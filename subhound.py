import requests
import pandas as pd
import time
import configparser
import os
import argparse
import sys
import logging


BANNER = '''
   _____       __    __  __                      __
  / ___/__  __/ /_  / / / /___  __  ______  ____/ /
  \__ \/ / / / __ \/ /_/ / __ \/ / / / __ \/ __  / 
 ___/ / /_/ / /_/ / __  / /_/ / /_/ / / / / /_/ /  
/____/\__,_/_.___/_/ /_/\____/\__,_/_/ /_/\__,_/   
        
        By: Abdelrhman Allam (@sl4x0)                                               

'''
print(BANNER)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_subdomains(domain):
    try:
        # Retrieve the subdomains for a domain from crt.sh
        url = f'https://crt.sh/?q=%25.{domain}&output=json'
        response = requests.get(url)
        response.raise_for_status()
        subdomains = response.json()

        # Extract the subdomains from the response
        subdomain_list = [entry['name_value'] for entry in subdomains]

        return subdomain_list

    except requests.exceptions.RequestException as e:
        logging.error(f'🛑 Error getting subdomains for {domain}: {e}')
        sys.exit(1)


def save_subdomains_to_file(subdomains, filename):
    try:
        # Load the existing subdomains from the file
        with open(filename, 'r') as f:
            existing_subdomains = set(f.read().splitlines())
    except FileNotFoundError:
        existing_subdomains = set()

    # Save any new subdomains to the file
    with open(filename, 'a') as f:
        for subdomain in subdomains:
            if not subdomain.startswith('*') and not subdomain.startswith('.'):
                if subdomain not in existing_subdomains:
                    f.write(f'{subdomain}\n')
                    existing_subdomains.add(subdomain)

    # Sort the subdomains and remove duplicates
    with open(filename, 'r') as f:
        subdomains = f.read().splitlines()
    subdomains = sorted(set(subdomains))
    with open(filename, 'w') as f:
        f.write('\n'.join(subdomains))


def send_discord_message(channel_name, message, webhook_url):
    # Send a message to the specified Discord channel using the specified webhook URL
    payload = {'content': message, 'username': 'Subdomain Monitor'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, json=payload, headers=headers)
    response.raise_for_status()


def send_telegram_message(bot_token, chat_id, message):
    # Send a message to the specified Telegram chat using the specified bot token
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, params=params)
    response.raise_for_status()


def send_telegram_message(bot_token, chat_id, message):
    # Send a message to the specified Telegram chat using the specified bot token
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, params=params)
    response.raise_for_status()


def check_for_new_subdomains(domain, config, interval=60):
    # Retrieve the Discord and Telegram details from the configuration
    try:
        discord_webhook_url = config.get('discord', 'webhook_url')
        discord_channel_name = config.get('discord', 'channel_name')
        telegram_bot_token = config.get('telegram', 'bot_token')
        telegram_chat_id = config.get('telegram', 'chat_id')
    except configparser.Error as e:
        logging.error(f'Error reading configuration file: {e}')
        sys.exit(1)

    # Create a directory for the domain's files
    directory = f"{domain}_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the filenames for the subdomains and new subdomains
    subdomains_filename = f'{directory}/{domain}_subdomains.txt'
    new_subdomains_filename = f'{directory}/{domain}_new_subdomains.txt'

    # Retrieve the existing subdomains from the file
    try:
        with open(subdomains_filename, 'r') as f:
            existing_subdomains = set(f.read().splitlines())
    except FileNotFoundError:
        existing_subdomains = set()

    while True:
        # Retrieve the subdomains for the domain
        subdomains = get_subdomains(domain)

        # Save the subdomains to a file
        save_subdomains_to_file(subdomains, subdomains_filename)

        # Check for new subdomains
        new_subdomains = set(subdomains) - existing_subdomains

        # Save the new subdomains to a file
        with open(new_subdomains_filename, 'a') as f:
            for subdomain in new_subdomains:
                f.write(f'{subdomain}\n')

        # Send a message if there are new subdomains
        if new_subdomains:
            message = f'New subdomains found for {domain}:\n\n'
            message += '\n'.join(sorted(new_subdomains))

            try:
                send_discord_message(discord_channel_name, message, discord_webhook_url)
            except Exception as e:
                logging.error(f'Error sending Discord message: {e}')

            try:
                send_telegram_message(telegram_bot_token, telegram_chat_id, message)
            except Exception as e:
                logging.error(f'Error sending Telegram message: {e}')

            logging.info(f'New subdomains found for {domain}!')

        # Update the existing subdomains
        existing_subdomains |= new_subdomains

        # Wait for the specified interval before checking for new subdomains again
        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monitor subdomains for a domain.')
    parser.add_argument('-d', '--domain', type=str, help='Domain to search subdomains for', required=True)
    parser.add_argument('--config', type=str, help='the configuration file to use', default='config.ini')
    parser.add_argument('--interval', type=int, help='the interval between checks (in seconds)', default=60)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    check_for_new_subdomains(args.domain, config, args.interval)