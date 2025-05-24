This file provides deeper insights into how the project was built.
Content to include:
AI Implementation:
LLM Integration: Specify the LLM model used (e.g., liuhaotian/llava-v1.6-vicuna-13b) and the rationale for its selection. Briefly describe the use of the OpenRouter API.
Prompt Engineering: Include the final core prompt for image analysis. Explain key instructions within the prompt and any significant challenges or iterations during its design.
Context Management: Describe how image data and other inputs are passed to the LLM.
Response Accuracy/Validation: Explain how the LLM's JSON response is parsed, validated, and how errors are handled.
Development Choices & Logic:
Implementation Choice: Justify the choice of Streamlit for the web interface.
Code Structure: Briefly outline the main components of app.py.
Key Calculation Logic: Detail the formulas and critical assumptions for:
Solar Panel Capacity.
Annual Energy Production.
System Cost.
ROI (including how savings are calculated and any caps).
Clearly list all major assumptions (e.g., panel efficiency, PSH, cost/W, ITC rate).
Error Handling: Briefly describe the types of errors the application handles.
Limitations: Acknowledge known limitations, such as the approximate nature of AI visual estimations, simplified ROI calculations, and dependency on image quality