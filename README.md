# Virtual Health Assistant

A simple, modular Virtual Health Assistant application built with Python and Tkinter.

## Features

- **Symptom Selection**: Choose from 50 diverse symptoms
- **AI Diagnosis**: Machine learning-based diagnosis using Decision Tree (scikit-learn)
- **Persistent Storage**: SQLite database for diagnosis history
- **Health Tips**: Browser-based health tips display
- **Database Statistics**: Track your health history and usage stats

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/VirtualHealthAssistant.git
   cd VirtualHealthAssistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python health_assistant.py
   ```

## Usage

1. **Report Symptoms**: Click "Report Symptoms" and select from 50 available symptoms
2. **Get Diagnosis**: Click "Get Diagnosis" for AI-powered analysis
3. **View History**: See your previous diagnoses and track patterns
4. **Health Tips**: Get general health advice displayed in your browser
5. **Database Stats**: View usage statistics and database information

## Project Structure

```
VirtualHealthAssistant/
├── health_assistant.py      # Main application file
├── symptom_checker.py       # Symptom validation and management
├── diagnostic_engine.py     # AI diagnosis using scikit-learn
├── health_tips.py          # Health tips and browser display
├── database.py             # SQLite database operations
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Dependencies

- **tkinter**: GUI framework (included with Python)
- **scikit-learn**: Machine learning library for diagnosis
- **numpy**: Numerical computing (required by scikit-learn)
- **sqlite3**: Database (included with Python)

## Medical Conditions Supported

The AI can diagnose 17 different conditions including:
- Common Cold, Flu, Pneumonia
- Gastroenteritis, Migraine, Allergic Reaction
- UTI, Arthritis, Anxiety Disorder
- Depression, Diabetes, Hypertension
- Hypotension, Anemia, Heart Disease
- Acid Reflux, Insomnia

## Data Storage

- All diagnoses are stored locally in SQLite database
- History includes symptoms, diagnosis, confidence levels, and timestamps
- Database statistics track usage patterns

## Disclaimer

⚠️ **IMPORTANT**: This application is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

Created by 192411263.simats@saveetha.com - Saveetha Engineering College

## Acknowledgments

- Built with Python and Tkinter
- Machine learning powered by scikit-learn
- Inspired by the need for accessible health information tools
