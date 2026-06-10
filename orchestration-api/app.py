"""
API D'ORCHESTRATION AVANCÉE v2.0
Coordonne les 12 systèmes d'organes humains répartis en 3 groupes
Compatible avec tous les endpoints de test
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
import concurrent.futures
import time
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# ===================== CONFIGURATION DES 3 GROUPES =======================

GROUPS_CONFIG = {
    "vital": {
        "name": "Groupe Vital",
        "description": "Systèmes essentiels à la survie immédiate",
        "url": "http://localhost:5003",
        "priority": 1,
        "color": "🔴",
        "systems": {
            "cardiac": {"name": "Cœur", "icon": "❤️", "critical": True},
            "respiratory": {"name": "Poumons", "icon": "🫁", "critical": True},
            "neural": {"name": "Cerveau", "icon": "🧠", "critical": True},
            "hepatic": {"name": "Foie", "icon": "🟤", "critical": False}
        }
    },
    "support": {
        "name": "Groupe Support",
        "description": "Systèmes de régulation et maintien",
        "url": "http://localhost:5002",
        "priority": 2,
        "color": "🟢",
        "systems": {
            "renal": {"name": "Reins", "icon": "🫘", "critical": False},
            "digestive": {"name": "Système Digestif", "icon": "🫃", "critical": False},
            "dermal": {"name": "Peau", "icon": "🤚", "critical": False},
            "endocrine": {"name": "Système Endocrinien", "icon": "⚗️", "critical": False},
            "lymphatic": {"name": "Système Lymphatique", "icon": "💚", "critical": False}
        }
    },
    "specialized": {
        "name": "Groupe Spécialisé",
        "description": "Systèmes spécialisés et défense",
        "url": "http://localhost:5004",
        "priority": 3,
        "color": "🔵",
        "systems": {
            "immune": {"name": "Système Immunitaire", "icon": "🛡️", "critical": False},
            "musculoskeletal": {"name": "Système Musculosquelettique", "icon": "💪", "critical": False},
            "hematological": {"name": "Système Sanguin", "icon": "🩸", "critical": True},
            "reproductive": {"name": "Système Reproductif", "icon": "👶", "critical": False}
        }
    }
}

TIMEOUT = 5
request_cache = {}
alerts_log = []

# ===================== FONCTIONS UTILITAIRES =======================

def get_critical_systems():
    """Retourne la liste des systèmes critiques"""
    critical = []
    for group_name, group in GROUPS_CONFIG.items():
        for sys_name, sys_info in group["systems"].items():
            if sys_info.get("critical", False):
                critical.append({
                    "group": group_name,
                    "system": sys_name,
                    "name": sys_info["name"],
                    "icon": sys_info["icon"]
                })
    return critical

def check_system_status(group_name, system_name):
    """Vérifie le statut d'un système spécifique"""
    try:
        group = GROUPS_CONFIG[group_name]
        url = f"{group['url']}/api/{system_name}/status"
        
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "group": group_name,
                "system": system_name,
                "status": "online",
                "health_status": data.get("health_status", "unknown"),
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                "data": data
            }
        else:
            return {
                "group": group_name,
                "system": system_name,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
    except requests.exceptions.ConnectionError:
        return {
            "group": group_name,
            "system": system_name,
            "status": "offline",
            "error": "Connection refused"
        }
    except Exception as e:
        return {
            "group": group_name,
            "system": system_name,
            "status": "error",
            "error": str(e)
        }

def get_system_data(group_name, system_name):
    """Récupère les données d'un système"""
    try:
        group = GROUPS_CONFIG[group_name]
        url = f"{group['url']}/api/{system_name}/data"
        
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return {
                "success": True,
                "group": group_name,
                "system": system_name,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "group": group_name,
                "system": system_name,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "group": group_name,
            "system": system_name,
            "error": str(e)
        }

def simulate_system_condition(group_name, system_name, condition):
    """Simule une condition sur un système"""
    try:
        group = GROUPS_CONFIG[group_name]
        url = f"{group['url']}/api/{system_name}/simulate/{condition}"
        
        response = requests.post(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return {
                "success": True,
                "group": group_name,
                "system": system_name,
                "condition": condition,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "group": group_name,
                "system": system_name,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "group": group_name,
            "system": system_name,
            "error": str(e)
        }

def add_alert(level, message, group=None, system=None):
    """Ajoute une alerte au log"""
    alert = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
        "group": group,
        "system": system
    }
    alerts_log.append(alert)
    
    # Garder seulement les 100 dernières alertes
    if len(alerts_log) > 100:
        alerts_log.pop(0)
    
    return alert

# ===================== ENDPOINTS =======================

@app.route('/')
def home():
    """Page d'accueil avec architecture complète"""
    critical_systems = get_critical_systems()
    
    return jsonify({
        "api": "Orchestration Globale Avancée - 12 Systèmes Corporels",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "architecture": {
            "groups": len(GROUPS_CONFIG),
            "total_systems": sum(len(g["systems"]) for g in GROUPS_CONFIG.values()),
            "critical_systems": len(critical_systems)
        },
        "groups": {
            group_name: {
                "name": group["name"],
                "description": group["description"],
                "url": group["url"],
                "priority": group["priority"],
                "systems_count": len(group["systems"])
            }
            for group_name, group in GROUPS_CONFIG.items()
        },
        "endpoints": {
            "health": "/api/health",
            "groups_status": "/api/groups/status",
            "systems_status": "/api/systems/status",
            "dashboard": "/api/dashboard",
            "metrics": "/api/metrics",
            "alerts": "/api/alerts",
            "group_detail": "/api/group/<group_name>",
            "system_detail": "/api/system/<group_name>/<system_name>",
            "simulate": "/api/simulate/<group_name>/<system_name>",
            "batch_simulate": "/api/simulate/batch"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Santé globale de l'API d'orchestration"""
    return jsonify({
        "service": "Orchestration API",
        "status": "healthy",
        "uptime": "operational",
        "timestamp": datetime.now().isoformat(),
        "groups_configured": len(GROUPS_CONFIG),
        "cache_size": len(request_cache)
    })

@app.route('/api/groups/status', methods=['GET'])
def groups_status():
    """Statut de tous les groupes"""
    results = {}
    
    for group_name, group in GROUPS_CONFIG.items():
        try:
            # Test de connexion au groupe
            first_system = list(group["systems"].keys())[0]
            url = f"{group['url']}/api/{first_system}/status"
            response = requests.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                results[group_name] = {
                    "status": "online",
                    "name": group["name"],
                    "url": group["url"],
                    "systems_count": len(group["systems"]),
                    "response_time_ms": int(response.elapsed.total_seconds() * 1000)
                }
            else:
                results[group_name] = {
                    "status": "error",
                    "name": group["name"],
                    "error": f"HTTP {response.status_code}"
                }
        except requests.exceptions.ConnectionError:
            results[group_name] = {
                "status": "offline",
                "name": group["name"],
                "url": group["url"],
                "error": "Connection refused"
            }
            add_alert("error", f"Groupe {group['name']} hors ligne", group=group_name)
        except Exception as e:
            results[group_name] = {
                "status": "error",
                "name": group["name"],
                "error": str(e)
            }
    
    # Calculer statistiques
    total_groups = len(results)
    online_groups = sum(1 for g in results.values() if g["status"] == "online")
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_groups": total_groups,
            "online_groups": online_groups,
            "offline_groups": total_groups - online_groups,
            "health_percentage": (online_groups / total_groups * 100) if total_groups > 0 else 0
        },
        "groups": results
    })

@app.route('/api/systems/status', methods=['GET'])
def systems_status():
    """Statut détaillé de tous les systèmes"""
    tasks = []
    for group_name, group in GROUPS_CONFIG.items():
        for system_name in group["systems"].keys():
            tasks.append((group_name, system_name))
    
    # Vérifier tous les systèmes en parallèle
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(check_system_status, group_name, system_name): (group_name, system_name)
            for group_name, system_name in tasks
        }
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    # Organiser par groupe
    by_group = defaultdict(list)
    for result in results:
        by_group[result["group"]].append(result)
    
    # Statistiques
    total_systems = len(results)
    online_systems = sum(1 for r in results if r["status"] == "online")
    
    # Vérifier les systèmes critiques
    critical_offline = []
    for result in results:
        group = GROUPS_CONFIG[result["group"]]
        system_info = group["systems"][result["system"]]
        if system_info.get("critical") and result["status"] != "online":
            critical_offline.append(result)
            add_alert("critical", f"Système critique hors ligne: {system_info['name']}", 
                     group=result["group"], system=result["system"])
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_systems": total_systems,
            "online_systems": online_systems,
            "offline_systems": total_systems - online_systems,
            "critical_offline": len(critical_offline),
            "health_percentage": (online_systems / total_systems * 100) if total_systems > 0 else 0
        },
        "by_group": dict(by_group),
        "critical_systems_status": critical_offline if critical_offline else "All critical systems online"
    })

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Dashboard complet avec métriques en temps réel"""
    # Récupérer le statut de tous les systèmes
    systems_response = systems_status()
    systems_data = systems_response.get_json()
    
    # Récupérer le statut des groupes
    groups_response = groups_status()
    groups_data = groups_response.get_json()
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "overview": {
            "total_groups": len(GROUPS_CONFIG),
            "total_systems": systems_data["summary"]["total_systems"],
            "online_systems": systems_data["summary"]["online_systems"],
            "health_percentage": systems_data["summary"]["health_percentage"],
            "critical_offline": systems_data["summary"]["critical_offline"]
        },
        "groups_health": groups_data["groups"],
        "systems_health": systems_data["by_group"],
        "recent_alerts": alerts_log[-10:] if alerts_log else []
    })

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Métriques détaillées du système"""
    # Compter les systèmes par état
    systems_response = systems_status()
    systems_data = systems_response.get_json()
    
    status_counts = defaultdict(int)
    response_times = []
    
    for group_systems in systems_data["by_group"].values():
        for system in group_systems:
            status_counts[system["status"]] += 1
            if "response_time_ms" in system:
                response_times.append(system["response_time_ms"])
    
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "systems_by_status": dict(status_counts),
        "performance": {
            "average_response_time_ms": round(avg_response_time, 2),
            "fastest_response_ms": min(response_times) if response_times else 0,
            "slowest_response_ms": max(response_times) if response_times else 0
        },
        "alerts": {
            "total": len(alerts_log),
            "by_level": {
                "critical": sum(1 for a in alerts_log if a["level"] == "critical"),
                "error": sum(1 for a in alerts_log if a["level"] == "error"),
                "warning": sum(1 for a in alerts_log if a["level"] == "warning"),
                "info": sum(1 for a in alerts_log if a["level"] == "info")
            }
        }
    })

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Liste des alertes récentes"""
    limit = request.args.get('limit', 50, type=int)
    level = request.args.get('level', None, type=str)
    
    filtered_alerts = alerts_log
    
    if level:
        filtered_alerts = [a for a in alerts_log if a["level"] == level]
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "total_alerts": len(alerts_log),
        "filtered_count": len(filtered_alerts),
        "alerts": filtered_alerts[-limit:]
    })

