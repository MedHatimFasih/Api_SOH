import requests

BASE_URL = "http://127.0.0.1:5002/api"

ORGANS = {
    "renal": ["insuffisance", "infection"],
    "digestive": ["ulcere", "diarrhee"],
    "dermal": ["brulure", "eczema"],
    "endocrine": ["diabete", "stress"]
}

def test_status(organ):
    url = f"{BASE_URL}/{organ}/status"
    response = requests.get(url)
    print(f"\n🔵 GET /{organ}/status")
    print(response.json())


def test_data(organ):
    url = f"{BASE_URL}/{organ}/data"
    response = requests.get(url)
    print(f"\n🟢 GET /{organ}/data")
    print(response.json())


def test_parameters(organ):
    url = f"{BASE_URL}/{organ}/parameters"
    response = requests.get(url)
    print(f"\n🟣 GET /{organ}/parameters")
    print(response.json())


def test_simulate(organ, condition):
    url = f"{BASE_URL}/{organ}/simulate/{condition}"
    response = requests.post(url)
    print(f"\n🔴 POST /{organ}/simulate/{condition}")
    print(response.json())


if __name__ == "__main__":
    print("\n========== 🔥 TESTING SUPPORT API 🔥 ==========")

    for organ, conditions in ORGANS.items():
        print(f"\n==================== {organ.upper()} ====================")

        test_status(organ)
        test_data(organ)
        test_parameters(organ)

        for cond in conditions:
            test_simulate(organ, cond)

    print("\n========== ✅ TEST FINISHED SUCCESSFULLY ==========\n")
