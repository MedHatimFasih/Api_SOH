"""
API GROUPE SPÉCIALISÉ - Port 5004
Gère 4 systèmes: immune, musculoskeletal, hematological, reproductive
Compatible avec orchestration-api et tests individuels
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# ===================== CONFIGURATION DES SYSTÈMES =======================

SYSTEMS = {
    "immune": {
        "name": "Système Immunitaire",
        "icon": "🛡️",
        "metrics": ["white_blood_cells", "antibody_level", "lymphocyte_count", "body_temperature"],
        "conditions": ["infection", "autoimmune", "immunodeficiency", "allergy", "normal"],
        "parameters": {
            "sensitivity": 75,
            "response_time": 2.5,
            "memory_cells": 85
        }
    },
    "musculoskeletal": {
        "name": "Système Musculosquelettique",
        "icon": "💪",
        "metrics": ["bone_density", "muscle_mass", "joint_flexibility", "strength_index"],
        "conditions": ["arthritis", "osteoporosis", "muscle_strain", "fracture", "normal"],
        "parameters": {
            "bone_remodeling_rate": 70,
            "muscle_recovery": 80,
            "joint_lubrication": 85
        }
    },
    "hematological": {
        "name": "Système Sanguin",
        "icon": "🩸",
        "metrics": ["red_blood_cells", "hemoglobin", "platelet_count", "hematocrit"],
        "conditions": ["anemia", "leukemia", "thrombocytopenia", "polycythemia", "normal"],
        "parameters": {
            "coagulation_factor": 90,
            "oxygen_capacity": 95,
            "blood_viscosity": 75
        }
    },
    "reproductive": {
        "name": "Système Reproductif",
        "icon": "👶",
        "metrics": ["hormone_levels", "fertility_index", "reproductive_health", "cycle_regularity"],
        "conditions": ["infertility", "hormonal_imbalance", "dysfunction", "normal"],
        "parameters": {
            "hormone_balance": 80,
            "reproductive_efficiency": 75,
            "gametogenesis_rate": 70
        }
    }
}

# État actuel de chaque système
system_states = {sys: "normal" for sys in SYSTEMS.keys()}
active_conditions = {sys: [] for sys in SYSTEMS.keys()}
system_parameters = {sys: SYSTEMS[sys]["parameters"].copy() for sys in SYSTEMS.keys()}

# Configuration patient par défaut
patient_config = {
    "age": 35,
    "weight": 70,
    "height": 175,
    "gender": "unknown",
    "medical_history": []
}

# ===================== FONCTIONS UTILITAIRES =======================

def generate_metrics(system_name, condition="normal"):
    """Génère des métriques aléatoires selon la condition"""
    metrics = {}
    
    if system_name == "immune":
        if condition == "infection":
            metrics = {
                "white_blood_cells": random.randint(12000, 20000),
                "antibody_level": random.randint(80, 100),
                "lymphocyte_count": random.randint(3000, 5000),
                "body_temperature": round(random.uniform(38.5, 40.0), 1)
            }
        elif condition == "immunodeficiency":
            metrics = {
                "white_blood_cells": random.randint(2000, 4000),
                "antibody_level": random.randint(20, 40),
                "lymphocyte_count": random.randint(500, 1000),
                "body_temperature": round(random.uniform(36.0, 37.0), 1)
            }
        elif condition == "allergy":
            metrics = {
                "white_blood_cells": random.randint(9000, 13000),
                "antibody_level": random.randint(90, 110),
                "lymphocyte_count": random.randint(2500, 4000),
                "body_temperature": round(random.uniform(37.0, 37.5), 1)
            }
        else:  # normal
            metrics = {
                "white_blood_cells": random.randint(4000, 11000),
                "antibody_level": random.randint(60, 90),
                "lymphocyte_count": random.randint(1500, 3000),
                "body_temperature": round(random.uniform(36.5, 37.2), 1)
            }
    
    elif system_name == "musculoskeletal":
        if condition == "osteoporosis":
            metrics = {
                "bone_density": round(random.uniform(0.5, 0.7), 2),
                "muscle_mass": round(random.uniform(25, 35), 1),
                "joint_flexibility": random.randint(40, 60),
                "strength_index": random.randint(50, 70)
            }
        elif condition == "arthritis":
            metrics = {
                "bone_density": round(random.uniform(0.8, 1.0), 2),
                "muscle_mass": round(random.uniform(30, 40), 1),
                "joint_flexibility": random.randint(20, 40),
                "strength_index": random.randint(60, 75)
            }
        elif condition == "muscle_strain":
            metrics = {
                "bone_density": round(random.uniform(0.9, 1.2), 2),
                "muscle_mass": round(random.uniform(35, 45), 1),
                "joint_flexibility": random.randint(50, 70),
                "strength_index": random.randint(40, 60)
            }
        else:  # normal
            metrics = {
                "bone_density": round(random.uniform(0.9, 1.3), 2),
                "muscle_mass": round(random.uniform(35, 50), 1),
                "joint_flexibility": random.randint(70, 90),
                "strength_index": random.randint(80, 100)
            }
    
    elif system_name == "hematological":
        if condition == "anemia":
            metrics = {
                "red_blood_cells": round(random.uniform(3.0, 4.0), 2),
                "hemoglobin": round(random.uniform(8.0, 11.0), 1),
                "platelet_count": random.randint(150000, 250000),
                "hematocrit": round(random.uniform(30, 36), 1)
            }
        elif condition == "thrombocytopenia":
            metrics = {
                "red_blood_cells": round(random.uniform(4.5, 5.5), 2),
                "hemoglobin": round(random.uniform(13.0, 16.0), 1),
                "platelet_count": random.randint(50000, 100000),
                "hematocrit": round(random.uniform(40, 45), 1)
            }
        elif condition == "polycythemia":
            metrics = {
                "red_blood_cells": round(random.uniform(6.0, 7.5), 2),
                "hemoglobin": round(random.uniform(18.0, 22.0), 1),
                "platelet_count": random.randint(200000, 450000),
                "hematocrit": round(random.uniform(52, 62), 1)
            }
        else:  # normal
            metrics = {
                "red_blood_cells": round(random.uniform(4.5, 5.9), 2),
                "hemoglobin": round(random.uniform(13.0, 17.0), 1),
                "platelet_count": random.randint(150000, 400000),
                "hematocrit": round(random.uniform(40, 50), 1)
            }
    
    elif system_name == "reproductive":
        if condition == "hormonal_imbalance":
            metrics = {
                "hormone_levels": random.randint(30, 50),
                "fertility_index": round(random.uniform(0.3, 0.6), 2),
                "reproductive_health": random.randint(40, 60),
                "cycle_regularity": random.randint(30, 50)
            }
        elif condition == "infertility":
            metrics = {
                "hormone_levels": random.randint(40, 60),
                "fertility_index": round(random.uniform(0.1, 0.4), 2),
                "reproductive_health": random.randint(50, 70),
                "cycle_regularity": random.randint(40, 60)
            }
        else:  # normal
            metrics = {
                "hormone_levels": random.randint(70, 100),
                "fertility_index": round(random.uniform(0.7, 1.0), 2),
                "reproductive_health": random.randint(80, 95),
                "cycle_regularity": random.randint(80, 100)
            }
    
    return metrics

def get_health_status(system_name, metrics):
    """Détermine l'état de santé basé sur les métriques"""
    if system_name == "immune":
        wbc = metrics.get("white_blood_cells", 0)
        temp = metrics.get("body_temperature", 37.0)
        if wbc > 11000 or temp > 38.0:
            return "elevated"
        elif wbc < 4000:
            return "low"
        return "normal"
    
    elif system_name == "musculoskeletal":
        bone_density = metrics.get("bone_density", 0)
        if bone_density < 0.8:
            return "low_density"
        return "normal"
    
    elif system_name == "hematological":
        hemoglobin = metrics.get("hemoglobin", 0)
        if hemoglobin < 12.0:
            return "anemic"
        elif hemoglobin > 17.5:
            return "elevated"
        return "normal"
    
    elif system_name == "reproductive":
        fertility = metrics.get("fertility_index", 0)
        if fertility < 0.7:
            return "impaired"
        return "normal"
    
    return "normal"