@app.route('/api/group/<group_name>', methods=['GET'])
def get_group_detail(group_name):
    """Détails complets d'un groupe"""
    if group_name not in GROUPS_CONFIG:
        return jsonify({
            "error": "Groupe non trouvé",
            "available_groups": list(GROUPS_CONFIG.keys()),
            "timestamp": datetime.now().isoformat(),
            "status": 404
        }), 404
    
    group = GROUPS_CONFIG[group_name]
    
    # Récupérer le statut de tous les systèmes du groupe
    systems_data = {}
    for system_name in group["systems"].keys():
        status = check_system_status(group_name, system_name)
        systems_data[system_name] = status
    
    online_count = sum(1 for s in systems_data.values() if s["status"] == "online")
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "group": group_name,
        "name": group["name"],
        "description": group["description"],
        "url": group["url"],
        "priority": group["priority"],
        "summary": {
            "total_systems": len(group["systems"]),
            "online_systems": online_count,
            "health_percentage": (online_count / len(group["systems"]) * 100)
        },
        "systems": systems_data
    })

@app.route('/api/system/<group_name>/<system_name>', methods=['GET'])
def get_system_detail(group_name, system_name):
    """Détails complets d'un système spécifique"""
    if group_name not in GROUPS_CONFIG:
        return jsonify({
            "error": "Groupe non trouvé",
            "timestamp": datetime.now().isoformat(),
            "status": 404
        }), 404
    
    if system_name not in GROUPS_CONFIG[group_name]["systems"]:
        return jsonify({
            "error": "Système non trouvé",
            "timestamp": datetime.now().isoformat(),
            "status": 404
        }), 404
    
    # Récupérer le statut
    status = check_system_status(group_name, system_name)
    
    # Récupérer les données
    data = get_system_data(group_name, system_name)
    
    system_info = GROUPS_CONFIG[group_name]["systems"][system_name]
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "group": group_name,
        "system": system_name,
        "name": system_info["name"],
        "icon": system_info["icon"],
        "critical": system_info.get("critical", False),
        "status": status,
        "data": data.get("data") if data.get("success") else None,
        "error": data.get("error") if not data.get("success") else None
    })

