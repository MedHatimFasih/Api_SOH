"""
API D'ORCHESTRATION GLOBALE
Coordonne les 12 systèmes d'organes humains
- Groupe VITAL (4 organes)
- Groupe SUPPORT (4 organes)
- Groupe SPECIALIZED (4 organes)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
import concurrent.futures
import time

app = Flask(__name__)
CORS(app)

# ===================== CONFIGURATION DES 3 GROUPES =======================

APIS_CONFIG = {
    # ========== GROUPE VITAL (Port 5003) ==========
    "vital": {
        "name": "Groupe Vital",
        "url": "http://localhost:5003",
        "color": "🔴",
        "systems": {
            "cardiac": {
                "name": "Cœur",
                "icon": "❤️",
                "endpoints": {
                    "status": "/api/cardiac/status",
                    "data": "/api/cardiac/data",
                    "simulate": "/api/cardiac/simulate",
                    "parameters": "/api/cardiac/parameters"
                }
            },
            "respiratory": {
                "name": "Poumons",
                "icon": "🫁",
                "endpoints": {
                    "status": "/api/respiratory/status",
                    "data": "/api/respiratory/data",
                    "simulate": "/api/respiratory/simulate",
                    "parameters": "/api/respiratory/parameters"
                }
            },
            "neural": {
                "name": "Cerveau",
                "icon": "🧠",
                "endpoints": {
                    "status": "/api/neural/status",
                    "data": "/api/neural/data",
                    "simulate": "/api/neural/simulate",
                    "parameters": "/api/neural/parameters"
                }
            },
            "hepatic": {
                "name": "Foie",
                "icon": "🟤",
                "endpoints": {
                    "status": "/api/hepatic/status",
                    "data": "/api/hepatic/data",
                    "simulate": "/api/hepatic/simulate",
                    "parameters": "/api/hepatic/parameters"
                }
            }
        }
    },
    
    # ========== GROUPE SUPPORT (Port 5002) ==========
    "support": {
        "name": "Groupe Support",
        "url": "http://localhost:5002",
        "color": "🟢",
        "systems": {
            "renal": {
                "name": "Reins",
                "icon": "🫘",
                "endpoints": {
                    "status": "/api/renal/status",
                    "data": "/api/renal/data",
                    "simulate": "/api/renal/simulate",
                    "parameters": "/api/renal/parameters"
                }
            },
            "digestive": {
                "name": "Système Digestif",
                "icon": "🫃",
                "endpoints": {
                    "status": "/api/digestive/status",
                    "data": "/api/digestive/data",
                    "simulate": "/api/digestive/simulate",
                    "parameters": "/api/digestive/parameters"
                }
            },
            "dermal": {
                "name": "Peau",
                "icon": "🤚",
                "endpoints": {
                    "status": "/api/dermal/status",
                    "data": "/api/dermal/data",
                    "simulate": "/api/dermal/simulate",
                    "parameters": "/api/dermal/parameters"
                }
            },
            "endocrine": {
                "name": "Système Endocrinien",
                "icon": "⚗️",
                "endpoints": {
                    "status": "/api/endocrine/status",
                    "data": "/api/endocrine/data",
                    "simulate": "/api/endocrine/simulate",
                    "parameters": "/api/endocrine/parameters"
                }
            }
        }
    },
    
    # ========== GROUPE SPECIALIZED (Port 5004) ==========
    "specialized": {
        "name": "Groupe Spécialisé",
        "url": "http://localhost:5004",
        "color": "🔵",
        "systems": {
            "immune": {
                "name": "Système Immunitaire",
                "icon": "🛡️",
                "endpoints": {
                    "status": "/api/immune/status",
                    "data": "/api/immune/data",
                    "simulate": "/api/immune/simulate",
                    "parameters": "/api/immune/parameters"
                }
            },
            "musculoskeletal": {
                "name": "Système Musculosquelettique",
                "icon": "💪",
                "endpoints": {
                    "status": "/api/musculoskeletal/status",
                    "data": "/api/musculoskeletal/data",
                    "simulate": "/api/musculoskeletal/simulate",
                    "parameters": "/api/musculoskeletal/parameters"
                }
            },
            "hematological": {
                "name": "Système Sanguin",
                "icon": "🩸",
                "endpoints": {
                    "status": "/api/hematological/status",
                    "data": "/api/hematological/data",
                    "simulate": "/api/hematological/simulate",
                    "parameters": "/api/hematological/parameters"
                }
            },
            "reproductive": {
                "name": "Système Reproductif",
                "icon": "👶",
                "endpoints": {
                    "status": "/api/reproductive/status",
                    "data": "/api/reproductive/data",
                    "simulate": "/api/reproductive/simulate",
                    "parameters": "/api/reproductive/parameters"
                }
            }
        }
    }
}

TIMEOUT = 5

# ===================== FONCTIONS UTILITAIRES =======================

def check_group_health(group_key, group_config):
    """Vérifie la santé d'un groupe entier (API)"""
    try:
        # Test simple sur le premier système du groupe
        first_system = list(group_config["systems"].keys())[0]
        endpoint = group_config["systems"][first_system]["endpoints"]["status"]
        url = group_config["url"] + endpoint
        
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return {
                "group": group_key,
                "name": group_config["name"],
                "status": "online",
                "url": group_config["url"],
                "systems_count": len(group_config["systems"]),
                "response_time": response.elapsed.total_seconds()
            }
        else:
            return {
                "group": group_key,
                "name": group_config["name"],
                "status": "error",
                "url": group_config["url"],
                "error": f"Status code: {response.status_code}"
            }
    except requests.exceptions.ConnectionError:
        return {
            "group": group_key,
            "name": group_config["name"],
            "status": "offline",
            "url": group_config["url"],
            "error": "Connexion impossible"
        }
    except Exception as e:
        return {
            "group": group_key,
            "name": group_config["name"],
            "status": "error",
            "url": group_config["url"],
            "error": str(e)
        }

