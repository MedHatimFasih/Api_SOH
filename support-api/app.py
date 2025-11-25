from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# --- Classes des organes (mêmes que avant) ---
class RenalSystem:
    def __init__(self):
        self.parameters = {"filtration_rate": (80, 120), "urine_output": (1, 3), "creatinine": (0.6, 1.2)}

    def get_status(self):
        return {"organ": "Reins", "status": "Fonctionne normalement"}

    def generate_data(self):
        return {"filtration_rate": random.randint(80, 120),
                "urine_output": round(random.uniform(1, 3), 2),
                "creatinine": round(random.uniform(0.6, 1.2), 2)}

    def simulate(self, condition):
        if condition == "insuffisance":
            return {"simulation": "Insuffisance rénale", "filtration_rate": 40}
        if condition == "infection":
            return {"simulation": "Infection urinaire", "creatinine": 1.8}
        return {"error": "Condition inconnue"}


class DigestiveSystem:
    def __init__(self):
        self.parameters = {"acid_level": (1, 3), "motility": (70, 100), "absorption": (80, 100)}

    def get_status(self):
        return {"organ": "Système digestif", "status": "Fonctionne normalement"}

    def generate_data(self):
        return {"acid_level": round(random.uniform(1, 3), 2),
                "motility": random.randint(70, 100),
                "absorption": random.randint(80, 100)}

    def simulate(self, condition):
        if condition == "ulcere":
            return {"simulation": "Ulcère gastrique", "acid_level": 4.5}
        if condition == "diarrhee":
            return {"simulation": "Diarrhée", "motility": 120}
        return {"error": "Condition inconnue"}


class DermalSystem:
    def __init__(self):
        self.parameters = {"hydration": (40, 70), "temperature": (33, 36)}

    def get_status(self):
        return {"organ": "Peau", "status": "Fonctionne normalement"}

    def generate_data(self):
        return {"hydration": random.randint(40, 70),
                "temperature": round(random.uniform(33, 36), 2)}

    def simulate(self, condition):
        if condition == "brulure":
            return {"simulation": "Brûlure", "hydration": 20}
        if condition == "eczema":
            return {"simulation": "Eczéma", "temperature": 38}
        return {"error": "Condition inconnue"}


class EndocrineSystem:
    def __init__(self):
        self.parameters = {"insulin": (4, 7), "cortisol": (5, 20), "thyroid_hormone": (0.8, 1.8)}

    def get_status(self):
        return {"organ": "Système endocrinien", "status": "Fonctionne normalement"}

    def generate_data(self):
        return {"insulin": round(random.uniform(4, 7), 2),
                "cortisol": random.randint(5, 20),
                "thyroid_hormone": round(random.uniform(0.8, 1.8), 2)}

    def simulate(self, condition):
        if condition == "diabete":
            return {"simulation": "Diabète", "insulin": 1.2}
        if condition == "stress":
            return {"simulation": "Stress", "cortisol": 35}
        return {"error": "Condition inconnue"}


# --- Instances ---
renal = RenalSystem()
digestive = DigestiveSystem()
dermal = DermalSystem()
endocrine = EndocrineSystem()


# --- Génération dynamique des routes ---
def build_routes(organ_name, organ_obj):

    @app.get(f"/api/{organ_name}/status", endpoint=f"{organ_name}_status")
    def status_func():
        return jsonify(organ_obj.get_status())

    @app.get(f"/api/{organ_name}/data", endpoint=f"{organ_name}_data")
    def data_func():
        return jsonify(organ_obj.generate_data())

    @app.post(f"/api/{organ_name}/simulate/<condition>", endpoint=f"{organ_name}_simulate")
    def simulate_func(condition):
        return jsonify(organ_obj.simulate(condition))

    @app.get(f"/api/{organ_name}/parameters", endpoint=f"{organ_name}_parameters")
    def parameters_func():
        return jsonify(organ_obj.parameters)


# --- Créer toutes les routes ---
build_routes("renal", renal)
build_routes("digestive", digestive)
build_routes("dermal", dermal)
build_routes("endocrine", endocrine)


# --- Lancer le serveur ---
if __name__ == "__main__":
    app.run(port=5002, debug=True)
