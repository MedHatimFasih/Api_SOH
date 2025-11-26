from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime
import logging
import sys

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Active CORS pour permettre les requêtes depuis d'autres origines

class ImmuneSystemSimulator:
    """Simulateur du système immunitaire"""
    
    def __init__(self):
        self.age = 30
        self.sex = "M"
        self.health_status = "normal"
        self.active_conditions = []
        logger.info("Simulateur du système immunitaire initialisé")
        
    def generate_immune_data(self):
        """Génère des données synthétiques du système immunitaire"""
        try:
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
            neutrophils = random.uniform(40, 70) * multiplier
            lymphocytes = random.uniform(20, 40)
            monocytes = random.uniform(2, 8)
            eosinophils = random.uniform(1, 4) * (1.5 if "allergic" in self.health_status else 1.0)
            basophils = random.uniform(0.5, 1)
            
            # Normalisation pour avoir 100%
            total = neutrophils + lymphocytes + monocytes + eosinophils + basophils
            if total == 0:
                total = 1  # Éviter division par zéro
                
            neutrophils = (neutrophils / total) * 100
            lymphocytes = (lymphocytes / total) * 100
            monocytes = (monocytes / total) * 100
            eosinophils = (eosinophils / total) * 100
            basophils = (basophils / total) * 100
            
            # Immunoglobulines (en g/L)
            igg = random.uniform(7, 16) * multiplier
            iga = random.uniform(0.7, 4) * multiplier
            igm = random.uniform(0.4, 2.3) * multiplier
            ige = random.uniform(0, 100) * (2.0 if "allergic" in self.health_status else 1.0)
            
            # Cytokines (niveau d'inflammation)
            inflammation_level = random.uniform(0, 10) * multiplier
            
            # Température corporelle
            temperature = 36.5 + random.uniform(-0.3, 0.3)
            if self.health_status == "infection":
                temperature += random.uniform(1, 3)
            
            # Activité des cellules NK (Natural Killer)
            nk_activity = random.uniform(10, 40) * multiplier
            
            # Complément (système du complément)
            complement_c3 = random.uniform(0.9, 1.8)
            complement_c4 = random.uniform(0.1, 0.4)
            
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
        except Exception as e:
            logger.error(f"Erreur lors de la génération des données: {str(e)}")
            raise
    
    def simulate_condition(self, condition):
        """Simule une condition pathologique"""
        try:
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
                logger.info(f"Condition simulée: {condition}")
                return True, valid_conditions[condition]
            return False, "Condition inconnue"
        except Exception as e:
            logger.error(f"Erreur lors de la simulation: {str(e)}")
            return False, f"Erreur: {str(e)}"

# Instance globale du simulateur
simulator = ImmuneSystemSimulator()

# Gestionnaire d'erreurs global
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint non trouvé",
        "message": "L'URL demandée n'existe pas",
        "available_endpoints": {
            "home": "/",
            "status": "/api/immune/status",
            "data": "/api/immune/data",
            "simulate": "/api/immune/simulate/<condition>",
            "parameters": "/api/immune/parameters",
            "configure": "/api/immune/configure"
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erreur serveur: {str(error)}")
    return jsonify({
        "error": "Erreur interne du serveur",
        "message": "Une erreur s'est produite lors du traitement de votre requête"
    }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Exception non gérée: {str(e)}", exc_info=True)
    return jsonify({
        "error": "Erreur inattendue",
        "message": str(e)
    }), 500

@app.route('/')
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        "api": "Immune System API",
        "version": "1.0.0",
        "description": "API de simulation du système immunitaire",
        "status": "opérationnel",
        "endpoints": {
            "status": "/api/immune/status",
            "data": "/api/immune/data",
            "simulate": "/api/immune/simulate/<condition>",
            "parameters": "/api/immune/parameters",
            "configure": "/api/immune/configure"
        }
    })

@app.route('/api/immune/status', methods=['GET'])
def get_status():
    """Retourne le statut du système immunitaire"""
    try:
        return jsonify({
            "status": "operational",
            "organ": "immune_system",
            "health_status": simulator.health_status,
            "active_conditions": simulator.active_conditions,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/immune/data', methods=['GET'])
def get_data():
    """Retourne les données synthétiques courantes"""
    try:
        return jsonify(simulator.generate_immune_data())
    except Exception as e:
        logger.error(f"Erreur dans get_data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/immune/simulate/<condition>', methods=['POST'])
def simulate_condition(condition):
    """Simule une pathologie du système immunitaire"""
    try:
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
    except Exception as e:
        logger.error(f"Erreur dans simulate_condition: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/immune/parameters', methods=['GET'])
def get_parameters():
    """Retourne les paramètres de simulation disponibles"""
    try:
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
    except Exception as e:
        logger.error(f"Erreur dans get_parameters: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/immune/configure', methods=['POST'])
def configure():
    """Configure les paramètres du patient"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Aucune donnée JSON fournie"
            }), 400
        
        # Validation des données
        if 'age' in data:
            try:
                age = int(data['age'])
                if age < 0 or age > 120:
                    return jsonify({
                        "success": False,
                        "error": "L'âge doit être entre 0 et 120 ans"
                    }), 400
                simulator.age = age
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": "L'âge doit être un nombre entier"
                }), 400
        
        if 'sex' in data:
            sex = str(data['sex']).upper()
            if sex not in ['M', 'F']:
                return jsonify({
                    "success": False,
                    "error": "Le sexe doit être 'M' ou 'F'"
                }), 400
            simulator.sex = sex
        
        if 'health_status' in data:
            valid_statuses = ["normal", "infection", "autoimmune", "immunodeficiency", "allergic_reaction"]
            if data['health_status'] not in valid_statuses:
                return jsonify({
                    "success": False,
                    "error": f"État de santé invalide. Valeurs acceptées: {', '.join(valid_statuses)}"
                }), 400
            simulator.health_status = data['health_status']
        
        logger.info(f"Configuration mise à jour: age={simulator.age}, sex={simulator.sex}, status={simulator.health_status}")
        
        return jsonify({
            "success": True,
            "message": "Configuration mise à jour",
            "current_config": {
                "age": simulator.age,
                "sex": simulator.sex,
                "health_status": simulator.health_status
            }
        })
    except Exception as e:
        logger.error(f"Erreur dans configure: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("=" * 60)
        logger.info("Démarrage de l'API Immune System")
        logger.info("=" * 60)
        logger.info("URL: http://127.0.0.1:5004")
        logger.info("Appuyez sur Ctrl+C pour arrêter le serveur")
        logger.info("=" * 60)
        
        app.run(debug=True, port=5004, host='0.0.0.0')
    except KeyboardInterrupt:
        logger.info("\nArrêt du serveur...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erreur fatale: {str(e)}", exc_info=True)
        sys.exit(1)