def check_system_health(group_key, system_key, group_config, system_config):
    """Vérifie la santé d'un système spécifique"""
    try:
        url = group_config["url"] + system_config["endpoints"]["status"]
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return {
                "group": group_key,
                "system": system_key,
                "name": system_config["name"],
                "icon": system_config["icon"],
                "status": "online",
                "response_time": response.elapsed.total_seconds(),
                "data": response.json()
            }
        else:
            return {
                "group": group_key,
                "system": system_key,
                "name": system_config["name"],
                "status": "error",
                "error": f"Status code: {response.status_code}"
            }
    except Exception as e:
        return {
            "group": group_key,
            "system": system_key,
            "name": system_config["name"],
            "status": "offline",
            "error": str(e)
        }

def get_system_data(group_key, system_key, group_config, system_config):
    """Récupère les données d'un système"""
    try:
        url = group_config["url"] + system_config["endpoints"]["data"]
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return {
                "group": group_key,
                "system": system_key,
                "name": system_config["name"],
                "icon": system_config["icon"],
                "status": "success",
                "data": response.json()
            }
        else:
            return {
                "group": group_key,
                "system": system_key,
                "name": system_config["name"],
                "status": "error",
                "error": f"Status code: {response.status_code}"
            }
    except Exception as e:
        return {
            "group": group_key,
            "system": system_key,
            "name": system_config["name"],
            "status": "error",
            "error": str(e)
        }

# ===================== ENDPOINTS =======================