# ===================== ENDPOINTS STANDARDS =======================

@app.route('/')
def home():
    """Page d'accueil du groupe spécialisé"""
    return jsonify({
        "group": "Specialized Systems",
        "port": 5004,
        "systems": list(SYSTEMS.keys()),
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "status": "operational",
        "endpoints": {
            "status": "/api/<system>/status",
            "data": "/api/<system>/data",
            "simulate": "/api/<system>/simulate/<condition>",
            "parameters": "/api/<system>/parameters",
            "configure": "/api/<system>/configure"
        }
    })

@app.route('/api/<system_name>/status', methods=['GET'])
def get_status(system_name):
    """Retourne le statut d'un système"""
    if system_name not in SYSTEMS:
        return jsonify({
            "error": "System not found",
            "available_systems": list(SYSTEMS.keys())
        }), 404
    
    condition = system_states.get(system_name, "normal")
    metrics = generate_metrics(system_name, condition)
    health = get_health_status(system_name, metrics)
    
    # Format pour test.py du système immune
    response = {
        "system": system_name,
        "name": SYSTEMS[system_name]["name"],
        "icon": SYSTEMS[system_name]["icon"],
        "status": "online",
        "health_status": health,
        "state": health,  # Alias pour compatibilité
        "current_condition": condition,
        "active_conditions": active_conditions.get(system_name, []),
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    }
    
    # Ajouter des champs spécifiques pour immune
    if system_name == "immune":
        response["white_blood_cells"] = metrics.get("white_blood_cells", 0)
        response["body_temperature"] = metrics.get("body_temperature", 37.0)
    
    return jsonify(response)

