

from sklearn.tree import DecisionTreeClassifier
import numpy as np

class DiagnosticEngine:
    def __init__(self):
        self.illnesses = {
            'common_cold': ['runny_nose', 'sore_throat', 'cough', 'fatigue'],
            'flu': ['fever', 'muscle_aches', 'fatigue', 'headache', 'cough'],
            'pneumonia': ['fever', 'cough', 'chest_pain', 'shortness_of_breath'],
            'gastroenteritis': ['nausea', 'vomiting', 'diarrhea', 'stomach_pain', 'abdominal_pain'],
            'migraine': ['headache', 'nausea', 'blurred_vision', 'dizziness'],
            'allergic_reaction': ['rash', 'runny_nose', 'shortness_of_breath'],
            'urinary_tract_infection': ['frequent_urination', 'difficulty_urinating', 'fever'],
            'arthritis': ['joint_pain', 'muscle_aches', 'fatigue'],
            'anxiety_disorder': ['chest_pain', 'shortness_of_breath', 'dizziness', 'fatigue', 'anxiety', 'restlessness'],
            'depression': ['fatigue', 'loss_of_appetite', 'memory_problems', 'difficulty_sleeping', 'weakness'],
            'diabetes': ['frequent_urination', 'fatigue', 'blurred_vision', 'weight_loss'],
            'hypertension': ['headache', 'dizziness', 'chest_pain', 'shortness_of_breath', 'high_blood_pressure'],
            'hypotension': ['dizziness', 'weakness', 'fatigue', 'low_blood_pressure'],
            'anemia': ['fatigue', 'weakness', 'pale_skin', 'shortness_of_breath'],
            'heart_disease': ['chest_pain', 'shortness_of_breath', 'rapid_heartbeat', 'irregular_heartbeat'],
            'acid_reflux': ['heartburn', 'acid_reflux', 'chest_pain', 'dry_mouth'],
            'insomnia': ['difficulty_sleeping', 'insomnia', 'fatigue', 'memory_problems']
        }
        
        self.all_symptoms = ['fever', 'headache', 'cough', 'sore_throat', 'runny_nose', 'fatigue',
                           'nausea', 'vomiting', 'diarrhea', 'stomach_pain', 'muscle_aches',
                           'chest_pain', 'shortness_of_breath', 'dizziness', 'rash', 'joint_pain',
                           'back_pain', 'difficulty_swallowing', 'loss_of_appetite', 'weight_loss',
                           'night_sweats', 'chills', 'confusion', 'memory_problems', 'blurred_vision',
                           'ear_pain', 'difficulty_urinating', 'frequent_urination', 'constipation',
                           'difficulty_sleeping', 'insomnia', 'anxiety', 'stress', 'weakness',
                           'tremors', 'sweating', 'dry_mouth', 'abdominal_pain', 'bloating',
                           'heartburn', 'acid_reflux', 'swollen_lymph_nodes', 'bruising',
                           'pale_skin', 'rapid_heartbeat', 'irregular_heartbeat', 'high_blood_pressure',
                           'low_blood_pressure', 'tingling', 'numbness', 'leg_cramps', 'restlessness']
        
        self.clf = DecisionTreeClassifier(random_state=42)
        self._train_model()
    
    def _train_model(self):
        """Train the decision tree model"""
        X, y = [], []
        
        for illness, symptoms in self.illnesses.items():
            for _ in range(5):  # Generate multiple samples per illness
                sample = [0] * len(self.all_symptoms)
                for symptom in symptoms:
                    if symptom in self.all_symptoms:
                        sample[self.all_symptoms.index(symptom)] = 1
                
                # Add some noise
                for i in range(len(sample)):
                    if np.random.random() < 0.1:
                        sample[i] = 1 - sample[i]
                
                X.append(sample)
                y.append(illness)
        
        self.clf.fit(X, y)
    
    def analyze_symptoms(self, user_symptoms):
        """Analyze symptoms and return possible diagnoses"""
        if not user_symptoms:
            return []
        
        # Convert symptoms to feature vector
        features = [0] * len(self.all_symptoms)
        for symptom in user_symptoms:
            if symptom in self.all_symptoms:
                features[self.all_symptoms.index(symptom)] = 1
        
        # Get prediction probabilities
        probabilities = self.clf.predict_proba([features])[0]
        classes = self.clf.classes_
        
        # Create diagnosis results
        results = []
        for i, prob in enumerate(probabilities):
            if prob > 0.1:  # Only include significant probabilities
                results.append({
                    'name': classes[i].replace('_', ' ').title(),
                    'confidence': prob * 100,
                    'symptoms_match': self._calculate_symptom_match(user_symptoms, classes[i])
                })
        
        # Sort by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results[:3]  # Return top 3
    
    def _calculate_symptom_match(self, user_symptoms, illness):
        """Calculate how many symptoms match the illness"""
        illness_symptoms = self.illnesses.get(illness, [])
        matches = len(set(user_symptoms) & set(illness_symptoms))
        return matches
    
    def format_diagnosis_report(self, diagnoses, symptoms):
        """Format diagnosis results into a readable report"""
        report = f"DIAGNOSIS REPORT\n\nSymptoms analyzed: {', '.join([s.replace('_', ' ').title() for s in symptoms])}\n\n"
        
        if not diagnoses:
            report += "No specific diagnosis found. Please consult a healthcare professional."
            return report
        
        report += "Possible conditions:\n\n"
        for i, diagnosis in enumerate(diagnoses, 1):
            report += f"{i}. {diagnosis['name']}\n"
            report += f"   Confidence: {diagnosis['confidence']:.1f}%\n"
            report += f"   Symptom matches: {diagnosis['symptoms_match']}\n\n"
        
        report += "DISCLAIMER: This is for informational purposes only.\nAlways consult a healthcare professional for proper diagnosis!"
        return report
