"""
Test pour specialized_systems.py
Compatible avec la structure actuelle de l'API
"""
import requests
import json

BASE_URL = "http://localhost:5004"

def print_separator():
    print("=" * 60)

def test_connection():
    """Test 1: Connexion à l'API"""
    print("Test 1: Connexion à l'API...")
    try:
        r = requests.get(f"{BASE_URL}/", timeout=3)
        data = r.json()
        print(f"[OK] API connectée")
        print(f"     Groupe: {data.get('group')}")
        print(f"     Version: {data.get('version')}")
        print(f"     Systèmes: {', '.join(data.get('systems', []))}")
        return True
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False

def test_status(system="immune"):
    """Test 2: Récupération du status"""
    print(f"Test 2: Récupération du status de {system}...")
    try:
        r = requests.get(f"{BASE_URL}/api/{system}/status")
        data = r.json()
        print(f"[OK] Status récupéré")
        print(f"     Système: {data.get('name')}")
        print(f"     État: {data.get('current_condition')}")
        print(f"     Status: {data.get('status')}")
        return True
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False

def test_data(system="immune"):
    """Test 3: Récupération des données"""
    print(f"Test 3: Récupération des données de {system}...")
    try:
        r = requests.get(f"{BASE_URL}/api/{system}/data")
        data = r.json()
        print(f"[OK] Données récupérées")
        
        metrics = data.get('metrics', {})
        print(f"  Métriques disponibles: {len(metrics)}")
        
        # Afficher les métriques de manière sûre
        for key, value in metrics.items():
            try:
                # Gérer tous les types de valeurs correctement
                if isinstance(value, (int, float)):
                    print(f"  • {key}: {value}")
                elif isinstance(value, str):
                    print(f"  • {key}: {value}")
                elif isinstance(value, dict):
                    print(f"  • {key}: {{...}} ({len(value)} éléments)")
                elif isinstance(value, list):
                    print(f"  • {key}: [...] ({len(value)} éléments)")
                else:
                    print(f"  • {key}: {type(value).__name__}")
            except Exception as metric_error:
                print(f"  • {key}: [Erreur d'affichage: {metric_error}]")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simulation(system="immune", condition="infection"):
    """Test 4: Simulation d'une condition"""
    print(f"Test 4: Simulation de {condition} sur {system}...")
    try:
        r = requests.post(f"{BASE_URL}/api/{system}/simulate/{condition}")
        data = r.json()
        
        if data.get('success'):
            print(f"[OK] {condition.capitalize()} simulée")
            print(f"     Message: {data.get('message')}")
            
            # Afficher les nouvelles métriques de manière sûre
            new_metrics = data.get('new_metrics', {})
            if new_metrics and isinstance(new_metrics, dict):
                print(f"     Nouvelles métriques:")
                count = 0
                for key, value in new_metrics.items():
                    if count >= 3:  # Limiter à 3 métriques
                        break
                    if isinstance(value, (int, float, str)):
                        print(f"       • {key}: {value}")
                        count += 1
            return True
        else:
            print(f"[ERREUR] Simulation échouée")
            print(f"     Message: {data.get('message')}")
            return False
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False

def test_parameters(system="immune"):
    """Test 5: Récupération des paramètres"""
    print(f"Test 5: Récupération des paramètres de {system}...")
    try:
        r = requests.get(f"{BASE_URL}/api/{system}/parameters")
        data = r.json()
        print(f"[OK] Paramètres récupérés")
        
        metrics = data.get('metrics', [])
        conditions = data.get('conditions', [])
        
        print(f"     Métriques disponibles: {len(metrics)}")
        if metrics:
            print(f"       {', '.join(metrics[:4])}")
        
        print(f"     Conditions disponibles: {len(conditions)}")
        if conditions:
            print(f"       {', '.join(conditions)}")
        
        return True
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False

def test_all_systems():
    """Test 6: Tester tous les systèmes"""
    print("Test 6: Test de tous les systèmes...")
    systems = ["immune", "musculoskeletal", "hematological", "reproductive"]
    results = []
    
    for system in systems:
        try:
            r = requests.get(f"{BASE_URL}/api/{system}/status")
            if r.status_code == 200:
                data = r.json()
                print(f"  [OK] {data.get('icon')} {data.get('name'):30} - {data.get('current_condition')}")
                results.append(True)
            else:
                print(f"  [ERREUR] {system} - Code {r.status_code}")
                results.append(False)
        except Exception as e:
            print(f"  [ERREUR] {system} - {e}")
            results.append(False)
    
    return all(results)