@app.route('/api/<system_name>/data', methods=['GET'])
def get_data(system_name):
    """Retourne les données détaillées d'un système"""
    if system_name not in SYSTEMS:
        return jsonify({
            "error": "System not found"
        }), 404
    
    condition = system_states.get(system_name, "normal")
    metrics = generate_metrics(system_name, condition)
    
    response = {
        "system": system_name,
        "name": SYSTEMS[system_name]["name"],
        "icon": SYSTEMS[system_name]["icon"],
        "condition": condition,
        "metrics": metrics,
        "parameters": system_parameters.get(system_name, {}),
        "available_conditions": SYSTEMS[system_name]["conditions"],
        "timestamp": datetime.now().isoformat()
    }
    
    # Format spécial pour immune
    if system_name == "immune":
        response["white_blood_cells"] = metrics.get("white_blood_cells", 0)
        response["body_temperature"] = metrics.get("body_temperature", 37.0)
    
    return jsonify(response)

@app.route('/api/<system_name>/simulate/<condition>', methods=['POST'])
def simulate_condition(system_name, condition):
    """Simule une condition pathologique"""
    if system_name not in SYSTEMS:
        return jsonify({
            "error": "System not found"
        }), 404
    
    if condition not in SYSTEMS[system_name]["conditions"]:
        return jsonify({
            "error": "Invalid condition",
            "message": f"Condition '{condition}' not available for {system_name}",
            "available_conditions": SYSTEMS[system_name]["conditions"]
        }), 400
    
    # Mettre à jour l'état du système
    system_states[system_name] = condition
    if condition != "normal" and condition not in active_conditions[system_name]:
        active_conditions[system_name].append(condition)
    
    # Générer les nouvelles métriques
    metrics = generate_metrics(system_name, condition)
    health = get_health_status(system_name, metrics)
    
    response = {
        "success": True,
        "system": system_name,
        "name": SYSTEMS[system_name]["name"],
        "condition_applied": condition,
        "health_status": health,
        "new_metrics": metrics,
        "message": f"{condition.capitalize()} simulation activated for {SYSTEMS[system_name]['name']}",
        "timestamp": datetime.now().isoformat()
    }
    
    # Format spécial pour immune
    if system_name == "immune":
        response["white_blood_cells"] = metrics.get("white_blood_cells", 0)
        response["body_temperature"] = metrics.get("body_temperature", 37.0)
    
    return jsonify(response)