@app.route('/')
def home():
    """Page d'accueil avec vue d'ensemble"""
    total_systems = sum(len(g["systems"]) for g in APIS_CONFIG.values())
    
    return jsonify({
        "api": "Orchestration Globale - Simulation Organes Humains",
        "version": "2.0.0",
        "description": "API centrale coordonnant les 12 systèmes d'organes humains",
        "groups": {
            "vital": {
                "name": APIS_CONFIG["vital"]["name"],
                "systems": list(APIS_CONFIG["vital"]["systems"].keys()),
                "count": len(APIS_CONFIG["vital"]["systems"])
            },
            "support": {
                "name": APIS_CONFIG["support"]["name"],
                "systems": list(APIS_CONFIG["support"]["systems"].keys()),
                "count": len(APIS_CONFIG["support"]["systems"])
            },
            "specialized": {
                "name": APIS_CONFIG["specialized"]["name"],
                "systems": list(APIS_CONFIG["specialized"]["systems"].keys()),
                "count": len(APIS_CONFIG["specialized"]["systems"])
            }
        },
        "total_systems": total_systems,
        "endpoints": {
            "health": "/api/health",
            "health_detailed": "/api/health/detailed",
            "status": "/api/status",
            "data": "/api/data",
            "data_by_group": "/api/data/<group>",
            "data_by_system": "/api/data/<group>/<system>",
            "simulate_global": "/api/simulate/<scenario>",
            "simulate_system": "/api/simulate/<group>/<system>/<condition>",
            "report": "/api/report",
            "groups": "/api/groups",
            "systems": "/api/systems"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def check_health():
    """Santé globale - Version rapide"""
    
    # Vérifier chaque groupe en parallèle
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(check_group_health, group_key, group_config): group_key
            for group_key, group_config in APIS_CONFIG.items()
        }
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    # Statistiques
    total_groups = len(results)
    online_groups = sum(1 for r in results if r["status"] == "online")
    total_systems = sum(len(APIS_CONFIG[g]["systems"]) for g in APIS_CONFIG)
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_groups": total_groups,
            "online_groups": online_groups,
            "offline_groups": total_groups - online_groups,
            "total_systems": total_systems,
            "health_percentage": (online_groups / total_groups * 100) if total_groups > 0 else 0
        },
        "groups": results
    })

@app.route('/api/health/detailed', methods=['GET'])
def check_health_detailed():
    """Santé détaillée - Vérifie chaque système individuellement"""
    
    tasks = []
    for group_key, group_config in APIS_CONFIG.items():
        for system_key, system_config in group_config["systems"].items():
            tasks.append((group_key, system_key, group_config, system_config))
    
    # Vérifier tous les systèmes en parallèle
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(check_system_health, *task): task
            for task in tasks
        }
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    # Organiser par groupe
    by_group = {"vital": [], "support": [], "specialized": []}
    for result in results:
        by_group[result["group"]].append(result)
    
    # Statistiques
    total_systems = len(results)
    online_systems = sum(1 for r in results if r["status"] == "online")
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_systems": total_systems,
            "online_systems": online_systems,
            "offline_systems": total_systems - online_systems,
            "health_percentage": (online_systems / total_systems * 100) if total_systems > 0 else 0
        },
        "by_group": by_group,
        "all_systems": results
    })

@app.route('/api/status', methods=['GET'])
def get_global_status():
    """Statut global simplifié"""
    
    health_check = check_health()
    health_data = health_check.get_json()
    
    online_groups = health_data["summary"]["online_groups"]
    total_groups = health_data["summary"]["total_groups"]
    
    # Déterminer le statut
    if online_groups == total_groups:
        global_status = "optimal"
        message = "Tous les systèmes sont opérationnels"
    elif online_groups >= total_groups * 0.66:
        global_status = "good"
        message = "La plupart des systèmes fonctionnent"
    elif online_groups >= total_groups * 0.33:
        global_status = "degraded"
        message = "Plusieurs systèmes sont hors ligne"
    else:
        global_status = "critical"
        message = "État critique - Majorité des systèmes hors ligne"
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "global_status": global_status,
        "message": message,
        "groups_online": f"{online_groups}/{total_groups}",
        "health_percentage": health_data["summary"]["health_percentage"]
    })

@app.route('/api/data', methods=['GET'])
def get_all_data():
    """Récupère TOUTES les données de TOUS les systèmes"""
    
    tasks = []
    for group_key, group_config in APIS_CONFIG.items():
        for system_key, system_config in group_config["systems"].items():
            tasks.append((group_key, system_key, group_config, system_config))
    
    # Récupérer toutes les données en parallèle
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(get_system_data, *task): task
            for task in tasks
        }
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            key = f"{result['group']}_{result['system']}"
            results[key] = result
    
    # Organiser par groupe
    by_group = {
        "vital": {},
        "support": {},
        "specialized": {}
    }
    
    for key, data in results.items():
        by_group[data["group"]][data["system"]] = data
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "patient_id": "VIRTUAL_PATIENT_001",
        "all_data": results,
        "by_group": by_group
    })

