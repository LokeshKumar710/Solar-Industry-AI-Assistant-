import streamlit as st
import requests
import json
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file (optional, for local development)
load_dotenv()

# --- Configuration ---
OPENROUTER_API_KEY_ENV = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_NAME = "openai/gpt-4o-mini" #  <-- ### UPDATE THIS WITH A VALID VISION MODEL ###

# --- Helper Functions ---

def get_image_base64(image_bytes):
    """Converts image bytes to base64 string."""
    return base64.b64encode(image_bytes).decode('utf-8')

def get_llm_analysis_prompt():
    return """
    Analyze the provided rooftop image. Your goal is to assess its solar potential.
    Provide your analysis in a structured JSON format with the following keys:
    - "overall_suitability": A rating ('High', 'Medium', 'Low', 'Not Suitable', 'Unknown').
    - "roof_planes": A list of objects, where each object represents a distinct usable roof plane and has:
        - "id": A unique identifier (e.g., "plane_1").
        - "estimated_area_sqm": Approximate area in square meters (number).
        - "orientation": Estimated cardinal direction (e.g., "South", "South-West", "West", "Unknown").
        - "shading_level": Estimated shading ('None', 'Low', 'Moderate', 'High', 'Unknown').
        - "obstructions": A list of strings describing obstructions (e.g., ["chimney", "vent pipe"], or [] if none).
    - "total_estimated_usable_area_sqm": Sum of 'estimated_area_sqm' from suitable 'roof_planes' (number).
    - "dominant_orientation": The orientation with the largest usable area ('South', 'South-West', etc., or 'Unknown').
    - "estimated_pitch_degrees": Approximate roof pitch in degrees (e.g., 20, 30, 0 for flat, 'Unknown').
    - "roof_material_guess": A guess of the roof material (e.g., "Asphalt Shingle", "Tile", "Metal", "Flat Membrane", "Unknown").
    - "general_comments": Any other relevant observations (e.g., "Complex roof geometry", "Large trees nearby to the west").

    Guidelines:
    - If you cannot determine some information, use "Unknown" for strings or null/0 for numbers where appropriate.
    - Assume a standard residential solar panel is about 1.7m x 1m (1.7 sqm). Use this to help gauge areas.
    - Focus only on the primary building in the image if multiple are present, or the largest roof structure.
    - Be conservative with area estimates if the image quality is poor or parts of the roof are obscured.
    - Prioritize south-facing (in the northern hemisphere) or north-facing (in the southern hemisphere) planes if not specified, but analyze all visible planes.
    - "total_estimated_usable_area_sqm" should only include areas from planes deemed reasonably suitable (e.g., not heavily shaded, not facing directly away from the optimal direction unless it's a large flat roof).
    """

def analyze_rooftop_with_llm(image_data_or_url, api_key, is_url=False):
    """
    Sends image (and prompt) to OpenRouter vision LLM and gets analysis.
    """
    if not api_key:
        st.error("OpenRouter API Key is missing. Please provide it in the sidebar.")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    content_parts = [{"type": "text", "text": get_llm_analysis_prompt()}]

    if is_url:
        if not image_data_or_url.startswith(('http://', 'https://')):
             st.error("Invalid image URL provided. Must start with http:// or https://")
             return None
        content_parts.append({
            "type": "image_url",
            "image_url": {
                "url": image_data_or_url
            }
        })
    else: # It's image bytes
        # Determine image format (e.g., jpeg, png)
        try:
            img = Image.open(io.BytesIO(image_data_or_url))
            if img.format.lower() not in ['jpeg', 'png', 'gif', 'webp']: # Common supported formats
                 st.warning(f"Image format {img.format} might not be optimally supported. Trying anyway.")
            image_base64 = get_image_base64(image_data_or_url)
            mime_type = f"image/{img.format.lower() if img.format else 'jpeg'}" # Default to jpeg if format unknown
            content_parts.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            })
        except Exception as e:
            st.error(f"Error processing uploaded image: {e}")
            return None

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": content_parts
            }
        ],
        "max_tokens": 1500 # Adjust as needed for JSON output size
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=90) # Increased timeout
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error: {e}")
        if e.response is not None:
            st.error(f"Response content: {e.response.text}")
        return None
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from API.")
        st.error(f"Raw response: {response.text}")
        return None