@app.route('/api/simulate/<group_name>/<system_name>', methods=['POST'])
def simulate_system(group_name, system_name):
    """Simule une condition sur un système"""
    if group_name not in GROUPS_CONFIG:
        return jsonify({
            "error": "Groupe non trouvé",
            "timestamp": datetime.now().isoformat(),
            "status": 404
        }), 404
    
    if system_name not in GROUPS_CONFIG[group_name]["systems"]:
        return jsonify({
            "error": "Système non trouvé",
            "timestamp": datetime.now().isoformat(),
            "status": 404
        }), 404
    
    # Récupérer la condition depuis le body JSON
    data = request.get_json() or {}
    condition = data.get('condition', 'normal')
    
    result = simulate_system_condition(group_name, system_name, condition)
    
    if result["success"]:
        add_alert("info", f"Simulation lancée: {system_name} -> {condition}", 
                 group=group_name, system=system_name)
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        **result
    })

@app.route('/api/simulate/batch', methods=['POST'])
def simulate_batch():
    """Simule plusieurs conditions en parallèle"""
    data = request.get_json()
    
    if not data or "simulations" not in data:
        return jsonify({
            "error": "Format invalide. Attendu: {\"simulations\": [{\"group\": \"...\", \"system\": \"...\", \"condition\": \"...\"}]}",
            "timestamp": datetime.now().isoformat(),
            "status": 400
        }), 400
    
    simulations = data["simulations"]
    results = []
    
    for sim in simulations:
        group = sim.get("group")
        system = sim.get("system")
        condition = sim.get("condition", "normal")
        
        if group and system:
            result = simulate_system_condition(group, system, condition)
            results.append(result)
    
    success_count = sum(1 for r in results if r["success"])
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "total_simulations": len(results),
        "successful": success_count,
        "failed": len(results) - success_count,
        "results": results
    })

