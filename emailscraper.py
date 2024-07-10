from collections import deque
import re
from bs4 import BeautifulSoup
import requests
import urllib.parse

print('''
██████╗ ███████╗  ██████╗      
██╔══██╗██╔════╝ ██╔═══██╗    
██████╔╝█████╗   ██╔═══██╝    
██╔═══╝ ██╔══╝   ███████      
██║     ███████╗ ███  ███     
╚═╝     ╚══════╝ ╚═╝  ╚═╝     
''')
print('Made with ❤️ by Mamanwhide')

try:
    user_url = input('\n[+] Masukkan URL: ').strip()
    limit = int(input('[+] Masukkan Limit Pencarian: ').strip())
except ValueError:
    print("Error: Limit harus berupa bilangan bulat.")
    exit()

urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0

try:
    while urls and count < limit:
        count += 1
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        print(f'[*] {count} Memproses {url}')

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error saat mengambil {url}: {e}")
            continue

        new_emails = set(re.findall(r'[a-z0-9.\-+_]+@\w+\.[a-z.]+', response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.get('href', '')
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = urllib.parse.urljoin(url, link)

            if link not in urls and link not in scraped_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Proses Dihentikan oleh Pengguna')
except Exception as e:
    print(f"Error: {e}")

print('\n==================== Proses Selesai =======================')
print(f'================== {len(emails)} Email Ditemukan!! ====================')
print('\n===========================================================')

for mail in emails:
    print('                    ' + mail
