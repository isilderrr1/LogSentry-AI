import pytest
from src.core.regex_engine import RegexAnalyzer

@pytest.fixture
def analyzer():
    return RegexAnalyzer()

def test_safe_log(analyzer):
    log = "GET /index.html HTTP/1.1 Mozilla/5.0"
    result = analyzer.analyze(log)
    assert result["score"] == 0
    assert len(result["matches"]) == 0

def test_sqli_detection(analyzer):
    log = "GET /login?user=admin' OR 1=1-- HTTP/1.1"
    result = analyzer.analyze(log)
    assert result["score"] >= 80
    assert "SQL Injection" in result["matches"]

def test_suspicious_user_agent(analyzer):
    log = "GET /api/data HTTP/1.1 sqlmap/1.5.8"
    result = analyzer.analyze(log)
    assert result["score"] >= 50
    assert "Suspicious User-Agent" in result["matches"]

def test_base64_detection(analyzer):
    log = "Payload: dGhpcyBpcyBhIHRlc3QgcGF5bG9hZCBmb3IgYmFzZTY0Cg=="
    result = analyzer.analyze(log)
    assert result["score"] >= 40
    assert "Base64 Encoding" in result["matches"]

def test_xss_detection(analyzer):
    log = "GET /search?q=<script>alert(1)</script> HTTP/1.1"
    result = analyzer.analyze(log)
    assert result["score"] >= 80
    assert "Cross-Site Scripting (XSS)" in result["matches"]

def test_path_traversal_detection(analyzer):
    log = "GET /download?file=../../../../etc/passwd HTTP/1.1"
    result = analyzer.analyze(log)
    assert result["score"] >= 70
    assert "Path Traversal" in result["matches"]

def test_multiple_matches_and_score_cap(analyzer):
    # Log with both SQLi and suspicious user agent
    log = "GET /?id=1' UNION SELECT HTTP/1.1 nmap"
    result = analyzer.analyze(log)
    assert "SQL Injection" in result["matches"]
    assert "Suspicious User-Agent" in result["matches"]
    assert result["score"] == 100
    assert result["raw_score"] == 140 # 80 + 60 = 140