def parse_llm_response_content(api_response):
    """Parses the JSON string from the LLM response content."""
    try:
        if api_response and "choices" in api_response and len(api_response["choices"]) > 0:
            content_str = api_response["choices"][0]["message"]["content"]
            # The LLM might return JSON within a ```json ... ``` block
            if "```json" in content_str:
                content_str = content_str.split("```json")[1].split("```")[0].strip()
            elif "```" in content_str and content_str.startswith("{") == False: # Sometimes it just uses ``` without json
                 content_str = content_str.split("```")[1].strip()


            parsed_json = json.loads(content_str)
            return parsed_json
        else:
            st.error("Invalid or empty API response structure.")
            st.json(api_response) # Show what was received
            return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON from LLM response: {e}")
        st.text("LLM Raw Content:")
        st.code(api_response["choices"][0]["message"]["content"] if api_response and "choices" in api_response and len(api_response["choices"]) > 0 else "No content found")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during LLM response parsing: {e}")
        st.json(api_response)
        return None


# --- Placeholder Calculation Functions (YOU NEED TO IMPLEMENT THESE) ---

def calculate_solar_potential(llm_analysis):
    """
    Calculates solar system potential based on LLM analysis.
    Returns a dictionary with:
        - estimated_dc_capacity_kw (float)
        - estimated_annual_production_kwh (float)
        - notes (list of strings)
    """
    if not llm_analysis or "total_estimated_usable_area_sqm" not in llm_analysis:
        return {
            "estimated_dc_capacity_kw": 0,
            "estimated_annual_production_kwh": 0,
            "notes": ["LLM analysis incomplete or missing usable area."]
        }

    usable_area = llm_analysis.get("total_estimated_usable_area_sqm", 0)
    if usable_area is None or not isinstance(usable_area, (int, float)): usable_area = 0


    # Assumptions (make these clear and configurable if possible)
    PANEL_AREA_SQM = 1.7  # Average panel area
    PANEL_PEAK_POWER_W = 400  # Average panel wattage
    SYSTEM_EFFICIENCY_DERATE = 0.85 # Accounts for inverter, wiring, dirt, temperature losses etc.
    # Simplified Peak Sun Hours (PSH) - this is highly location-dependent!
    # For a real tool, this should come from a database or API (e.g., PVWatts) based on location.
    AVG_PEAK_SUN_HOURS_PER_DAY = 4.5 # A very rough average for many US locations

    notes = [
        f"Assuming average panel size: {PANEL_AREA_SQM} sqm",
        f"Assuming average panel power: {PANEL_PEAK_POWER_W} Wp",
        f"Assuming overall system derate factor: {SYSTEM_EFFICIENCY_DERATE*100}%",
        f"Assuming average peak sun hours per day: {AVG_PEAK_SUN_HOURS_PER_DAY} (Location specific data needed for accuracy)"
    ]

    if usable_area <= 0:
        return {
            "estimated_dc_capacity_kw": 0,
            "estimated_annual_production_kwh": 0,
            "notes": notes + ["No usable solar area identified."]
        }

    num_panels = int(usable_area / PANEL_AREA_SQM)
    estimated_dc_capacity_kw = (num_panels * PANEL_PEAK_POWER_W) / 1000

    # Simplified annual production: DC Capacity * PSH * 365 days * System Efficiency
    estimated_annual_production_kwh = estimated_dc_capacity_kw * AVG_PEAK_SUN_HOURS_PER_DAY * 365 * SYSTEM_EFFICIENCY_DERATE

    return {
        "estimated_dc_capacity_kw": round(estimated_dc_capacity_kw, 2),
        "num_panels": num_panels,
        "estimated_annual_production_kwh": round(estimated_annual_production_kwh, 0),
        "notes": notes
    }

