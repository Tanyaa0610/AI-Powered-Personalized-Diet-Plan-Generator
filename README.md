# AI-Powered Personalized Diet Planning System

## Overview

The AI-Powered Personalized Diet Planning System is an intelligent healthcare application designed to generate personalized dietary recommendations based on an individual's health condition, body metrics, nutritional deficiencies, allergies, and fitness objectives. The system integrates Artificial Intelligence (AI), Machine Learning (ML), Retrieval-Augmented Generation (RAG), and a Multi-Agent Architecture to provide accurate, explainable, and user-centric diet plans.

The primary objective of this project is to overcome the limitations of conventional diet recommendation systems, which often provide generic suggestions without considering an individual's unique health profile. By combining data-driven analysis with AI-powered reasoning, the system delivers tailored nutritional guidance and automated health reports.

---

## Key Features

- Personalized diet recommendations based on disease conditions
- BMI-based nutritional planning
- Goal-oriented diet generation (weight loss, weight gain, maintenance)
- Nutritional deficiency-aware recommendations
- Allergy and food restriction filtering
- Machine Learning-based text classification using TF-IDF and Logistic Regression
- Retrieval-Augmented Generation (RAG) for enhanced dietary knowledge retrieval
- OpenAI-powered food explanations and recommendations
- Nutritional analysis and health score generation
- Automated PDF and JSON report generation
- Interactive Streamlit-based user interface

---

## System Architecture

The proposed system follows a modular Multi-Agent Architecture, where each agent is responsible for a specific task within the recommendation pipeline.

```text
User Input
      ↓
Validator Agent
      ↓
ML Classifier Agent
      ↓
Research Agent (RAG)
      ↓
Nutritionist Agent
      ↓
Analyzer Agent
      ↓
Allergen Filter Agent
      ↓
Aggregator Agent
      ↓
Output Generation (PDF / JSON)
```

---

## Multi-Agent Workflow

### Validator Agent
- Validates and structures user inputs
- Performs data cleaning and preprocessing
- Calculates Body Mass Index (BMI)

### ML Classifier Agent
- Processes textual inputs
- Utilizes TF-IDF Vectorization and Logistic Regression
- Supports intelligent disease-related classification

### Research Agent
- Retrieves disease-specific dietary information
- Integrates structured datasets and external knowledge sources
- Implements Retrieval-Augmented Generation (RAG)

### Nutritionist Agent
- Generates personalized meal plans
- Considers disease conditions, BMI, deficiencies, and user goals

### Analyzer Agent
- Calculates:
  - Basal Metabolic Rate (BMR)
  - Total Daily Energy Expenditure (TDEE)
  - Daily calorie requirements
  - Macronutrient distribution

### Allergen Filter Agent
- Identifies and removes allergenic food items
- Suggests suitable alternatives

### Aggregator Agent
- Combines outputs from all agents
- Produces the final structured recommendation

### Output Agent
- Generates downloadable PDF reports
- Stores results in JSON format

---

## Retrieval-Augmented Generation (RAG)

The system employs a lightweight Retrieval-Augmented Generation framework to enhance the quality and relevance of dietary recommendations.

```text
User Query
      ↓
Knowledge Retrieval
(JSON Dataset / API Sources)
      ↓
Context Augmentation
      ↓
OpenAI Language Model
      ↓
Personalized Diet Recommendation
```

The retrieval layer ensures that generated recommendations are grounded in structured nutritional knowledge while maintaining flexibility through AI-driven personalization.

---

## Machine Learning Pipeline

```text
Input Text
      ↓
Text Preprocessing
      ↓
TF-IDF Vectorization
      ↓
Logistic Regression
      ↓
Predicted Output
```

The Machine Learning module converts textual input into numerical representations and supports disease-related classification tasks.

---

## Nutritional Analysis

The system performs comprehensive nutritional analysis using established health formulas.

### Body Mass Index (BMI)

```text
BMI = Weight (kg) / Height² (m²)
```

### Basal Metabolic Rate (BMR)

```text
BMR = 10 × Weight + 6.25 × Height − 5 × Age + 5
```

### Total Daily Energy Expenditure (TDEE)

```text
TDEE = BMR × Activity Factor
```

### Macronutrient Distribution

| Nutrient | Allocation |
|-----------|-----------|
| Protein | 25% |
| Carbohydrates | 50% |
| Fat | 25% |

---

## Generated Outputs

The system automatically generates:

- Personalized diet plans
- Disease-specific food recommendations
- Foods to avoid
- Meal-wise nutritional guidance
- Calorie and macronutrient analysis
- Health score assessment
- Macronutrient distribution charts
- Meal calorie distribution visualizations
- AI-generated food explanations
- Downloadable PDF reports
- Structured JSON outputs

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| User Interface | Streamlit |
| Machine Learning | Scikit-Learn |
| AI/LLM Integration | OpenAI GPT-4o-mini |
| Visualization | Matplotlib |
| Report Generation | ReportLab |
| Data Storage | JSON |
| Environment Management | Python Dotenv |

---

## Project Structure

```bash
Diet-Plan-Generator/
│
├── agents/
│   ├── validator.py
│   ├── researcher.py
│   ├── nutritionist.py
│   ├── analyzer.py
│   ├── allergen.py
│   ├── aggregator.py
│   ├── json_validator.py
│   └── file_generator.py
│
├── data/
│   └── diseases.json
│
├── outputs/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/Tanyaa0610/AI-Powered-Personalized-Diet-Plan-Generator.git
cd AI-Diet-Planner
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## Running the Application

### Streamlit Interface

```bash
streamlit run app.py
```

### Command-Line Execution

```bash
python main.py
```

---

## Future Scope

- Integration with wearable health monitoring devices
- Mobile application development
- Advanced disease prediction models
- Semantic retrieval using vector databases
- Real-time health tracking and monitoring
- Multilingual support
- Clinical validation with healthcare professionals


---

## License

This project has been developed for academic, research, and educational purposes.