def test_error_handling():
    """Test 7: Gestion des erreurs"""
    print("Test 7: Test gestion d'erreur...")
    try:
        # Test système invalide
        r1 = requests.get(f"{BASE_URL}/api/invalid_system/status")
        if r1.status_code == 404:
            print(f"  [OK] Système invalide géré (404)")
        
        # Test condition invalide
        r2 = requests.post(f"{BASE_URL}/api/immune/simulate/invalid_condition")
        if r2.status_code == 400:
            data = r2.json()
            print(f"  [OK] Condition invalide gérée (400)")
            print(f"       Message: {data.get('error')}")
            return True
        
        return False
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False

def test_health():
    """Test 8: Health check"""
    print("Test 8: Health check...")
    try:
        r = requests.get(f"{BASE_URL}/health")
        data = r.json()
        
        if data.get('status') == 'healthy':
            print(f"[OK] Service healthy")
            print(f"     Service: {data.get('service')}")
            print(f"     Port: {data.get('port')}")
            print(f"     Systèmes: {data.get('systems_count')}")
            return True
        else:
            print(f"[ERREUR] Service non healthy")
            return False
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False

def test_multiple_simulations():
    """Test 9: Simulations multiples"""
    print("Test 9: Simulations multiples...")
    
    scenarios = [
        ("immune", "infection"),
        ("musculoskeletal", "arthritis"),
        ("hematological", "anemia"),
        ("reproductive", "hormonal_imbalance")
    ]
    
    results = []
    for system, condition in scenarios:
        try:
            r = requests.post(f"{BASE_URL}/api/{system}/simulate/{condition}")
            data = r.json()
            if data.get('success'):
                print(f"  [OK] {system} -> {condition}")
                results.append(True)
            else:
                print(f"  [ERREUR] {system} -> {condition}")
                results.append(False)
        except Exception as e:
            print(f"  [ERREUR] {system} -> {condition}: {e}")
            results.append(False)
    
    return all(results)

def test_reset_to_normal():
    """Test 10: Retour à la normale"""
    print("Test 10: Retour à la normale...")
    systems = ["immune", "musculoskeletal", "hematological", "reproductive"]
    results = []
    
    for system in systems:
        try:
            r = requests.post(f"{BASE_URL}/api/{system}/simulate/normal")
            data = r.json()
            if data.get('success'):
                results.append(True)
            else:
                results.append(False)
        except:
            results.append(False)
    
    if all(results):
        print(f"[OK] Tous les systèmes remis à normal")
        return True
    else:
        print(f"[ERREUR] Certains systèmes non remis à normal")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print_separator()
    print("TEST DE L'API SPECIALIZED SYSTEMS")
    print_separator()
    
    # Vérifier la connexion
    try:
        requests.get(BASE_URL, timeout=2)
    except:
        print("\n[ERREUR CRITIQUE] Impossible de se connecter à l'API")
        print("Assurez-vous que specialized_systems.py est lancé sur le port 5004\n")
        print_separator()
        return
    
    results = []
    errors = []
    
    # Exécuter les tests
    tests = [
        ("Connexion", test_connection),
        ("Status", lambda: test_status("immune")),
        ("Données", lambda: test_data("immune")),
        ("Simulation", lambda: test_simulation("immune", "infection")),
        ("Paramètres", lambda: test_parameters("immune")),
        ("Tous systèmes", test_all_systems),
        ("Gestion erreurs", test_error_handling),
        ("Health check", test_health),
        ("Simulations multiples", test_multiple_simulations),
        ("Reset normal", test_reset_to_normal)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
            if not result:
                errors.append(test_name)
        except Exception as e:
            results.append(False)
            errors.append(f"{test_name}: {str(e)}")
        print()  # Ligne vide entre tests
    
    # Résumé
    print_separator()
    print("RÉSUMÉ")
    print_separator()
    
    total = len(results)
    passed = sum(results)
    failed = total - passed
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Tests réussis: {passed}/{total}")
    print(f"Taux de réussite: {percentage:.1f}%")
    
    if failed == 0:
        print("\n[SUCCÈS] Tous les tests ont réussi! 🎉")
    else:
        print(f"\n[ATTENTION] {failed} test(s) ont échoué")
        if errors:
            print("Tests échoués:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
    
    print_separator()
    
    # État final des systèmes
    print("\nÉTAT FINAL DES SYSTÈMES:")
    print("-" * 60)
    systems = ["immune", "musculoskeletal", "hematological", "reproductive"]
    for system in systems:
        try:
            r = requests.get(f"{BASE_URL}/api/{system}/status")
            data = r.json()
            icon = data.get('icon', '❓')
            name = data.get('name', system)
            condition = data.get('current_condition', 'unknown')
            print(f"  {icon} {name:30} -> {condition}")
        except:
            print(f"  ❌ {system:30} -> Erreur")
    
    print_separator()

if __name__ == "__main__":
    run_all_tests()