"""
Script de test pour l'API d'orchestration
Teste tous les endpoints principaux
"""

import requests
import json
from datetime import datetime

# ✅ CORRECTION : Port 5000 au lieu de 5001
BASE_URL = "http://localhost:5000"

def print_section(title):
    """Affiche une section avec style"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_json(data):
    """Affiche du JSON avec indentation"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_home():
    """Test de la page d'accueil"""
    print_section("Test Home")
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        print_json(response.json())
        return True
    except requests.exceptions.ConnectionError:
        print("❌ ERREUR: Serveur non accessible sur le port 5000")
        print("   → Lancez d'abord: python orchestration_api_advanced.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_health():
    """Test du endpoint health"""
    print_section("Test Health")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        response.raise_for_status()
        print_json(response.json())
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_groups_status():
    """Test du statut des groupes"""
    print_section("Test Groups Status")
    try:
        response = requests.get(f"{BASE_URL}/api/groups/status")
        response.raise_for_status()
        data = response.json()
        print_json(data)
        
        # Analyse
        summary = data.get('summary', {})
        print(f"\n📊 Résumé:")
        print(f"   Total groupes: {summary.get('total_groups', 0)}")
        print(f"   Groupes en ligne: {summary.get('online_groups', 0)}")
        print(f"   Santé globale: {summary.get('health_percentage', 0):.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_systems_status():
    """Test du statut des systèmes"""
    print_section("Test Systems Status")
    try:
        response = requests.get(f"{BASE_URL}/api/systems/status")
        response.raise_for_status()
        data = response.json()
        
        summary = data.get('summary', {})
        print(f"📊 Résumé:")
        print(f"   Total systèmes: {summary.get('total_systems', 0)}")
        print(f"   Systèmes en ligne: {summary.get('online_systems', 0)}")
        print(f"   Systèmes hors ligne: {summary.get('offline_systems', 0)}")
        print(f"   Critiques hors ligne: {summary.get('critical_offline', 0)}")
        print(f"   Santé globale: {summary.get('health_percentage', 0):.1f}%")
        
        # Détails par groupe
        print("\n📋 Détails par groupe:")
        for group_name, systems in data.get('by_group', {}).items():
            print(f"\n   {group_name.upper()}:")
            for system in systems:
                status_icon = "✅" if system['status'] == 'online' else "❌"
                print(f"      {status_icon} {system['system']}: {system['status']}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_dashboard():
    """Test du dashboard"""
    print_section("Test Dashboard")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard")
        response.raise_for_status()
        data = response.json()
        
        overview = data.get('overview', {})
        print(f"📊 Vue d'ensemble:")
        print(f"   Total groupes: {overview.get('total_groups', 0)}")
        print(f"   Total systèmes: {overview.get('total_systems', 0)}")
        print(f"   Systèmes en ligne: {overview.get('online_systems', 0)}")
        print(f"   Santé: {overview.get('health_percentage', 0):.1f}%")
        print(f"   Critiques hors ligne: {overview.get('critical_offline', 0)}")
        
        # Alertes récentes
        alerts = data.get('recent_alerts', [])
        if alerts:
            print(f"\n🚨 Alertes récentes ({len(alerts)}):")
            for alert in alerts[-5:]:  # Afficher les 5 dernières
                print(f"   [{alert.get('level', 'info').upper()}] {alert.get('message', 'N/A')}")
        else:
            print("\n✅ Aucune alerte")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_metrics():
    """Test des métriques"""
    print_section("Test Metrics")
    try:
        response = requests.get(f"{BASE_URL}/api/metrics")
        response.raise_for_status()
        data = response.json()
        
        # Statuts
        status_counts = data.get('systems_by_status', {})
        print(f"📊 Systèmes par statut:")
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
        
        # Performance
        perf = data.get('performance', {})
        print(f"\n⚡ Performance:")
        print(f"   Temps de réponse moyen: {perf.get('average_response_time_ms', 0):.2f} ms")
        print(f"   Plus rapide: {perf.get('fastest_response_ms', 0)} ms")
        print(f"   Plus lent: {perf.get('slowest_response_ms', 0)} ms")
        
        # Alertes
        alert_stats = data.get('alerts', {})
        print(f"\n🚨 Statistiques alertes:")
        print(f"   Total: {alert_stats.get('total', 0)}")
        by_level = alert_stats.get('by_level', {})
        for level, count in by_level.items():
            print(f"   {level}: {count}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_group_detail():
    """Test des détails d'un groupe"""
    print_section("Test Group Detail: specialized")
    try:
        response = requests.get(f"{BASE_URL}/api/group/specialized")
        response.raise_for_status()
        data = response.json()
        
        print(f"📦 Groupe: {data.get('name', 'N/A')}")
        print(f"   Description: {data.get('description', 'N/A')}")
        print(f"   URL: {data.get('url', 'N/A')}")
        print(f"   Priorité: {data.get('priority', 'N/A')}")
        
        summary = data.get('summary', {})
        print(f"\n📊 Résumé:")
        print(f"   Total systèmes: {summary.get('total_systems', 0)}")
        print(f"   En ligne: {summary.get('online_systems', 0)}")
        print(f"   Santé: {summary.get('health_percentage', 0):.1f}%")
        
        print("\n🔧 Systèmes:")
        for sys_name, sys_data in data.get('systems', {}).items():
            status_icon = "✅" if sys_data.get('status') == 'online' else "❌"
            print(f"   {status_icon} {sys_name}: {sys_data.get('status', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_system_detail():
    """Test des détails d'un système"""
    print_section("Test System Detail: specialized/immune")
    try:
        response = requests.get(f"{BASE_URL}/api/system/specialized/immune")
        response.raise_for_status()
        data = response.json()
        
        print(f"🔧 Système: {data.get('name', 'N/A')} {data.get('icon', '')}")
        print(f"   Groupe: {data.get('group', 'N/A')}")
        print(f"   Critique: {'Oui' if data.get('critical') else 'Non'}")
        
        status = data.get('status', {})
        print(f"\n📊 Statut:")
        print(f"   État: {status.get('status', 'unknown')}")
        print(f"   Santé: {status.get('health_status', 'unknown')}")
        
        if data.get('data'):
            print(f"\n✅ Données disponibles")
        elif data.get('error'):
            print(f"\n❌ Erreur: {data.get('error')}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_simulate():
    """Test de simulation"""
    print_section("Test Simulate: specialized/immune -> infection")
    try:
        payload = {"condition": "infection"}
        response = requests.post(
            f"{BASE_URL}/api/simulate/specialized/immune",
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Simulation réussie!")
            print(f"   Groupe: {data.get('group', 'N/A')}")
            print(f"   Système: {data.get('system', 'N/A')}")
            print(f"   Condition: {data.get('condition', 'N/A')}")
        else:
            print(f"❌ Échec de la simulation")
            print(f"   Erreur: {data.get('error', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_batch_simulate():
    """Test de simulation batch"""
    print_section("Test Batch Simulate")
    try:
        payload = {
            "simulations": [
                {"group": "specialized", "system": "immune", "condition": "infection"},
                {"group": "specialized", "system": "musculoskeletal", "condition": "arthritis"},
                {"group": "specialized", "system": "hematological", "condition": "anemia"}
            ]
        }
        response = requests.post(
            f"{BASE_URL}/api/simulate/batch",
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"📊 Résultats:")
        print(f"   Total simulations: {data.get('total_simulations', 0)}")
        print(f"   Réussies: {data.get('successful', 0)}")
        print(f"   Échouées: {data.get('failed', 0)}")
        
        print("\n📋 Détails:")
        for result in data.get('results', []):
            status_icon = "✅" if result.get('success') else "❌"
            print(f"   {status_icon} {result.get('system', 'N/A')}: {result.get('condition', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("  🧪 SUITE DE TESTS - ORCHESTRATION API")
    print("="*60)
    print(f"  Timestamp: {datetime.now().isoformat()}")
    print(f"  URL de base: {BASE_URL}")
    print("="*60)
    
    tests = [
        ("Home", test_home),
        ("Health", test_health),
        ("Groups Status", test_groups_status),
        ("Systems Status", test_systems_status),
        ("Dashboard", test_dashboard),
        ("Metrics", test_metrics),
        ("Group Detail", test_group_detail),
        ("System Detail", test_system_detail),
        ("Simulate", test_simulate),
        ("Batch Simulate", test_batch_simulate)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Erreur critique dans {name}: {e}")
            results.append((name, False))
    
    # Résumé final
    print_section("RÉSUMÉ DES TESTS")
    total = len(results)
    passed = sum(1 for _, success in results if success)
    failed = total - passed
    
    print(f"\n📊 Résultats:")
    print(f"   Total: {total}")
    print(f"   ✅ Réussis: {passed}")
    print(f"   ❌ Échoués: {failed}")
    print(f"   📈 Taux de réussite: {(passed/total*100):.1f}%")
    
    print("\n📋 Détails:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print("\n" + "="*60)
    if failed == 0:
        print("  🎉 TOUS LES TESTS ONT RÉUSSI!")
    else:
        print("  ⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()