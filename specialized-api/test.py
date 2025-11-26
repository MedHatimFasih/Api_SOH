import sys
import io
import requests
import json
from datetime import datetime

# Force l'encodage UTF-8 pour Windows
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except AttributeError:
    pass  # Déjà en UTF-8

BASE_URL = "http://localhost:5004"

def print_separator():
    print("=" * 60)

def print_test_header(test_num, description):
    print(f"\nTest {test_num}: {description}...")

def test_api():
    """Test complet de l'API Immune System"""
    print_separator()
    print("TEST DE L'API IMMUNE SYSTEM")
    print_separator()
    
    results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    # Test 1: Connexion à l'API
    print_test_header(1, "Connexion à l'API")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("[OK] API connectée")
            print(f"     Version: {response.json().get('version', 'N/A')}")
            results["passed"] += 1
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"[ERREUR] {e}")
        results["failed"] += 1
        results["errors"].append(str(e))
    
    # Test 2: Récupération du status
    print_test_header(2, "Récupération du status")
    try:
        response = requests.get(f"{BASE_URL}/api/immune/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("[OK] Status récupéré")
            print(f"     État: {data.get('health_status', 'N/A')}")
            print(f"     Conditions actives: {len(data.get('active_conditions', []))}")
            results["passed"] += 1
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"[ERREUR] {e}")
        results["failed"] += 1
        results["errors"].append(str(e))
    
    # Test 3: Récupération des données
    print_test_header(3, "Récupération des données")
    try:
        response = requests.get(f"{BASE_URL}/api/immune/data", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("[OK] Données récupérées")
            wbc = data.get('white_blood_cells', {})
            print(f"     Leucocytes: {wbc.get('total_count', 'N/A')} {wbc.get('unit', '')}")
            temp = data.get('inflammation', {}).get('temperature', 'N/A')
            print(f"     Température: {temp}°C")
            results["passed"] += 1
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"[ERREUR] {e}")
        results["failed"] += 1
        results["errors"].append(str(e))
    
    # Test 4: Simulation d'infection
    print_test_header(4, "Simulation d'infection")
    try:
        response = requests.post(f"{BASE_URL}/api/immune/simulate/infection", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("[OK] Infection simulée")
            print(f"     Message: {data.get('message', 'N/A')}")
            current = data.get('current_data', {})
            wbc = current.get('white_blood_cells', {})
            print(f"     Leucocytes: {wbc.get('total_count', 'N/A')} (augmentés)")
            results["passed"] += 1
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"[ERREUR] {e}")
        results["failed"] += 1
        results["errors"].append(str(e))
    
    # Test 5: Récupération des paramètres
    print_test_header(5, "Récupération des paramètres")
    try:
        response = requests.get(f"{BASE_URL}/api/immune/parameters", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("[OK] Paramètres récupérés")
            conditions = data.get('available_conditions', {})
            print(f"     Conditions disponibles: {len(conditions)}")
            for condition in list(conditions.keys())[:3]:
                print(f"       - {condition}")
            results["passed"] += 1
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"[ERREUR] {e}")
        results["failed"] += 1
        results["errors"].append(str(e))
    
    # Test 6: Configuration du patient
    print_test_header(6, "Configuration du patient")
    try:
        config_data = {
            "age": 45,
            "sex": "F",
            "health_status": "normal"
        }
        response = requests.post(
            f"{BASE_URL}/api/immune/configure",
            json=config_data,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("[OK] Configuration mise à jour")
            config = data.get('current_config', {})
            print(f"     Âge: {config.get('age')} ans")
            print(f"     Sexe: {config.get('sex')}")
            print(f"     État: {config.get('health_status')}")
            results["passed"] += 1
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"[ERREUR] {e}")
        results["failed"] += 1
        results["errors"].append(str(e))
    
    # Test 7: Test d'erreur (condition invalide)
    print_test_header(7, "Test gestion d'erreur")
    try:
        response = requests.post(f"{BASE_URL}/api/immune/simulate/invalid_condition", timeout=5)
        if response.status_code == 400:
            print("[OK] Erreur correctement gérée")
            print(f"     Message: {response.json().get('error', 'N/A')}")
            results["passed"] += 1
        else:
            print(f"[ERREUR] Code attendu 400, reçu {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"[ERREUR] {e}")
        results["failed"] += 1
        results["errors"].append(str(e))
    
    # Affichage du résumé
    print_separator()
    print("RÉSUMÉ")
    print_separator()
    total = results["passed"] + results["failed"]
    success_rate = (results["passed"] / total * 100) if total > 0 else 0
    
    print(f"Tests réussis: {results['passed']}/{total}")
    print(f"Taux de réussite: {success_rate:.1f}%")
    
    if results["failed"] > 0:
        print(f"\n[ATTENTION] {results['failed']} test(s) ont échoué")
        if results["errors"]:
            print("\nErreurs détectées:")
            for i, error in enumerate(results["errors"], 1):
                print(f"  {i}. {error}")
    else:
        print("\n[SUCCÈS] Tous les tests sont passés!")
    
    print_separator()
    
    return results

def test_endpoint_manually(endpoint):
    """Test manuel d'un endpoint spécifique"""
    print(f"\nTest manuel: {endpoint}")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        print(f"Status: {response.status_code}")
        print("Réponse:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    # Test automatique
    test_api()
    
    # Exemples de tests manuels (décommentez si besoin)
    # test_endpoint_manually("/")
    # test_endpoint_manually("/api/immune/status")
    # test_endpoint_manually("/api/immune/data")