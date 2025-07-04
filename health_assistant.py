import tkinter as tk
from tkinter import messagebox

try:
    from symptom_checker import SymptomChecker
    from diagnostic_engine import DiagnosticEngine
    from health_tips import HealthTips
    from database import HealthDatabase
except ImportError as e:
    print(f"Error: {e}"); exit(1)

class HealthAssistant:
    def __init__(self):
        # Initialize all modules
        self.symptom_checker, self.diagnostic_engine = SymptomChecker(), DiagnosticEngine()
        self.health_tips, self.database = HealthTips(), HealthDatabase()
        self.current_symptoms = {}
        
        # Setup main window
        self.root = tk.Tk()
        self.root.title("Health Assistant")
        self.root.geometry("550x450")
        
        # Title
        tk.Label(self.root, text="Health Assistant", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Buttons
        for i, (buttons) in enumerate([
            [("Report Symptoms", self.report_symptoms, 'lightblue'),
             ("Get Diagnosis", self.get_diagnosis, 'lightgreen'),
             ("Health Tips", self.show_tips, 'lightcoral')],
            [("View History", self.view_history, 'lightyellow'),
             ("Database Stats", self.show_stats, 'lightcyan')]
        ]):
            frame = tk.Frame(self.root)
            frame.pack(pady=5 if i else 10)
            for text, cmd, color in buttons:
                tk.Button(frame, text=text, command=cmd, bg=color, width=15).pack(side=tk.LEFT, padx=5)
        
        # Status and results
        self.symptoms_label = tk.Label(self.root, text="No symptoms recorded", font=('Arial', 10), fg='blue')
        self.symptoms_label.pack(pady=10)
        
        results_frame = tk.LabelFrame(self.root, text="Results", font=('Arial', 12, 'bold'))
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.results_text = tk.Text(results_frame, height=12, wrap=tk.WORD, font=('Arial', 9))
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.update_results("Welcome! Select symptoms and get AI diagnosis.")
    
    def report_symptoms(self):
        """Symptom selection window"""
        window = tk.Toplevel(self.root)
        window.title("Select Symptoms")
        window.geometry("450x600")  # Made larger
        tk.Label(window, text="Select your symptoms:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Create scrollable frame
        canvas = tk.Canvas(window)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add symptoms to scrollable frame
        self.symptom_vars = {}
        for symptom in self.symptom_checker.get_available_symptoms():
            var = tk.BooleanVar()
            tk.Checkbutton(scrollable_frame, text=symptom.replace('_', ' ').title(), 
                          variable=var, font=('Arial', 10)).pack(anchor='w', padx=20, pady=2)
            self.symptom_vars[symptom] = var
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 10))
        scrollbar.pack(side="right", fill="y", pady=(0, 10))
        
        tk.Button(window, text="Save", bg='lightgreen', font=('Arial', 11, 'bold'),
                 command=lambda: self.save_symptoms(window)).pack(pady=10)
    
    def save_symptoms(self, window):
        """Save selected symptoms"""
        selected = [s for s, var in self.symptom_vars.items() if var.get()]
        if not selected:
            return messagebox.showwarning("No Selection", "Please select at least one symptom!")
        
        self.current_symptoms = {s: True for s in selected}
        symptoms_text = ", ".join([s.replace('_', ' ').title() for s in selected])
        self.symptoms_label.config(text=f"Current: {symptoms_text}")
        self.update_results(f"Recorded: {symptoms_text}")
        window.destroy()
    
    def get_diagnosis(self):
        """Get AI diagnosis"""
        if not self.current_symptoms:
            return messagebox.showwarning("No Symptoms", "Please report symptoms first!")
        
        symptoms_list = list(self.current_symptoms.keys())
        diagnoses = self.diagnostic_engine.analyze_symptoms(symptoms_list)
        
        if diagnoses:
            top = diagnoses[0]
            self.database.save_diagnosis(symptoms_list, top['name'], top['confidence'])
            report = self.diagnostic_engine.format_diagnosis_report(diagnoses, symptoms_list)
            self.update_results(report + "\nSaved to database!")
        else:
            self.update_results("No diagnosis found. Please consult a doctor.")
    
    def view_history(self):
        """Show diagnosis history"""
        history = self.database.get_diagnosis_history(10)
        if not history:
            return messagebox.showinfo("No History", "No previous diagnoses found.")
        
        text = "DIAGNOSIS HISTORY:\n\n"
        for i, (date, symptoms, diagnosis, confidence) in enumerate(history, 1):
            text += f"{i}. {date}\n   Symptoms: {symptoms}\n   Diagnosis: {diagnosis}"
            text += f" ({confidence:.1f}%)" if confidence > 0 else ""
            text += "\n\n"
        self.update_results(text)
    
    def show_tips(self):
        """Show smart health tips (automatically personalized or general)"""
        result_message = self.health_tips.show_smart_tips()
        self.update_results(result_message)
    
    def show_stats(self):
        """Show database statistics"""
        stats = self.database.get_database_stats()
        
        text = f"DATABASE STATISTICS\n\nDiagnosis Records:\nTotal Diagnoses: {stats['total_diagnoses']}\n"
        text += f"Most Common: {stats['most_common']}\n\n"
        text += f"Database Size: {stats['database_size']} bytes\nLocation: {self.database.db_path}\n\nAll data permanently saved!"
        self.update_results(text)
    
    def update_results(self, text):
        """Update results display"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Health Assistant...")
    try:
        HealthAssistant().run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
