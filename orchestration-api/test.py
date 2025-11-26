# test.py
import requests
import json

BASE_URL = "http://localhost:5000"

def test_home():
    print("=== Test Home ===")
    response = requests.get(BASE_URL)
    print(json.dumps(response.json(), indent=2))

def test_health():
    print("\n=== Test Health ===")
    response = requests.get(f"{BASE_URL}/api/health")
    print(json.dumps(response.json(), indent=2))

def test_health_detailed():
    print("\n=== Test Health Detailed ===")
    response = requests.get(f"{BASE_URL}/api/health/detailed")
    print(json.dumps(response.json(), indent=2))

def test_group_data(group):
    print(f"\n=== Test Group Data: {group} ===")
    response = requests.get(f"{BASE_URL}/api/data/{group}")
    print(json.dumps(response.json(), indent=2))

def test_system_data(group, system):
    print(f"\n=== Test System Data: {group}/{system} ===")
    response = requests.get(f"{BASE_URL}/api/data/{group}/{system}")
    print(json.dumps(response.json(), indent=2))

def test_simulate_global(scenario):
    print(f"\n=== Test Simulate Global: {scenario} ===")
    response = requests.post(f"{BASE_URL}/api/simulate/{scenario}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_home()
    test_health()
    test_health_detailed()
    test_group_data("vital")
    test_system_data("specialized", "immune")
    test_simulate_global("normal")