# ===================== GESTION DES ERREURS =======================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint non trouvé",
        "timestamp": datetime.now().isoformat(),
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Erreur interne du serveur",
        "message": str(error),
        "timestamp": datetime.now().isoformat(),
        "status": 500
    }), 500

# ===================== LANCEMENT =======================

if __name__ == '__main__':
    print("="*80)
    print(" "*15 + "🏥 ORCHESTRATION AVANCÉE - 12 SYSTÈMES CORPORELS 🏥")
    print("="*80)
    print(f"\n✅ Version: 2.0")
    print(f"✅ Port d'écoute: 5000")
    print(f"✅ Total de systèmes gérés: {sum(len(g['systems']) for g in GROUPS_CONFIG.values())}")
    print(f"✅ Groupes configurés: {len(GROUPS_CONFIG)}")
    print(f"✅ Systèmes critiques: {len(get_critical_systems())}")
    print("\n📋 Groupes d'APIs requis:")
    for group_name, group in GROUPS_CONFIG.items():
        print(f"   {group['color']} {group['name']:25} → {group['url']:25} ({len(group['systems'])} systèmes)")
    print("\n" + "="*80)
    print("🌐 Accès API: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/api/dashboard")
    print("🚨 Alertes: http://localhost:5000/api/alerts")
    print("📈 Métriques: http://localhost:5000/api/metrics")
    print("="*80 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')