def estimate_roi(solar_potential_data, avg_monthly_bill_usd):
    """
    Estimates ROI based on solar potential and electricity bill.
    Returns a dictionary with:
        - estimated_system_cost_usd (float)
        - estimated_annual_savings_usd (float)
        - simple_payback_years (float or "N/A")
        - notes (list of strings)
    """
    if not solar_potential_data or solar_potential_data["estimated_dc_capacity_kw"] == 0:
        return {
            "estimated_system_cost_usd": 0,
            "estimated_annual_savings_usd": 0,
            "simple_payback_years": "N/A",
            "notes": ["Cannot calculate ROI without estimated system capacity."]
        }

    # Assumptions
    COST_PER_WATT_USD = 2.8 # National average, can vary widely
    AVG_ELECTRICITY_PRICE_PER_KWH_USD = 0.15 # National average, should ideally be user input or localized
    FEDERAL_TAX_CREDIT_PERCENT = 0.30 # Current ITC, can change

    notes = [
        f"Assuming installed cost per Watt: ${COST_PER_WATT_USD:.2f}/Wp (DC)",
        f"Using average electricity price: ${AVG_ELECTRICITY_PRICE_PER_KWH_USD:.2f}/kWh for savings calculation (can be inaccurate, use local rates)",
        f"Assuming Federal Tax Credit (ITC): {FEDERAL_TAX_CREDIT_PERCENT*100}% applies to system cost"
    ]

    system_capacity_kw = solar_potential_data["estimated_dc_capacity_kw"]
    annual_production_kwh = solar_potential_data["estimated_annual_production_kwh"]

    gross_system_cost_usd = system_capacity_kw * 1000 * COST_PER_WATT_USD
    net_system_cost_usd = gross_system_cost_usd * (1 - FEDERAL_TAX_CREDIT_PERCENT)

    # Savings can be complex (e.g., net metering, time-of-use rates)
    # Simple approach: value of energy produced at average rate
    # More advanced: % of bill offset. If production > consumption, value of export credit?
    # For now, let's estimate savings by offsetting the bill, capped by annual bill
    annual_bill_usd = avg_monthly_bill_usd * 12
    estimated_annual_savings_usd = min(annual_production_kwh * AVG_ELECTRICITY_PRICE_PER_KWH_USD, annual_bill_usd)
    notes.append(f"Estimated annual savings are capped by your annual electricity bill of ${annual_bill_usd:,.0f}.")


    simple_payback_years = "N/A"
    if estimated_annual_savings_usd > 0:
        simple_payback_years = round(net_system_cost_usd / estimated_annual_savings_usd, 1)

    return {
        "gross_system_cost_usd": round(gross_system_cost_usd, 0),
        "net_system_cost_after_itc_usd": round(net_system_cost_usd, 0),
        "estimated_annual_savings_usd": round(estimated_annual_savings_usd, 0),
        "simple_payback_years": simple_payback_years,
        "notes": notes
    }

def generate_recommendations(llm_analysis, solar_potential):
    """
    Generates installation recommendations.
    Returns a list of strings.
    """
    recs = []
    if not llm_analysis or not solar_potential:
        return ["Awaiting analysis results."]

    suitability = llm_analysis.get("overall_suitability", "Unknown").lower()
    if suitability == "high":
        recs.append("✅ Rooftop appears highly suitable for solar installation.")
    elif suitability == "medium":
        recs.append("⚠️ Rooftop appears moderately suitable. Some factors might need closer inspection.")
    elif suitability == "low":
        recs.append("❌ Rooftop appears to have low suitability. Significant challenges may exist.")
    elif suitability == "not suitable":
        recs.append("⛔ Rooftop does not appear suitable for solar installation based on the image.")
    else:
        recs.append("ℹ️ Solar suitability assessment from image is unclear or pending.")

    if solar_potential.get("estimated_dc_capacity_kw", 0) > 0:
        recs.append(f"Estimated system size: {solar_potential['estimated_dc_capacity_kw']:.2f} kW DC, potentially using around {solar_potential.get('num_panels', 'N/A')} panels.")
    else:
        recs.append("No viable system size could be estimated from the usable area.")

    orientation = llm_analysis.get("dominant_orientation", "Unknown")
    if orientation != "Unknown":
        recs.append(f"Dominant usable roof orientation appears to be: {orientation}.")
    else:
        recs.append("Roof orientation information is important; aim for south-facing in Northern Hemisphere (or north-facing in Southern Hemisphere).")

    total_usable_area = llm_analysis.get("total_estimated_usable_area_sqm", 0)
    if total_usable_area is None: total_usable_area = 0
    recs.append(f"Total estimated usable roof area for solar: {total_usable_area:.1f} sqm.")


    # Check for specific obstructions or shading
    shading_notes = []
    obstruction_notes = []
    if "roof_planes" in llm_analysis and llm_analysis["roof_planes"]:
        for plane in llm_analysis["roof_planes"]:
            if plane.get("shading_level", "Unknown").lower() in ["moderate", "high"]:
                shading_notes.append(f"Plane {plane.get('id','N/A')} shows {plane.get('shading_level','N/A')} shading.")
            if plane.get("obstructions") and len(plane.get("obstructions")) > 0 :
                obstruction_notes.append(f"Plane {plane.get('id','N/A')} has obstructions: {', '.join(plane.get('obstructions'))}.")

    if shading_notes:
        recs.append(f"Shading concerns: {'; '.join(shading_notes)}. A detailed on-site shade analysis is crucial.")
    if obstruction_notes:
        recs.append(f"Obstructions noted: {'; '.join(obstruction_notes)}. These may reduce usable area or require careful panel placement.")


    recs.append("Consider using high-efficiency monocrystalline panels for best performance in limited space.")
    recs.append("Obtain multiple quotes from certified local solar installers.")
    recs.append("Verify local net metering policies, permitting requirements, and available incentives.")
    recs.append("A professional on-site survey is essential before making any decisions.")

    return recs

