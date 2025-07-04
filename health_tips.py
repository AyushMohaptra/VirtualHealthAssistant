#!/usr/bin/env python3
"""Health Tips Module"""

import tempfile
import webbrowser
import os

class HealthTips:
    def __init__(self):
        self.tips_data = {
            'general': [
                "Drink at least 8 glasses of water daily",
                "Get 7-9 hours of sleep each night",
                "Exercise for at least 30 minutes daily",
                "Eat 5 servings of fruits and vegetables daily",
                "Practice stress management techniques",
                "Wash hands frequently to prevent infections",
                "Maintain good posture throughout the day",
                "Take regular breaks from screen time",
                "Practice deep breathing exercises",
                "Schedule regular health checkups"
            ],
            'nutrition': [
                "Choose whole grains over refined grains",
                "Limit processed and sugary foods",
                "Include protein in every meal",
                "Cook meals at home when possible",
                "Read nutrition labels carefully"
            ],
            'mental_health': [
                "Practice mindfulness and meditation",
                "Stay connected with friends and family",
                "Engage in hobbies you enjoy",
                "Seek professional help when needed",
                "Maintain a positive outlook"
            ]
        }
    
    def get_general_tips(self):
        """Get general health tips"""
        return self.tips_data['general']
    
    def get_nutrition_tips(self):
        """Get nutrition tips"""
        return self.tips_data['nutrition']
    
    def get_mental_health_tips(self):
        """Get mental health tips"""
        return self.tips_data['mental_health']
    
    def show_tips_in_browser(self, tips, title="Health Tips"):
        """Display tips in a web browser"""
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
            </style>
        </head>
        <body>
            <h1>{title}</h1>
        """
        
        for i, tip in enumerate(tips, 1):
            html_content += f'<div class="tip"><span class="tip-number">{i}.</span> {tip}</div>'
        
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
