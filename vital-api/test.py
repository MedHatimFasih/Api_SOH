import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5003"

# Organes vitaux
organs = {
    "cardiac": ["tachycardie", "bradycardie", "arythmie", "hypertension"],
    "respiratory": ["asthme", "bpco", "apnee", "hyperventilation"],
    "neural": ["epilepsie", "migraine", "trouble_sommeil", "stress"],
    "hepatic": ["hepatite", "cirrhose"]
}

def test_organ(organ_name, conditions):
    print(f"\n=== Test {organ_name.capitalize()} System ===")

    # Status
    r = requests.get(f"{BASE_URL}/api/{organ_name}/status")
    print("Status:", json.dumps(r.json(), indent=2))

    # Data
    r = requests.get(f"{BASE_URL}/api/{organ_name}/data")
    print("Data:", json.dumps(r.json(), indent=2))

    # Parameters
    r = requests.get(f"{BASE_URL}/api/{organ_name}/parameters")
    print("Parameters:", json.dumps(r.json(), indent=2))

    # Simulation
    for condition in conditions:
        r = requests.post(f"{BASE_URL}/api/{organ_name}/simulate/{condition}")
        print(f"Simulate {condition}:", json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    print(f"=== Test started at {datetime.now().isoformat()} ===")

    for organ, conditions in organs.items():
        test_organ(organ, conditions)

    print(f"\n=== Test finished at {datetime.now().isoformat()} ===")