@app.route('/api/data/<group>', methods=['GET'])
def get_group_data(group):
    """Récupère les données d'un groupe spécifique"""
    
    if group not in APIS_CONFIG:
        return jsonify({
            "error": "Groupe non trouvé",
            "available_groups": list(APIS_CONFIG.keys())
        }), 404
    
    group_config = APIS_CONFIG[group]
    results = {}
    
    for system_key, system_config in group_config["systems"].items():
        data = get_system_data(group, system_key, group_config, system_config)
        results[system_key] = data
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "group": group,
        "group_name": group_config["name"],
        "systems": results
    })

@app.route('/api/data/<group>/<system>', methods=['GET'])
def get_system_data_endpoint(group, system):
    """Récupère les données d'un système spécifique"""
    
    if group not in APIS_CONFIG:
        return jsonify({"error": "Groupe non trouvé"}), 404
    
    if system not in APIS_CONFIG[group]["systems"]:
        return jsonify({"error": "Système non trouvé"}), 404
    
    group_config = APIS_CONFIG[group]
    system_config = group_config["systems"][system]
    
    data = get_system_data(group, system, group_config, system_config)
    
    return jsonify(data)

@app.route('/api/simulate/<scenario>', methods=['POST'])
def simulate_global_scenario(scenario):
    """Simule un scénario global affectant plusieurs systèmes"""
    
    # Scénarios prédéfinis
    scenarios = {
        "cardiac_arrest": {
            "name": "Arrêt Cardiaque",
            "description": "Arrêt du cœur - Affecte tous les systèmes vitaux",
            "simulations": {
                ("vital", "cardiac", "bradycardie"): "Cœur en bradycardie sévère",
                ("vital", "respiratory", "apnee"): "Arrêt respiratoire",
                ("vital", "neural", "stress"): "Stress cérébral extrême"
            }
        },
        "septic_shock": {
            "name": "Choc Septique",
            "description": "Infection généralisée",
            "simulations": {
                ("specialized", "immune", "infection"): "Réponse immunitaire",
                ("vital", "cardiac", "tachycardie"): "Tachycardie",
                ("support", "renal", "insuffisance"): "Insuffisance rénale"
            }
        },
        "trauma": {
            "name": "Traumatisme Grave",
            "description": "Accident avec fractures et hémorragie",
            "simulations": {
                ("specialized", "musculoskeletal", "fracture"): "Fractures multiples",
                ("specialized", "hematological", "hemorrhage"): "Hémorragie",
                ("vital", "cardiac", "tachycardie"): "Tachycardie compensatoire"
            }
        },
        "normal": {
            "name": "Retour à la Normale",
            "description": "Réinitialise tous les systèmes",
            "simulations": {}  # Implémentation spéciale
        }
    }
    
    if scenario not in scenarios:
        return jsonify({
            "error": "Scénario inconnu",
            "available_scenarios": list(scenarios.keys())
        }), 400
    
    scenario_config = scenarios[scenario]
    results = {}
    
    if scenario == "normal":
        # Réinitialiser tous les systèmes (implémentation simplifiée)
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "scenario": scenario,
            "name": scenario_config["name"],
            "message": "Réinitialisation demandée - À implémenter par groupe"
        })
    
    # Exécuter les simulations
    for (group, system, condition), description in scenario_config["simulations"].items():
        try:
            group_config = APIS_CONFIG[group]
            system_config = group_config["systems"][system]
            url = f"{group_config['url']}{system_config['endpoints']['simulate']}/{condition}"
            
            response = requests.post(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                results[f"{group}_{system}"] = {
                    "status": "success",
                    "description": description,
                    "data": response.json()
                }
            else:
                results[f"{group}_{system}"] = {
                    "status": "error",
                    "description": description,
                    "error": f"Status {response.status_code}"
                }
        except Exception as e:
            results[f"{group}_{system}"] = {
                "status": "error",
                "description": description,
                "error": str(e)
            }
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario,
        "name": scenario_config["name"],
        "description": scenario_config["description"],
        "results": results
    })

