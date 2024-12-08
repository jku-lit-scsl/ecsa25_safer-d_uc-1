import json
import random
import subprocess
import time

import requests


def send_http_request():
    try:
        response = requests.get("192.168.56.20:5000/in_sos_mode")
        if response.status_code == 200 and bool(json.loads(response.text)['is_in_SoS_mode']):
            return True
    except Exception as e:
        print(f"Error sending HTTP request: {e}")
    return False


def main():
    while True:
        # Start main.py
        process = subprocess.Popen(["python", "main.py"])
        print("Started main.py")

        # Wait a random time between 5 and 15 seconds
        wait_time = random.randint(5, 15)
        time.sleep(wait_time)

        # Terminate main.py
        process.terminate()
        process.wait()
        print("Terminated main.py")

        # Check API response every 2 seconds
        while True:
            time.sleep(2)
            if send_http_request():
                print("API returned true, restarting main.py")

                # Restart main.py
                process = subprocess.Popen(["python", "main.py"])
                print("Restarted main.py")

                # Wait an additional fixed 15 seconds
                time.sleep(15)

                # Break to restart the loop
                process.terminate()
                process.wait()
                print("Restart loop after 15 seconds")
                break


if __name__ == "__main__":
    main()
