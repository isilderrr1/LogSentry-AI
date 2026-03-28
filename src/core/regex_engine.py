import re
from dataclasses import dataclass

@dataclass
class RegexRule:
    name: str
    pattern: str
    description: str
    score: int
    flags: int = re.IGNORECASE

class RegexAnalyzer:
    def __init__(self):
        # Baseline rules
        self.rules = [
            RegexRule(
                name="Base64 Encoding",
                # Match somewhat long base64 strings to reduce noise (e.g. at least ~20 characters)
                pattern=r"(?:[A-Za-z0-9+/]{4}){5,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?",
                description="Potential base64 encoded payload",
                score=40,
                flags=0
            ),
            RegexRule(
                name="SQL Injection",
                pattern=r"(?i)('\s*OR\s*1\s*=\s*1|UNION\s+SELECT|DROP\s+TABLE|--$)",
                description="Common SQLi pattern detected",
                score=80
            ),
            RegexRule(
                name="Suspicious User-Agent",
                pattern=r"(?i)(curl|python-requests|nmap|nikto|sqlmap)",
                description="Automated or malicious tool signature in User-Agent",
                score=60
            ),
            RegexRule(
                name="Cross-Site Scripting (XSS)",
                pattern=r"(?i)(<script>|<script\s+.*?>|javascript:|<iframe>|<iframe\s+.*?>|onerror\s*=|onload\s*=)",
                description="Common XSS patterns like <script> tags or javascript protocols",
                score=80
            ),
            RegexRule(
                name="Path Traversal",
                pattern=r"(?i)(\.\./|\\\\\.\\|/etc/passwd|/windows/system32/cmd\.exe)",
                description="Path traversal attempts indicating LFI or sensitive file access",
                score=70
            )
        ]

    def analyze(self, text: str) -> dict:
        """
        Analyzes the text against all compiled regex rules.
        """
        total_score = 0
        matched_rules = []
        
        for rule in self.rules:
            if re.search(rule.pattern, text, rule.flags):
                total_score += rule.score
                matched_rules.append(rule.name)
        
        # Cap the final score at 100 for normalization
        return {
            "score": min(total_score, 100),
            "matches": matched_rules,
            "raw_score": total_score
        }
