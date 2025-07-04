import tempfile
import webbrowser
import os
import sqlite3
from database import HealthDatabase

class HealthTips:
    def __init__(self):
        self.database = HealthDatabase()
    
    def get_general_tips(self):
        """Get general health tips from database"""
        return self.database.get_tips_by_category('general')
    
    def get_nutrition_tips(self):
        """Get nutrition tips from database"""
        return self.database.get_tips_by_category('nutrition')
    
    def get_mental_health_tips(self):
        """Get mental health tips from database"""
        return self.database.get_tips_by_category('mental_health')
    
    def get_disease_specific_tips(self, condition):
        """Get tips specific to a medical condition"""
        try:
            # Normalize condition name for better matching
            condition_normalized = condition.lower().replace(' ', '_')
            
            with sqlite3.connect(self.database.db_path) as conn:
                cursor = conn.cursor()
                # Try multiple search patterns for better matching
                cursor.execute('''
                    SELECT tip_text FROM health_tips 
                    WHERE condition_related = ? 
                       OR condition_related = ?
                       OR condition_related LIKE ?
                       OR condition_related LIKE ?
                    ORDER BY category
                ''', (condition, condition_normalized, f'%{condition}%', f'%{condition_normalized}%'))
                
                results = [tip[0] for tip in cursor.fetchall()]
                
                # If no specific tips found, try partial matching with key words
                if not results:
                    key_words = ['uti', 'infection', 'arthritis', 'diabetes', 'anxiety', 'depression', 'hypertension', 'heart']
                    for word in key_words:
                        if word in condition_normalized:
                            cursor.execute('''
                                SELECT tip_text FROM health_tips 
                                WHERE condition_related LIKE ?
                            ''', (f'%{word}%',))
                            results.extend([tip[0] for tip in cursor.fetchall()])
                            break
                
                return results
        except Exception as e:
            print(f"Error getting disease tips: {e}")
            return []
    
    def get_personalized_tips(self, recent_diagnoses=None):
        """Get personalized tips based on recent diagnoses"""
        if not recent_diagnoses:
            return self.get_general_tips()
        
        personalized_tips = []
        
        # Get disease-specific tips for each diagnosis
        for diagnosis in recent_diagnoses[:3]:  # Last 3 diagnoses
            # Try multiple condition formats
            condition_formats = [
                diagnosis.lower().replace(' ', '_'),  # urinary_tract_infection
                diagnosis.lower(),                    # urinary tract infection
                diagnosis                            # Original format
            ]
            
            for condition in condition_formats:
                disease_tips = self.get_disease_specific_tips(condition)
                if disease_tips:
                    personalized_tips.extend(disease_tips[:2])  # Top 2 tips per condition
                    break  # Found tips, no need to try other formats
        
        # Add some general tips to fill up
        general_tips = self.get_general_tips()
        personalized_tips.extend(general_tips[:max(3, 8-len(personalized_tips))])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tips = []
        for tip in personalized_tips:
            if tip not in seen:
                seen.add(tip)
                unique_tips.append(tip)
        
        return unique_tips[:8]  # Return max 8 tips
    
    def get_all_tips_by_category(self):
        """Get all tips organized by category"""
        all_tips = self.database.get_all_tips()
        organized = {}
        for category, tip_text in all_tips:
            if category not in organized:
                organized[category] = []
            organized[category].append(tip_text)
        return organized

    def show_tips_in_browser(self, tips, title="Health Tips"):
        """Display tips in a web browser"""
        if not tips:  # If no tips provided, get general tips
            tips = self.get_general_tips()
            title = "General Health Tips"
            
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .tip {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .tip-number {{ color: #3498db; font-weight: bold; }}
                .personalized {{ border-left: 4px solid #e74c3c; }}
                .general {{ border-left: 4px solid #3498db; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
        """
        
        for i, tip in enumerate(tips, 1):
            tip_class = "personalized" if "Based on" in title else "general"
            html_content += f'<div class="tip {tip_class}"><span class="tip-number">{i}.</span> {tip}</div>'
        
        html_content += """
            <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
                <p>Remember: These are general tips. Always consult healthcare professionals for personalized advice!</p>
            </div>
        </body>
        </html>
        """
        
        # Create temporary file and open in browser
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_file = f.name
        
        try:
            webbrowser.open('file://' + temp_file)
        except Exception as e:
            print(f"Could not open browser: {e}")
        
        return temp_file

    def show_smart_tips(self):
        """Smart method that automatically shows personalized or general tips"""
        try:
            # Try to get recent diagnoses from database
            with sqlite3.connect(self.database.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT diagnosis FROM diagnoses 
                    ORDER BY created_at DESC 
                    LIMIT 3
                ''')
                recent_diagnoses = [row[0].lower().replace(' ', '_') for row in cursor.fetchall()]
            
            if recent_diagnoses:
                # Show personalized tips
                tips = self.get_personalized_tips(recent_diagnoses)
                conditions = ", ".join([d.replace('_', ' ').title() for d in recent_diagnoses[:2]])
                title = f"Personalized Tips Based on: {conditions}"
                self.show_tips_in_browser(tips, title)
                return f"Personalized health tips opened!\nBased on: {conditions}"
            else:
                # Show general tips
                tips = self.get_general_tips()
                self.show_tips_in_browser(tips, "General Health Tips")
                return "General health tips opened in browser!"
                
        except Exception as e:
            print(f"Error getting smart tips: {e}")
            # Fallback to general tips
            tips = self.get_general_tips()
            self.show_tips_in_browser(tips, "General Health Tips")
            return "General health tips opened in browser!"
    
    def show_disease_specific_tips_browser(self, condition):
        """Show tips for a specific medical condition in browser"""
        tips = self.get_disease_specific_tips(condition)
        if not tips:
            tips = self.get_general_tips()[:5]  # Fallback to general tips
            title = f"General Health Tips (No specific tips for {condition.replace('_', ' ').title()})"
        else:
            title = f"Health Tips for {condition.replace('_', ' ').title()}"
        
        return self.show_tips_in_browser(tips, title)
    
    def show_personalized_tips_browser(self, recent_diagnoses=None):
        """Show personalized tips based on diagnosis history"""
        tips = self.get_personalized_tips(recent_diagnoses)
        if recent_diagnoses:
            conditions = ", ".join([d.replace('_', ' ').title() for d in recent_diagnoses[:2]])
            title = f"Personalized Tips Based on: {conditions}"
        else:
            title = "General Health Tips"
        
        return self.show_tips_in_browser(tips, title)