# --- Streamlit App UI ---
st.set_page_config(layout="wide", page_title="Solar Rooftop AI Analyzer")
st.title("☀️ AI-Powered Rooftop Solar Analysis Tool")
st.markdown("Assess solar installation potential using satellite imagery.")

# --- Sidebar for API Key and Controls ---
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input("Enter OpenRouter API Key", type="password", value=OPENROUTER_API_KEY_ENV or "", help="Get your key from openrouter.ai")

st.sidebar.markdown("---")
st.sidebar.subheader("Image Input")
image_source_option = st.sidebar.radio("Choose image source:", ("Upload Image", "Image URL"))

uploaded_file = None
image_url = ""

if image_source_option == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Upload a satellite image of a rooftop", type=["jpg", "jpeg", "png", "webp"])
else:
    image_url = st.sidebar.text_input("Enter Image URL (e.g., from Google Maps)", placeholder="https://maps.googleapis.com/...")

avg_monthly_bill = st.sidebar.number_input("Average Monthly Electricity Bill (USD)", min_value=0.0, value=150.0, step=10.0)

analyze_button = st.sidebar.button("Analyze Rooftop", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown(f"Using LLM: `{MODEL_NAME}` via OpenRouter.")
st.sidebar.caption("Note: AI analysis provides estimates. Always consult a professional.")


# --- Main Panel for Results ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rooftop Image")
    if uploaded_file:
        try:
            image_bytes = uploaded_file.getvalue()
            st.image(image_bytes, caption="Uploaded Rooftop Image", use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying uploaded image: {e}")
    elif image_url:
        try:
            # Basic validation for common image extensions in URL, though server response matters more
            if any(ext in image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                st.image(image_url, caption="Rooftop Image from URL", use_container_width=True)
            else:
                st.warning("URL may not point to a direct image. If analysis fails, try a direct image link.")
                # We will still try to use it. The LLM might handle some indirect links or fail gracefully.
        except Exception as e:
            st.error(f"Error displaying image from URL: {e}. Make sure it's a direct link to an image.")
    else:
        st.info("Upload an image or provide an image URL in the sidebar to begin.")

# Initialize session state for results
if "llm_analysis" not in st.session_state:
    st.session_state.llm_analysis = None
if "solar_potential" not in st.session_state:
    st.session_state.solar_potential = None
if "roi_estimate" not in st.session_state:
    st.session_state.roi_estimate = None
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "raw_llm_response" not in st.session_state:
    st.session_state.raw_llm_response = None


if analyze_button:
    st.session_state.llm_analysis = None # Reset previous results
    st.session_state.solar_potential = None
    st.session_state.roi_estimate = None
    st.session_state.recommendations = None
    st.session_state.raw_llm_response = None

    current_api_key = api_key_input or OPENROUTER_API_KEY_ENV
    if not current_api_key:
        st.error("🚨 OpenRouter API Key is required. Please enter it in the sidebar.")
    elif not (uploaded_file or image_url):
        st.warning("👈 Please upload an image or provide an image URL.")
    else:
        with st.spinner("🧠 Analyzing rooftop with AI... This may take a minute..."):
            image_to_process = None
            is_url_input = False
            if uploaded_file:
                image_to_process = uploaded_file.getvalue()
                is_url_input = False
            elif image_url:
                image_to_process = image_url
                is_url_input = True

            if image_to_process:
                raw_response = analyze_rooftop_with_llm(image_to_process, current_api_key, is_url=is_url_input)
                st.session_state.raw_llm_response = raw_response # Store for debugging

                if raw_response:
                    llm_json_output = parse_llm_response_content(raw_response)
                    if llm_json_output:
                        st.session_state.llm_analysis = llm_json_output
                        st.session_state.solar_potential = calculate_solar_potential(st.session_state.llm_analysis)
                        st.session_state.roi_estimate = estimate_roi(st.session_state.solar_potential, avg_monthly_bill)
                        st.session_state.recommendations = generate_recommendations(st.session_state.llm_analysis, st.session_state.solar_potential)
                        st.success("✅ Analysis Complete!")
                    else:
                        st.error("Failed to parse valid JSON from LLM response.")
                else:
                    st.error("Failed to get a response from the LLM API.")
            else: # Should not happen due to earlier check, but as a safeguard
                st.error("No image data found to process.")


with col2:
    st.subheader("Analysis Results")
    if st.session_state.llm_analysis:
        st.markdown("#### AI Vision Analysis (Extracted Data)")
        st.json(st.session_state.llm_analysis) # Display the parsed JSON from LLM

        st.markdown("---")
        st.markdown("#### Solar Potential Assessment")
        if st.session_state.solar_potential:
            sp = st.session_state.solar_potential
            st.write(f"**Estimated DC System Capacity:** {sp['estimated_dc_capacity_kw']:.2f} kW")
            st.write(f"**Estimated Number of Panels:** {sp.get('num_panels', 'N/A')}")
            st.write(f"**Estimated Annual Energy Production:** {sp['estimated_annual_production_kwh']:,.0f} kWh")
            with st.expander("Calculation Notes & Assumptions (Solar Potential)"):
                for note in sp['notes']:
                    st.caption(note)
        else:
            st.warning("Could not calculate solar potential.")

        st.markdown("---")
        st.markdown("#### Return on Investment (ROI) Estimate")
        if st.session_state.roi_estimate:
            roi = st.session_state.roi_estimate
            st.write(f"**Estimated Gross System Cost:** ${roi['gross_system_cost_usd']:,.0f} USD")
            st.write(f"**Estimated Net System Cost (after 30% ITC):** ${roi['net_system_cost_after_itc_usd']:,.0f} USD")
            st.write(f"**Estimated Annual Savings:** ${roi['estimated_annual_savings_usd']:,.0f} USD")
            st.write(f"**Simple Payback Period:** {roi['simple_payback_years']} years")
            with st.expander("Calculation Notes & Assumptions (ROI)"):
                for note in roi['notes']:
                    st.caption(note)
        else:
            st.warning("Could not estimate ROI.")

        st.markdown("---")
        st.markdown("#### Installation & Next Step Recommendations")
        if st.session_state.recommendations:
            for rec in st.session_state.recommendations:
                st.markdown(f"- {rec}")
        else:
            st.warning("No recommendations generated.")

    elif analyze_button: # If button was clicked but no results (error occurred)
        st.info("Analysis attempted. Check for error messages above or in the sidebar.")
    else: # Initial state
        st.info("Results will appear here after analysis.")

# Optional: Display raw LLM response for debugging
if st.session_state.raw_llm_response:
    with st.expander(" görmek Raw LLM API Response (for debugging)"): # "görmek" means "see" in Turkish, often used for expanders
        st.json(st.session_state.raw_llm_response)

st.markdown("---")
st.caption("Disclaimer: This tool provides automated estimates based on AI analysis of satellite imagery. Accuracy is not guaranteed. All information should be verified by qualified solar professionals through an on-site assessment before making any financial or installation decisions.")