# ===================== NOUVEAUX ENDPOINTS POUR TESTS =======================

@app.route('/api/<system_name>/parameters', methods=['GET'])
def get_parameters(system_name):
    """Récupère les paramètres de configuration d'un système"""
    if system_name not in SYSTEMS:
        return jsonify({
            "error": "System not found",
            "available_systems": list(SYSTEMS.keys())
        }), 404
    
    return jsonify({
        "system": system_name,
        "name": SYSTEMS[system_name]["name"],
        "parameters": system_parameters.get(system_name, {}),
        "default_parameters": SYSTEMS[system_name]["parameters"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/<system_name>/configure', methods=['POST'])
def configure_system(system_name):
    """Configure les paramètres d'un système ou du patient"""
    if system_name not in SYSTEMS:
        return jsonify({
            "error": "System not found",
            "available_systems": list(SYSTEMS.keys())
        }), 404
    
    data = request.get_json() or {}
    
    # Configuration patient
    if "patient" in data:
        patient_data = data["patient"]
        for key in ["age", "weight", "height", "gender"]:
            if key in patient_data:
                patient_config[key] = patient_data[key]
        
        return jsonify({
            "success": True,
            "message": "Patient configuration updated",
            "patient": patient_config,
            "timestamp": datetime.now().isoformat()
        })
    
    # Configuration système
    if "parameters" in data:
        params = data["parameters"]
        if system_name not in system_parameters:
            system_parameters[system_name] = {}
        
        for key, value in params.items():
            if key in SYSTEMS[system_name]["parameters"]:
                system_parameters[system_name][key] = value
        
        return jsonify({
            "success": True,
            "message": f"Parameters updated for {SYSTEMS[system_name]['name']}",
            "system": system_name,
            "parameters": system_parameters[system_name],
            "timestamp": datetime.now().isoformat()
        })
    
    return jsonify({
        "error": "No configuration data provided",
        "expected_format": {
            "patient": {"age": 35, "weight": 70, "height": 175, "gender": "M"},
            "parameters": {"param_name": "value"}
        }
    }), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Santé globale du groupe"""
    return jsonify({
        "service": "Specialized Systems API",
        "port": 5004,
        "status": "healthy",
        "systems_count": len(SYSTEMS),
        "patient_configured": patient_config,
        "timestamp": datetime.now().isoformat()
    })

# ===================== GESTION DES ERREURS =======================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": str(error),
        "timestamp": datetime.now().isoformat()
    }), 500

# ===================== LANCEMENT =======================

if __name__ == '__main__':
    print("="*70)
    print(" "*15 + "🔵 GROUPE SPÉCIALISÉ - API v2.0")
    print("="*70)
    print(f"\n✅ Port: 5004")
    print(f"✅ Systèmes gérés: {len(SYSTEMS)}")
    print("\n📋 Systèmes disponibles:")
    for sys_name, sys_info in SYSTEMS.items():
        conditions_count = len(sys_info['conditions'])
        print(f"   {sys_info['icon']} {sys_info['name']:30} ({conditions_count} conditions)")
    print("\n🔧 Endpoints disponibles:")
    print("   • /api/<system>/status          - Statut du système")
    print("   • /api/<system>/data            - Données détaillées")
    print("   • /api/<system>/simulate/<cond> - Simuler une condition")
    print("   • /api/<system>/parameters      - Paramètres système")
    print("   • /api/<system>/configure       - Configurer patient/système")
    print("\n" + "="*70)
    print("🌐 API lancée sur: http://localhost:5004")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5004, host='0.0.0.0')