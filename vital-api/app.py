from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

# ===================== CLASSES PAR ORGANE ==========================

# === Cœur ==========================================================
class CardiacSystem:
    def __init__(self):
        self.parameters = {
            "heart_rate": (60, 100),
            "blood_pressure_systolic": (90, 120),
            "blood_pressure_diastolic": (60, 80),
            "oxygen_saturation": (95, 100)
        }
        self.active_conditions = set()

    def get_status(self):
        status = "Fonctionne normalement" if not self.active_conditions else "Pathologique"
        return {"organ": "Cœur", "status": status, "active_conditions": list(self.active_conditions)}

    def generate_data(self):
        hr = random.randint(*self.parameters["heart_rate"])
        sys = random.randint(*self.parameters["blood_pressure_systolic"])
        dia = random.randint(*self.parameters["blood_pressure_diastolic"])
        spo2 = random.randint(*self.parameters["oxygen_saturation"])

        # effets simples des conditions
        if "tachycardie" in self.active_conditions:
            hr = max(100, int(hr * 1.4))
        if "bradycardie" in self.active_conditions:
            hr = min(60, int(hr * 0.6))
        if "hypertension" in self.active_conditions:
            sys = max(sys, int(sys * 1.25))

        return {
            "heart_rate": hr,
            "blood_pressure_systolic": sys,
            "blood_pressure_diastolic": dia,
            "oxygen_saturation": spo2,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def simulate(self, condition):
        valid = {"tachycardie", "bradycardie", "arythmie", "hypertension"}
        if condition not in valid:
            return {"error": "Condition inconnue"}, 400
        # toggle condition
        if condition in self.active_conditions:
            self.active_conditions.remove(condition)
            return {"message": f"{condition} désactivée", "active_conditions": list(self.active_conditions)}
        else:
            self.active_conditions.add(condition)
            return {"message": f"{condition} activée", "active_conditions": list(self.active_conditions)}


# === Poumons ========================================================
class RespiratorySystem:
    def __init__(self):
        self.parameters = {
            "respiratory_rate": (12, 20),
            "tidal_volume": (400, 600),
            "vital_capacity": (3000, 5000),
            "blood_gases": {"PaO2": (80, 100), "PaCO2": (35, 45), "pH": (7.35, 7.45)}
        }
        self.active_conditions = set()

    def get_status(self):
        status = "Fonctionne normalement" if not self.active_conditions else "Pathologique"
        return {"organ": "Poumons", "status": status, "active_conditions": list(self.active_conditions)}

    def generate_data(self):
        rr = random.randint(*self.parameters["respiratory_rate"])
        tv = random.randint(*self.parameters["tidal_volume"])
        vc = random.randint(*self.parameters["vital_capacity"])
        pao2 = random.randint(*self.parameters["blood_gases"]["PaO2"])
        paco2 = random.randint(*self.parameters["blood_gases"]["PaCO2"])
        ph = round(random.uniform(*self.parameters["blood_gases"]["pH"]), 2)

        if "asthme" in self.active_conditions:
            rr = max(rr, 25)
            tv = max(200, int(tv * 0.7))
        if "bpco" in self.active_conditions:
            tv = max(200, int(tv * 0.6))
            pao2 = min(pao2, 85)
        if "apnee" in self.active_conditions:
            rr = 0
            pao2 = max(50, pao2 - 30)
        if "hyperventilation" in self.active_conditions:
            rr = max(rr, 30)
            paco2 = max(20, paco2 - 15)

        return {
            "respiratory_rate": rr,
            "tidal_volume": tv,
            "vital_capacity": vc,
            "blood_gases": {"PaO2": pao2, "PaCO2": paco2, "pH": ph},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def simulate(self, condition):
        valid = {"asthme", "bpco", "apnee", "hyperventilation"}
        if condition not in valid:
            return {"error": "Condition inconnue"}, 400
        if condition in self.active_conditions:
            self.active_conditions.remove(condition)
            return {"message": f"{condition} désactivée", "active_conditions": list(self.active_conditions)}
        else:
            self.active_conditions.add(condition)
            return {"message": f"{condition} activée", "active_conditions": list(self.active_conditions)}


# === Cerveau ========================================================
class NeuralSystem:
    def __init__(self):
        self.parameters = {
            "EEG_rhythm": ["alpha", "beta", "theta", "delta"],
            "reaction_time": (200, 400),  # ms
            "neurotransmitters": {"dopamine": (50, 100), "serotonin": (50, 100)}
        }
        self.active_conditions = set()

    def get_status(self):
        status = "Fonctionne normalement" if not self.active_conditions else "Pathologique"
        return {"organ": "Cerveau", "status": status, "active_conditions": list(self.active_conditions)}

    def generate_data(self):
        eeg = random.choice(self.parameters["EEG_rhythm"])
        rt = random.randint(*self.parameters["reaction_time"])
        dopamine = random.randint(*self.parameters["neurotransmitters"]["dopamine"])
        serotonin = random.randint(*self.parameters["neurotransmitters"]["serotonin"])

        if "epilepsie" in self.active_conditions:
            eeg = "delta"
            rt = min(rt * 2, 2000)
        if "migraine" in self.active_conditions:
            rt = max(rt, 600)
        if "trouble_sommeil" in self.active_conditions:
            eeg = "theta"
        if "stress" in self.active_conditions:
            dopamine = max(10, dopamine - 30)
            serotonin = max(10, serotonin - 20)

        return {
            "EEG_rhythm": eeg,
            "reaction_time_ms": rt,
            "neurotransmitters": {"dopamine": dopamine, "serotonin": serotonin},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def simulate(self, condition):
        valid = {"epilepsie", "migraine", "trouble_sommeil", "stress"}
        if condition not in valid:
            return {"error": "Condition inconnue"}, 400
        if condition in self.active_conditions:
            self.active_conditions.remove(condition)
            return {"message": f"{condition} désactivée", "active_conditions": list(self.active_conditions)}
        else:
            self.active_conditions.add(condition)
            return {"message": f"{condition} activée", "active_conditions": list(self.active_conditions)}


# === Foie ===========================================================
class HepaticSystem:
    def __init__(self):
        self.parameters = {
            "ALT": (7, 56),  # U/L
            "AST": (10, 40),  # U/L
            "bilirubin": (0.1, 1.2),  # mg/dL
            "albumin": (3.5, 5.0)  # g/dL
        }
        self.active_conditions = set()

    def get_status(self):
        status = "Fonctionne normalement" if not self.active_conditions else "Pathologique"
        return {"organ": "Foie", "status": status, "active_conditions": list(self.active_conditions)}

    def generate_data(self):
        alt = random.randint(*self.parameters["ALT"])
        ast = random.randint(*self.parameters["AST"])
        bilirubin = round(random.uniform(*self.parameters["bilirubin"]), 2)
        albumin = round(random.uniform(*self.parameters["albumin"]), 2)

        if "hepatite" in self.active_conditions:
            alt = max(alt, 150)
            ast = max(ast, 120)
        if "cirrhose" in self.active_conditions:
            bilirubin = max(bilirubin, 3.0)
            albumin = min(albumin, 2.5)

        return {
            "ALT": alt,
            "AST": ast,
            "bilirubin": bilirubin,
            "albumin": albumin,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def simulate(self, condition):
        valid = {"hepatite", "cirrhose"}
        if condition not in valid:
            return {"error": "Condition inconnue"}, 400
        if condition in self.active_conditions:
            self.active_conditions.remove(condition)
            return {"message": f"{condition} désactivée", "active_conditions": list(self.active_conditions)}
        else:
            self.active_conditions.add(condition)
            return {"message": f"{condition} activée", "active_conditions": list(self.active_conditions)}


# ===================== INSTANCES ==========================
cardiac = CardiacSystem()
respiratory = RespiratorySystem()
neural = NeuralSystem()
hepatic = HepaticSystem()

# ===================== ROUTES UTILITAIRES ==========================
def _register_route(f, route, methods=None):
    """Helper pour enregistrer dynamiquement une view sous un nom unique."""
    endpoint = f.__name__ + "_" + str(route)
    app.add_url_rule(route, endpoint=endpoint, view_func=f, methods=methods or ["GET"])

def build_routes(organ_name, organ_obj):
    # status
    def status_func(org=organ_obj):
        return jsonify(org.get_status())
    status_func.__name__ = f"{organ_name}_status"
    _register_route(status_func, f"/api/{organ_name}/status", methods=["GET"])

    # data (GET)
    def data_func(org=organ_obj):
        # on pourrait accepter des query params pour override (non persistant)
        return jsonify(org.generate_data())
    data_func.__name__ = f"{organ_name}_data"
    _register_route(data_func, f"/api/{organ_name}/data", methods=["GET"])

    # simulate (POST)
    def simulate_func(condition, org=organ_obj):
        result = org.simulate(condition)
        # handle returned (body, status) tuple
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], int):
            return jsonify(result[0]), result[1]
        return jsonify(result)
    simulate_func.__name__ = f"{organ_name}_simulate"
    _register_route(simulate_func, f"/api/{organ_name}/simulate/<condition>", methods=["POST"])

    # parameters
    def parameters_func(org=organ_obj):
        return jsonify(org.parameters)
    parameters_func.__name__ = f"{organ_name}_parameters"
    _register_route(parameters_func, f"/api/{organ_name}/parameters", methods=["GET"])


# Build all vital organs
build_routes("cardiac", cardiac)
build_routes("respiratory", respiratory)
build_routes("neural", neural)
build_routes("hepatic", hepatic)

# ===================== RUN SERVER ==========================
if __name__ == "__main__":
    app.run(debug=True, port=5003)
