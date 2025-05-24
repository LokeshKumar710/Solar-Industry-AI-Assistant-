# AI-Powered Rooftop Solar Analysis Tool

## Overview

This project is an AI-powered rooftop analysis tool designed to assess solar installation potential using satellite imagery. It aims to provide homeowners and solar professionals with quick, data-driven insights, including solar potential assessments, installation recommendations, and preliminary ROI estimates. The system leverages a Vision Large Language Model (LLM) for image analysis and custom logic for solar-specific calculations.

**This project was developed as part of the Solar Industry AI Assistant Internship Assessment.**

## Features

*   **Satellite Image Analysis:** Analyzes user-provided satellite images of rooftops.
*   **Rooftop Characteristics Extraction:** Identifies usable roof planes, estimates area, orientation, potential shading, and obstructions using AI.
*   **Solar Potential Assessment:** Calculates estimated solar system size (kW) and annual energy production (kWh).
*   **Installation Recommendations:** Provides general guidance on system sizing and next steps.
*   **ROI Estimation:** Offers a preliminary Return on Investment estimate based on system cost, assumed incentives, and user-provided electricity bill information.
*   **User-Friendly Web Interface:** Built with Streamlit for easy interaction.

## Technology Stack

*   **Backend:** Python
*   **Web Interface:** Streamlit
*   **AI Integration:** OpenRouter API
*   **Core LLM (Vision):** `openai/gpt-4o-mini`
*   **Key Python Libraries:** `requests`, `Pillow`, `python-dotenv`


## Project Setup Instructions (Setup Guide)

### Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)
*   Git


### 1. Clone the Repository

```bash
git clone https://github.com/LokeshKumar710/Solar-Industry-AI-Assistant-

```
### 2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

On Windows (Git Bash or PowerShell):
``` bash
python -m venv solar_venv
.\solar_venv\Scripts\activate
```
### 3. Install Dependencies
Install the required Python packages using the requirements.txt file:
```
pip install -r requirements.txt
```


## 🔐 4. Set Up OpenRouter API Key

This application requires an API key from [OpenRouter.ai](https://openrouter.ai) to access the LLM for image analysis.

### 📝 Steps to Obtain an API Key:

1. **Sign up / Log in** to [OpenRouter.ai](https://openrouter.ai).
2. Go to your **account dashboard** and navigate to the **"Keys"** section.
3. **Create a new API key**. Give it a descriptive name (e.g., `SolarAnalysisProject`).
4. **Copy** the generated API key.

---

### 🔧 Ways to Provide the API Key:

#### ✅ Option A (Recommended for Local Development - `.env` file)

1. In the **project root directory**, create a file named `.env`.
2. Add your API key to the file in the following format:

   ```env
   OPENROUTER_API_KEY=your_api_key_here

```
OPENROUTER_API_KEY="your_actual_openrouter_api_key_here"
```

(The .env file is included in .gitignore and will not be committed to GitHub).
Option B (Manual Input in UI):
You can also enter the API key directly into the designated field in the application's sidebar when you run it.
### 5. Running the Application
Once the setup is complete, you can run the Streamlit application:
```streamlit run app.py```


This will typically open the application in your default web browser. If not, the terminal will display a local URL (e.g., http://localhost:8501) that you can navigate to.

# Solar-Industry-AI-Assistant ☀️🏠

This tool uses AI to analyze rooftop satellite imagery to assess solar panel installation potential and provide return on investment (ROI) estimates.

---

## 🚀 Example Usage

### 🔑 Provide API Key
Enter your OpenRouter API key in the sidebar (or load it from a `.env` file).

### 🖼️ Input Rooftop Image
- **Upload Image**: Select a satellite image file (e.g., `.jpg`, `.png`) from your device.
- **Image URL**: Paste a direct URL link to a satellite image.

### 💡 Enter Electricity Bill
Input your **average monthly electricity bill (in USD)** in the sidebar.  
This value is used to calculate potential savings and ROI.

### 🧠 Click "Analyze Rooftop"
The app will:
- Send the image for AI analysis.
- Process solar feasibility.
- Estimate system specs and savings.

> **Note**: Analysis may take a few moments depending on image size and server response.

---

## 📊 Review Results

After analysis, you'll see:
- **Input Image** preview.
- **AI Vision Analysis**: Extracted data in JSON format.
- **Solar Potential Assessment**: System size, estimated energy production.
- **ROI Estimate**: System cost, savings over time, and payback period.
- **Installation Recommendations**: Suggestions and next steps.

---

## 📚 Project Documentation

For deeper insights into this project:

- [`IMPLEMENTATION_DETAILS.md`](IMPLEMENTATION_DETAILS.md): Explains AI integration, logic, and assumptions.
- [`EXAMPLE_USE_CASES.md`](EXAMPLE_USE_CASES.md): Sample scenarios and how to interpret the outputs.
- [`FUTURE_IMPROVEMENTS.md`](FUTURE_IMPROVEMENTS.md): Ideas for enhancing the tool further.

---


