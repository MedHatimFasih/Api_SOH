from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

class ImmuneSystemSimulator:
    """Simulateur du système immunitaire"""
    
    def __init__(self):
        self.age = 30
        self.sex = "M"
        self.health_status = "normal"
        self.active_conditions = []
        
    def generate_immune_data(self):
        """Génère des données synthétiques du système immunitaire"""
        
        # Valeurs de base selon l'état de santé
        base_multipliers = {
            "normal": 1.0,
            "infection": 1.5,
            "autoimmune": 0.7,
            "immunodeficiency": 0.4,
            "allergic_reaction": 1.3
        }
        
        multiplier = base_multipliers.get(self.health_status, 1.0)
        
        # Globules blancs (leucocytes) - normal: 4000-11000/mm³
        white_blood_cells = int(random.uniform(4000, 11000) * multiplier)
        
        # Types de leucocytes (en pourcentage)
        neutrophils = random.uniform(40, 70) * multiplier  # Neutrophiles
        lymphocytes = random.uniform(20, 40)  # Lymphocytes
        monocytes = random.uniform(2, 8)  # Monocytes
        eosinophils = random.uniform(1, 4) * (1.5 if "allergic" in self.health_status else 1.0)
        basophils = random.uniform(0.5, 1)  # Basophiles
        
        # Normalisation pour avoir 100%
        total = neutrophils + lymphocytes + monocytes + eosinophils + basophils
        neutrophils = (neutrophils / total) * 100
        lymphocytes = (lymphocytes / total) * 100
        monocytes = (monocytes / total) * 100
        eosinophils = (eosinophils / total) * 100
        basophils = (basophils / total) * 100
        
        # Immunoglobulines (en g/L)
        igg = random.uniform(7, 16) * multiplier  # IgG
        iga = random.uniform(0.7, 4) * multiplier  # IgA
        igm = random.uniform(0.4, 2.3) * multiplier  # IgM
        ige = random.uniform(0, 100) * (2.0 if "allergic" in self.health_status else 1.0)  # IgE en UI/mL
        
        # Cytokines (niveau d'inflammation)
        inflammation_level = random.uniform(0, 10) * multiplier
        
        # Température corporelle
        temperature = 36.5 + random.uniform(-0.3, 0.3)
        if self.health_status == "infection":
            temperature += random.uniform(1, 3)
        
        # Activité des cellules NK (Natural Killer)
        nk_activity = random.uniform(10, 40) * multiplier
        
        # Complément (système du complément)
        complement_c3 = random.uniform(0.9, 1.8)  # g/L
        complement_c4 = random.uniform(0.1, 0.4)  # g/L
        
        return {
            "timestamp": datetime.now().isoformat(),
            "patient_info": {
                "age": self.age,
                "sex": self.sex,
                "health_status": self.health_status
            },
            "white_blood_cells": {
                "total_count": white_blood_cells,
                "unit": "cells/mm³",
                "differential": {
                    "neutrophils": round(neutrophils, 2),
                    "lymphocytes": round(lymphocytes, 2),
                    "monocytes": round(monocytes, 2),
                    "eosinophils": round(eosinophils, 2),
                    "basophils": round(basophils, 2)
                }
            },
            "immunoglobulins": {
                "IgG": round(igg, 2),
                "IgA": round(iga, 2),
                "IgM": round(igm, 2),
                "IgE": round(ige, 2),
                "unit": "g/L (IgE en UI/mL)"
            },
            "inflammation": {
                "level": round(inflammation_level, 2),
                "temperature": round(temperature, 1),
                "cytokine_activity": "elevated" if inflammation_level > 5 else "normal"
            },
            "cellular_immunity": {
                "nk_cell_activity": round(nk_activity, 2),
                "unit": "%"
            },
            "complement_system": {
                "C3": round(complement_c3, 2),
                "C4": round(complement_c4, 2),
                "unit": "g/L"
            },
            "active_conditions": self.active_conditions
        }
    
    def simulate_condition(self, condition):
        """Simule une condition pathologique"""
        valid_conditions = {
            "infection": "État infectieux actif",
            "autoimmune": "Maladie auto-immune",
            "immunodeficiency": "Immunodéficience",
            "allergic_reaction": "Réaction allergique",
            "normal": "État normal"
        }
        
        if condition in valid_conditions:
            self.health_status = condition
            if condition not in self.active_conditions and condition != "normal":
                self.active_conditions.append(condition)
            elif condition == "normal":
                self.active_conditions = []
            return True, valid_conditions[condition]
        return False, "Condition inconnue"

# Instance globale du simulateur
simulator = ImmuneSystemSimulator()

@app.route('/')
def home():
    return jsonify({
        "api": "Immune System API",
        "version": "1.0.0",
        "description": "API de simulation du système immunitaire",
        "endpoints": {
            "status": "/api/immune/status",
            "data": "/api/immune/data",
            "simulate": "/api/immune/simulate/<condition>",
            "parameters": "/api/immune/parameters"
        }
    })

@app.route('/api/immune/status', methods=['GET'])
def get_status():
    """Retourne le statut du système immunitaire"""
    return jsonify({
        "status": "operational",
        "organ": "immune_system",
        "health_status": simulator.health_status,
        "active_conditions": simulator.active_conditions,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/immune/data', methods=['GET'])
def get_data():
    """Retourne les données synthétiques courantes"""
    return jsonify(simulator.generate_immune_data())

@app.route('/api/immune/simulate/<condition>', methods=['POST'])
def simulate_condition(condition):
    """Simule une pathologie du système immunitaire"""
    success, message = simulator.simulate_condition(condition)
    
    if success:
        return jsonify({
            "success": True,
            "condition": condition,
            "message": message,
            "current_data": simulator.generate_immune_data()
        })
    else:
        return jsonify({
            "success": False,
            "error": message
        }), 400

@app.route('/api/immune/parameters', methods=['GET'])
def get_parameters():
    """Retourne les paramètres de simulation disponibles"""
    return jsonify({
        "available_conditions": {
            "infection": "État infectieux - augmentation des leucocytes et inflammation",
            "autoimmune": "Maladie auto-immune - dérèglement du système immunitaire",
            "immunodeficiency": "Immunodéficience - diminution des défenses",
            "allergic_reaction": "Réaction allergique - augmentation IgE et éosinophiles",
            "normal": "Retour à l'état normal"
        },
        "modifiable_parameters": {
            "age": "Âge du patient (années)",
            "sex": "Sexe du patient (M/F)",
            "health_status": "État de santé actuel"
        },
        "measured_values": {
            "white_blood_cells": "Nombre de globules blancs",
            "immunoglobulins": "Taux d'immunoglobulines (IgG, IgA, IgM, IgE)",
            "inflammation": "Niveau d'inflammation et température",
            "cellular_immunity": "Activité des cellules NK",
            "complement": "Système du complément"
        }
    })

@app.route('/api/immune/configure', methods=['POST'])
def configure():
    """Configure les paramètres du patient"""
    data = request.get_json()
    
    if 'age' in data:
        simulator.age = int(data['age'])
    if 'sex' in data:
        simulator.sex = data['sex']
    if 'health_status' in data:
        simulator.health_status = data['health_status']
    
    return jsonify({
        "success": True,
        "message": "Configuration mise à jour",
        "current_config": {
            "age": simulator.age,
            "sex": simulator.sex,
            "health_status": simulator.health_status
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5004)