import openai

class LocalLLMAnalyzer:
    def __init__(self, base_url="http://10.5.0.2:1234/v1", model="deepseek-r1-distill-qwen-14b", api_key="lm-studio"):
        self.client = openai.OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def _clean_verdict(self, full_text: str) -> str:
        """
        Helper method to isolate the final verdict.
        Removes any <think> tags natively returned by the model,
        and splits the text returning only the segment after --- VERDICT ---.
        """
        import re
        
        # 1. Remove internal reasoning from deepseek-r1 native think tags if present
        text = re.sub(r'<think>.*?</think>', '', full_text, flags=re.DOTALL).strip()
        
        # 2. Extract final verdict if our explicit tags are present
        if "--- VERDICT ---" in text:
            parts = text.split("--- VERDICT ---")
            return parts[-1].strip()
        
        # 3. Strip text between REASONING and VERDICT if VERDICT is missing but REASONING is there 
        # (usually means it's malformed, so we strip the tag itself)
        if "--- REASONING ---" in text:
            text = re.sub(r'--- REASONING ---.*?--- VERDICT ---', '', text, flags=re.DOTALL)
            text = text.replace("--- REASONING ---", "")
            
        return text.strip()

    def evaluate_log(self, log_content: str, initial_score: int, matched_rules: list[str]) -> str:
        """
        Sends the suspicious log content to the local LLM for evaluation.
        """
        prompt = (
            f"Analyze the following log entry for malicious activity.\n\n"
            f"Log Entry: {log_content}\n"
            f"Regex Check Findings:\n"
            f"Initial Threat Score: {initial_score}\n"
            f"Matched Signatures: {', '.join(matched_rules) if matched_rules else 'None'}\n\n"
            f"Task: Based on these findings and your analysis, explain what kind of attack this might be "
            f"(if any), and provide a concise recommendation on how to proceed."
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior cybersecurity analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            message = response.choices[0].message
            content = message.content.strip() if message.content else "No direct content returned."
            reasoning = getattr(message, "reasoning_content", None)
            
            output = ""
            if reasoning:
                output += f"--- REASONING ---\n{reasoning.strip()}\n\n"
            output += f"--- VERDICT ---\n{content}"
            
            return self._clean_verdict(output)
        except Exception as e:
            return f"Error communicating with local LLM. Make sure your local LLM correctly adheres to the OpenAI API and is running. Details: {str(e)}"
