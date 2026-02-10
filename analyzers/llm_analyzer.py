import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: OPENAI_API_KEY not found. LLM analysis will be skipped.")

    def analyze_anomaly(self, transaction_data, detections):
        """
        Uses LLM (OpenAI GPT-4.1 Nano) to analyze the context of a flagged transaction.
        """
        if not self.client:
            return {
                "risk_assessment": "LLM analysis skipped (no API key)",
                "context_analysis": "N/A",
                "risk_score_modifier": 0,
                "suggested_action": "Configure OpenAI API key"
            }

        prompt = f"""
        Analyze the following accounting transaction for potential risk or anomaly context.
        
        Transaction Data:
        {json.dumps(transaction_data, indent=2)}
        
        System Detections:
        {json.dumps(detections, indent=2)}
        
        Provide your assessment in the following JSON format:
        {{
            "risk_assessment": "Short summary of the risk (Low, Medium, High, Critical)",
            "context_analysis": "Detailed explanation of why this might or might not be a problem",
            "risk_score_modifier": <float between -0.5 and 0.5 where positive increases risk>,
            "suggested_action": "Recommended next step for a human reviewer"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert forensic accountant and data auditor."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-4.1-nano-2025-04-14",
                response_format={"type": "json_object"}
            )
            
            response_content = response.choices[0].message.content
            return json.loads(response_content)
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {
                "risk_assessment": "Error",
                "context_analysis": f"Failed to call OpenAI: {str(e)}",
                "risk_score_modifier": 0,
                "suggested_action": "Review manually"
            }
