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
*   **Core LLM (Vision):** `<<FILL_THIS_IN_-_e.g., liuhaotian/llava-v1.6-vicuna-13b>>`
*   **Key Python Libraries:** `requests`, `Pillow`, `python-dotenv`

## Live Demo

🚀 You can try out the live application here: **`<<FILL_THIS_IN_-_Link_to_your_deployed_Hugging_Face_Space_or_Streamlit_Cloud_App_OR_State_Not_Available>>`**
*(Example if not deployed: "A live deployment is not currently available. Please follow the setup instructions below to run locally.")*

## Project Setup Instructions (Setup Guide)

### Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)
*   Git

### 1. Clone the Repository

```bash
git clone https://github.com/<<FILL_THIS_IN_-_YourGitHubUsername>>/<<FILL_THIS_IN_-_YourRepositoryName>>.git
cd <<FILL_THIS_IN_-_YourRepositoryName>>

