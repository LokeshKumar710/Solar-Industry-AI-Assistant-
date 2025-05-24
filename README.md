# MASTER DOCUMENTATION OUTLINE: AI-Powered Rooftop Solar Analysis Tool

---
## SECTION 1: PROJECT OVERVIEW & SETUP (Primarily for README.md)
---

### 1.1. Project Title
    AI-Powered Rooftop Solar Analysis Tool

### 1.2. General Overview
    - Brief 1-2 paragraph description: Purpose (assess solar potential from satellite imagery), target users (homeowners, solar professionals), key outputs (potential, recommendations, ROI).
    - Mention its context: "Developed as part of the Solar Industry AI Assistant Internship Assessment."

### 1.3. Features
    - Bullet list:
        - Satellite Image Analysis (user-provided images)
        - Rooftop Characteristics Extraction (AI-driven: area, orientation, shading, obstructions)
        - Solar Potential Assessment (system size kW, annual energy kWh)
        - Installation Recommendations (general guidance)
        - ROI Estimation (preliminary, based on inputs)
        - User-Friendly Web Interface (Streamlit)

### 1.4. Technology Stack
    - Backend: Python
    - Web Interface: Streamlit
    - AI Integration: OpenRouter API
    - Core LLM (Vision): `<<Specify LLM model used, e.g., liuhaotian/llava-v1.6-vicuna-13b>>`
    - Key Python Libraries: `requests`, `Pillow`, `python-dotenv`

### 1.5. Live Demo / Access
    - Link: `<<Link to deployed Hugging Face Space/Streamlit Cloud App OR State "Not deployed, run locally">>`

### 1.6. Project Setup Instructions (Setup Guide)
    #### 1.6.1. Prerequisites
        - Python 3.8+
        - `pip`
        - Git
    #### 1.6.2. Cloning the Repository
        - `git clone https://github.com/<<YourGitHubUsername>>/<<YourRepositoryName>>.git`
        - `cd <<YourRepositoryName>>`
    #### 1.6.3. Virtual Environment Setup
        - Instructions for macOS/Linux (`python3 -m venv solar_venv`, `source solar_venv/bin/activate`)
        - Instructions for Windows (`python -m venv solar_venv`, `.\solar_venv\Scripts\activate`)
    #### 1.6.4. Installing Dependencies
        - `pip install -r requirements.txt`
    #### 1.6.5. OpenRouter API Key Setup
        - How to get a key from OpenRouter.ai.
        - Options for providing the key:
            - `.env` file method (recommended for local dev): `OPENROUTER_API_KEY="your_key"`
            - Manual input in the UI sidebar.
    #### 1.6.6. Running the Application
        - `streamlit run app.py`
        - Mention local URL (e.g., `http://localhost:8501`).

---
## SECTION 2: USAGE & EXAMPLES (README.md brief, EXAMPLE_USE_CASES.md detailed)
---

### 2.1. Example Usage (Brief for README.md)
    1. Provide API Key (if not via .env).
    2. Input Rooftop Image (upload or URL).
    3. Enter Average Monthly Electricity Bill.
    4. Click "Analyze Rooftop".
    5. Review displayed results (AI analysis, potential, ROI, recommendations).

### 2.2. Detailed Example Use Cases (For EXAMPLE_USE_CASES.md)
    *(Structure for 2-3 distinct examples)*
    #### Example 1: `<<Scenario Title, e.g., Simple Pitched Residential Roof>>`
        - **Input Image:** (Description or embedded screenshot)
        - **User Inputs:** (e.g., Avg. Monthly Bill: $X)
        - **Key AI Analysis Output (JSON Snippet):** `overall_suitability`, relevant `roof_planes` details, `total_estimated_usable_area_sqm`.
        - **Key Application Results:** Est. DC Capacity, Est. Annual Production, Est. Net Cost, Payback Period, Key Recommendations.
        - **Brief Commentary:** Plausibility of AI assessment for this image, how results reflect inputs.
    #### Example 2: `<<Scenario Title, e.g., Large Flat Commercial Roof>>`
        - (Repeat structure above)
    #### Example 3: `<<Scenario Title, e.g., Roof with Partial Shading>>`
        - (Repeat structure above)

---
## SECTION 3: IMPLEMENTATION DETAILS (For IMPLEMENTATION_DETAILS.md)
---

