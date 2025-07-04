

import sqlite3
import json
import os
from datetime import datetime

class HealthDatabase:
    def __init__(self, db_name="health_data.db"):
        """Initialize database connection"""
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.init_database()
    
    def init_database(self):
        """Initialize database - tables already exist"""
        # Tables are already created, no need to create them again
        print("Database tables already exist - initialization complete")
    
    def save_diagnosis(self, symptoms, diagnosis, confidence):
        """Save a diagnosis to the database"""
        try:
            symptoms_str = json.dumps(symptoms) if isinstance(symptoms, list) else str(symptoms)
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO diagnoses (date, symptoms, diagnosis, confidence)
                    VALUES (?, ?, ?, ?)
                ''', (date_str, symptoms_str, diagnosis, confidence))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving diagnosis: {e}")
            return False
    
    def get_diagnosis_history(self, limit=10):
        """Get recent diagnosis history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT date, symptoms, diagnosis, confidence 
                    FROM diagnoses 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (limit,))
                
                results = []
                for row in cursor.fetchall():
                    date, symptoms_str, diagnosis, confidence = row
                    
                    # Parse symptoms
                    try:
                        symptoms = json.loads(symptoms_str)
                        if isinstance(symptoms, list):
                            symptoms_display = ', '.join([s.replace('_', ' ').title() for s in symptoms])
                        else:
                            symptoms_display = str(symptoms)
                    except:
                        symptoms_display = str(symptoms_str)
                    
                    results.append((date, symptoms_display, diagnosis, confidence))
                
                return results
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []
    
    def get_database_stats(self):
        """Get basic database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total diagnoses
                cursor.execute('SELECT COUNT(*) FROM diagnoses')
                total_diagnoses = cursor.fetchone()[0]
                
                # Most common diagnosis
                cursor.execute('''
                    SELECT diagnosis, COUNT(*) as count 
                    FROM diagnoses 
                    GROUP BY diagnosis 
                    ORDER BY count DESC 
                    LIMIT 1
                ''')
                most_common_result = cursor.fetchone()
                most_common = f"{most_common_result[0]} ({most_common_result[1]}x)" if most_common_result else "None"
                
                # Database file size
                try:
                    db_size = os.path.getsize(self.db_path)
                except:
                    db_size = 0
                
                return {
                    'total_diagnoses': total_diagnoses,
                    'most_common': most_common,
                    'database_size': db_size
                }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {'total_diagnoses': 0, 'most_common': 'Error', 'database_size': 0}
    


    def get_tips_by_category(self, category):
        """Get tips by category"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT tip_text FROM health_tips WHERE category = ?
                ''', (category,))
                return [tip[0] for tip in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting tips: {e}")
            return []

    def get_all_tips(self):
        """Get all health tips"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT category, tip_text FROM health_tips')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting tips: {e}")
            return []
