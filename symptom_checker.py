

class SymptomChecker:
    def __init__(self):
        self.symptoms = [
            'fever', 'headache', 'cough', 'sore_throat', 'runny_nose', 'fatigue',
            'nausea', 'vomiting', 'diarrhea', 'stomach_pain', 'muscle_aches',
            'chest_pain', 'shortness_of_breath', 'dizziness', 'rash', 'joint_pain',
            'back_pain', 'difficulty_swallowing', 'loss_of_appetite', 'weight_loss',
            'night_sweats', 'chills', 'confusion', 'memory_problems', 'blurred_vision',
            'ear_pain', 'difficulty_urinating', 'frequent_urination', 'constipation',
            'difficulty_sleeping', 'insomnia', 'anxiety', 'stress', 'weakness',
            'tremors', 'sweating', 'dry_mouth', 'abdominal_pain', 'bloating',
            'heartburn', 'acid_reflux', 'swollen_lymph_nodes', 'bruising',
            'pale_skin', 'rapid_heartbeat', 'irregular_heartbeat', 'high_blood_pressure',
            'low_blood_pressure', 'tingling', 'numbness', 'leg_cramps', 'restlessness'
        ]
    
    def get_available_symptoms(self):
        """Return list of available symptoms"""
        return self.symptoms.copy()
    
    def validate_symptoms(self, user_symptoms):
        """Validate user-provided symptoms"""
        valid_symptoms = []
        for symptom in user_symptoms:
            if symptom.lower() in self.symptoms:
                valid_symptoms.append(symptom.lower())
        return valid_symptoms