### 3.1. AI Implementation
    #### 3.1.1. LLM Integration & Vision AI
        - Choice of LLM: `<<Model Name>>` - Rationale (vision capabilities, OpenRouter availability, performance).
        - OpenRouter API Usage: Endpoint (`/v1/chat/completions`), authentication, data format (image as base64/URL).
    #### 3.1.2. Prompt Engineering
        - Final Core Prompt: (Paste the full prompt here).
        - Key Instructions in Prompt: Structured JSON output, identification of specific roof features (area, orientation, shading, obstructions, pitch, material), focus on primary building.
        - Iteration/Challenges: (Briefly mention any significant design choices or difficulties).
    #### 3.1.3. Context Management
        - How image data is passed to the LLM.
        - Handling of other user inputs (e.g., electricity bill used post-LLM analysis).
    #### 3.1.4. Response Accuracy & Validation
        - Parsing LLM's JSON response: `json.loads()`, handling of ```json ... ``` blocks.
        - Error handling for malformed JSON.
        - Confidence Scoring: Implicit (AI's use of "Unknown", qualitative ratings). No explicit confidence score from the model itself.

### 3.2. Development Skills & Choices
    #### 3.2.1. Choice of Implementation (Backend API vs. Web Interface)
        - Streamlit chosen for rapid web interface development, ease of use, and Python integration.
    #### 3.2.2. Code Structure (`app.py`)
        - Main components: UI element definitions (sidebar, input fields, output areas), API call function (`analyze_rooftop_with_llm`), LLM response parsing (`parse_llm_response_content`), calculation functions (`calculate_solar_potential`, `estimate_roi`, `generate_recommendations`).
    #### 3.2.3. Key Calculation Logic & Assumptions
        - **Solar Panel Capacity:**
            - Formula: `(Usable Area / Panel Area) * Panel Wattage`
            - Assumptions: Avg. Panel Area (`<<e.g., 1.7 sqm>>`), Avg. Panel Wattage (`<<e.g., 400 Wp>>`).
        - **Annual Energy Production:**
            - Formula: `Capacity (kW) * Avg. Peak Sun Hours (PSH) * 365 * System Derate Factor`
            - Assumptions: Avg. PSH (`<<e.g., 4.5 hours>>` - stated as location-dependent simplification), System Derate Factor (`<<e.g., 0.85>>` - for losses).
        - **System Cost:**
            - Formula: `Capacity (kW) * 1000 * Cost per Watt`
            - Assumptions: Avg. Cost per Watt (`<<e.g., $2.80/Wp DC>>`).
        - **ROI Estimation:**
            - Net Cost: `Gross Cost * (1 - Federal Tax Credit Percentage)`
            - Assumption: Federal ITC (`<<e.g., 30%>>`).
            - Annual Savings: `min(Annual Energy Production * Avg. Electricity Price, Annual Electricity Bill)`
            - Assumptions: Avg. Electricity Price (`<<e.g., $0.15/kWh>>`), savings capped by annual bill.
            - Payback Period: `Net Cost / Annual Savings`.
    #### 3.2.4. Error Handling
        - Types of errors handled: API request errors (network, auth), JSON parsing errors from LLM response, basic input validation hints.

### 3.3. Limitations
    - Accuracy of LLM's visual estimations (area, orientation, shading, pitch, material is a guess).
    - Simplified ROI calculations (fixed PSH, national average costs, no detailed local tariffs/incentives, capped savings).
    - Dependency on clear, unobstructed satellite imagery.
    - Current model might not perfectly identify all roof types or complex obstructions.
    - No precise geo-location integration for insolation data.

---
## SECTION 4: FUTURE IMPROVEMENTS (For FUTURE_IMPROVEMENTS.md)
---

### 4.1. Enhanced AI & Image Processing
    - Integrate with mapping APIs (Google Maps Static API, Mapbox) to fetch imagery by address.
    - Use precise geo-location (lat/long from address) for accurate solar insolation data (e.g., NREL PVWatts API).
    - Explore dedicated object detection models for more accurate obstruction/dimension identification prior to LLM analysis.
    - Allow users to draw/define roof planes on the image for refinement.
    - Investigate 3D roof modeling capabilities if feasible.

### 4.2. Solar & ROI Calculation Refinements
    - Allow user selection of specific panel models and their efficiencies.
    - More detailed shading analysis (e.g., considering time of year/day – advanced).
    - Database/API for local electricity tariffs, net metering policies, and specific state/local incentives.
    - Advanced ROI metrics (e.g., Net Present Value (NPV), Internal Rate of Return (IRR)).
    - Option to factor in battery storage costs and benefits.

### 4.3. User Experience & Features
    - User accounts to save and manage past analyses.
    - PDF report generation of the analysis.
    - Feature to compare different system configurations or panel choices.
    - Potential integration with solar installer databases or quote request systems.

### 4.4. Technical Enhancements
    - More robust and granular error handling and user feedback.
    - Implementation of unit and integration tests for backend logic.
    - Performance optimization, especially for API calls and image processing.
    - Research methods for improved confidence scoring or self-correction for AI outputs.

---
## SECTION 5: ADMINISTRATIVE (Primarily for README.md)
---

### 5.1. Disclaimer
    - Standard disclaimer: Tool provides estimates, AI accuracy varies, professional on-site assessment is essential before any decisions.

### 5.2. Author
    - `<<Your Name>>`
    - `<<Link to Your GitHub Profile (Optional)>>`
    - `<<Link to Your LinkedIn Profile (Optional)>>`

---
