import random
from datetime import datetime

def generate_test_file(filename="test_dataset.log", total_logs=100):
    ips = ["192.168.1.20", "10.0.0.15", "172.16.0.5", "8.8.8.8", "151.12.44.33"]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/91.0"
    ]
    pages = ["/index.html", "/about", "/contact", "/products?id=123", "/blog/post-1", "/css/style.css", "/js/main.js"]
    
    with open(filename, "w") as f:
        # Generiamo 97 log innocui
        for i in range(total_logs - 3):
            ip = random.choice(ips)
            date = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
            page = random.choice(pages)
            ua = random.choice(user_agents)
            f.write(f'{ip} - - [{date}] "GET {page} HTTP/1.1" 200 {random.randint(500, 5000)} "-" "{ua}"\n')
        
        # Inseriamo i 3 "Cattivi" (le nostre esche per LogSentry)
        date_now = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
        
        # 1. SQL Injection (Score alto)
        f.write(f'45.33.22.11 - - [{date_now}] "GET /admin?id=10%20OR%201=1 HTTP/1.1" 200 120 "-" "sqlmap/1.8.2"\n')
        
        # 2. Path Traversal (Score alto)
        f.write(f'93.184.216.34 - - [{date_now}] "GET /../../../../etc/passwd HTTP/1.1" 404 220 "-" "Nikto/2.1.6"\n')
        
        # 3. RCE con Base64 (Score critico)
        f.write(f'112.213.10.5 - - [{date_now}] "POST /api/exec?cmd=Y2F0IC9ldGMvcGFzc3dkCg== HTTP/1.1" 200 890 "-" "python-requests/2.28.1"\n')

    print(f"✅ File '{filename}' generato con successo!")

if __name__ == "__main__":
    generate_test_file()