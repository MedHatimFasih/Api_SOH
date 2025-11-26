"""
Suite de tests simple pour l'API (sans dépendances externes)
"""

import requests
import json

BASE_URL = "http://localhost:5004"

def test_api():
    print("\n" + "="*60)
    print("TEST DE L'API IMMUNE SYSTEM")
    print("="*60 + "\n")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Connexion
    print("Test 1: Connexion à l'API...")
    tests_total += 1
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            print("✓ API connectée")
            print(f"  Nom: {r.json()['api']}")
            tests_passed += 1
        else:
            print(f"✗ Erreur: Status {r.status_code}")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    # Test 2: Status
    print("\nTest 2: Récupération du status...")
    tests_total += 1
    try:
        r = requests.get(f"{BASE_URL}/api/immune/status")
        if r.status_code == 200:
            data = r.json()
            print("✓ Status récupéré")
            print(f"  État: {data['health_status']}")
            tests_passed += 1
        else:
            print(f"✗ Erreur: Status {r.status_code}")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    # Test 3: Données
    print("\nTest 3: Récupération des données...")
    tests_total += 1
    try:
        r = requests.get(f"{BASE_URL}/api/immune/data")
        if r.status_code == 200:
            data = r.json()
            print("✓ Données récupérées")
            print(f"  Globules blancs: {data['white_blood_cells']['total_count']}")
            print(f"  Température: {data['inflammation']['temperature']}°C")
            tests_passed += 1
        else:
            print(f"✗ Erreur: Status {r.status_code}")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    # Test 4: Simulation
    print("\nTest 4: Simulation d'infection...")
    tests_total += 1
    try:
        r = requests.post(f"{BASE_URL}/api/immune/simulate/infection")
        if r.status_code == 200:
            data = r.json()
            print("✓ Simulation réussie")
            print(f"  Message: {data['message']}")
            tests_passed += 1
        else:
            print(f"✗ Erreur: Status {r.status_code}")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    # Test 5: Paramètres
    print("\nTest 5: Récupération des paramètres...")
    tests_total += 1
    try:
        r = requests.get(f"{BASE_URL}/api/immune/parameters")
        if r.status_code == 200:
            data = r.json()
            conditions = len(data['available_conditions'])
            print("✓ Paramètres récupérés")
            print(f"  Conditions disponibles: {conditions}")
            tests_passed += 1
        else:
            print(f"✗ Erreur: Status {r.status_code}")
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    print(f"Tests réussis: {tests_passed}/{tests_total}")
    print(f"Taux de réussite: {(tests_passed/tests_total)*100:.1f}%")
    
    if tests_passed == tests_total:
        print("\n✓ TOUS LES TESTS SONT PASSÉS!")
    else:
        print(f"\n✗ {tests_total - tests_passed} test(s) ont échoué")
    print()

if __name__ == "__main__":
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\nTests interrompus")