@app.route('/api/simulate/<group>/<system>/<condition>', methods=['POST'])
def simulate_specific(group, system, condition):
    """Simule une condition sur un système spécifique"""
    
    if group not in APIS_CONFIG:
        return jsonify({"error": "Groupe non trouvé"}), 404
    
    if system not in APIS_CONFIG[group]["systems"]:
        return jsonify({"error": "Système non trouvé"}), 404
    
    try:
        group_config = APIS_CONFIG[group]
        system_config = group_config["systems"][system]
        url = f"{group_config['url']}{system_config['endpoints']['simulate']}/{condition}"
        
        response = requests.post(url, timeout=TIMEOUT)
        
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "group": group,
            "system": system,
            "condition": condition,
            "status": "success" if response.status_code == 200 else "error",
            "response": response.json() if response.status_code == 200 else {"error": f"Status {response.status_code}"}
        }), response.status_code
    except Exception as e:
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "group": group,
            "system": system,
            "condition": condition,
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/groups', methods=['GET'])
def list_groups():
    """Liste tous les groupes"""
    
    groups = []
    for group_key, group_config in APIS_CONFIG.items():
        groups.append({
            "id": group_key,
            "name": group_config["name"],
            "color": group_config["color"],
            "url": group_config["url"],
            "systems_count": len(group_config["systems"]),
            "systems": list(group_config["systems"].keys())
        })
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "total_groups": len(groups),
        "groups": groups
    })

@app.route('/api/systems', methods=['GET'])
def list_all_systems():
    """Liste tous les systèmes"""
    
    systems = []
    for group_key, group_config in APIS_CONFIG.items():
        for system_key, system_config in group_config["systems"].items():
            systems.append({
                "id": system_key,
                "name": system_config["name"],
                "icon": system_config["icon"],
                "group": group_key,
                "group_name": group_config["name"],
                "group_color": group_config["color"]
            })
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "total_systems": len(systems),
        "systems": systems
    })

@app.route('/api/report', methods=['GET'])
def generate_full_report():
    """Génère un rapport médical complet"""
    
    # Récupérer l'état de santé détaillé
    health_response = check_health_detailed()
    health_data = health_response.get_json()
    
    # Récupérer toutes les données
    data_response = get_all_data()
    data_json = data_response.get_json()
    
    # Analyse
    online_systems = health_data["summary"]["online_systems"]
    total_systems = health_data["summary"]["total_systems"]
    health_percent = health_data["summary"]["health_percentage"]
    
    # Déterminer l'état global
    if health_percent == 100:
        overall_assessment = "Excellent - Tous les systèmes fonctionnent normalement"
    elif health_percent >= 80:
        overall_assessment = "Bon - La plupart des systèmes sont opérationnels"
    elif health_percent >= 50:
        overall_assessment = "Moyen - Plusieurs systèmes présentent des problèmes"
    else:
        overall_assessment = "Critique - Intervention urgente nécessaire"
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "report_type": "Bilan de Santé Complet",
        "patient_id": "VIRTUAL_PATIENT_001",
        "overall_assessment": overall_assessment,
        "health_score": health_percent,
        "systems_status": {
            "total": total_systems,
            "operational": online_systems,
            "offline": total_systems - online_systems
        },
        "by_group": health_data["by_group"],
        "recommendations": [
            "Consulter les systèmes hors ligne",
            "Vérifier les connexions API",
            "Analyser les logs d'erreurs"
        ] if online_systems < total_systems else ["Aucune action requise - Tout fonctionne normalement"]
    })

# ===================== GESTION DES ERREURS =======================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint non trouvé",
        "message": "Consultez / pour la liste des endpoints disponibles"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Erreur interne du serveur",
        "message": str(error)
    }), 500

# ===================== LANCEMENT =======================

if __name__ == '__main__':
    print("="*80)
    print(" "*20 + "🏥 ORCHESTRATION GLOBALE - 12 SYSTÈMES D'ORGANES 🏥")
    print("="*80)
    print(f"\n✅ Port d'écoute: 5000")
    print(f"✅ Total de systèmes gérés: 12")
    print(f"✅ Groupes: {len(APIS_CONFIG)}")
    print("\n📋 APIs requises:")
    for group_key, group_config in APIS_CONFIG.items():
        print(f"   {group_config['color']} {group_config['name']:20} → {group_config['url']:25} ({len(group_config['systems'])} systèmes)")
    print("\n" + "="*80)
    print("🌐 Accès: http://localhost:5000")
    print("📊 Health Check: http://localhost:5000/api/health")
    print("="*80 + "\n")
    
    app.run(debug=True, port=5000)