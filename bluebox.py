#!/usr/bin/env python3
# ============================================================
#   ██████╗ ██╗     ██╗   ██╗███████╗██████╗  ██████╗ ██╗  ██╗
#   ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝
#   ██████╔╝██║     ██║   ██║█████╗  ██████╔╝██║   ██║ ╚███╔╝ 
#   ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ 
#   ██████╔╝███████╗╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗
#   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
#                                                         
#   ██████╗ ██╗      ██████╗ ███████╗██████╗  ██████╗ ██╗  ██╗
#   ██╔══██╗██║     ██╔═══██╗██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝
#   ██████╔╝██║     ██║   ██║█████╗  ██████╔╝██║   ██║ ╚███╔╝ 
#   ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ 
#   ██████╔╝███████╗╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗
#   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
#                                                         
#   BLUEBOX v1.0 - COMPLETE EDITION                      
#   create by vikk official                               
#   "Control everything." 🔥                            
# ============================================================

import os
import sys
import time
import json
import subprocess
import threading
import shutil
import re
from datetime import datetime

try:
    import requests
except ImportError:
    print("\033[91m   [!] requests not installed. Run: pip install requests\033[0m")
    sys.exit(1)

# ============================================================
#  WARNA
# ============================================================
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
B = '\033[94m'
M = '\033[95m'
N = '\033[0m'

# ============================================================
#  KONFIGURASI
# ============================================================
GEMINI_API_KEY = "AQ.Ab8RN6LJRYzjmm5oKqxRcPQw4Gz1cuMOGHOA04rPu-9qrfpEtQ"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# ============================================================
#  LOADING
# ============================================================
def load_spin(text, dur=0.8):
    chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    end = time.time() + dur
    i = 0
    while time.time() < end:
        sys.stdout.write(f'\r  {C}[{chars[i % len(chars)]}] {text}{N}')
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f'\r  {G}[✓] {text}{N}\n')

def load_prog(cur, total, label='processing'):
    bar_len = 35
    filled = int(bar_len * cur / total)
    bar = '█' * filled + '░' * (bar_len - filled)
    pct = int(cur * 100 / total)
    sys.stdout.write(f'\r  {C}[{bar}] {pct}%  -  {label}{N}')
    sys.stdout.flush()

# ============================================================
#  BANNER
# ============================================================
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{B}
   ██████╗ ██╗     ██╗   ██╗███████╗██████╗  ██████╗ ██╗  ██╗
   ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝
   ██████╔╝██║     ██║   ██║█████╗  ██████╔╝██║   ██║ ╚███╔╝ 
   ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ 
   ██████╔╝███████╗╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗
   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
{N}""")
    print(f"""{C}
   ██████╗ ██╗      ██████╗ ███████╗██████╗  ██████╗ ██╗  ██╗
   ██╔══██╗██║     ██╔═══██╗██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝
   ██████╔╝██║     ██║   ██║█████╗  ██████╔╝██║   ██║ ╚███╔╝ 
   ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ 
   ██████╔╝███████╗╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗
   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
{N}""")
    print(f"{B}   ════════════════════════════════════════════════════════════{N}")
    print(f"   BLUEBOX v1.0  |  complete edition")
    print(f"   create by {R}vikk official{N}")
    print(f"   {C}\"Control everything.\" 🔥{N}")
    print(f"{B}   ════════════════════════════════════════════════════════════{N}\n")

# ============================================================
#  AI CHAT
# ============================================================
def ask_ai(prompt, context=""):
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return "⚠️ Please set your Gemini API key in the script."
    
    full_prompt = f"""You are BLUEBOX, a coding assistant specialized in software development.
Help with code, debugging, architecture, and technical questions.
Be precise and provide code examples when relevant.

Context: {context if context else 'None'}

User: {prompt}
"""
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    
    try:
        response = requests.post(GEMINI_URL, json=payload)
        data = response.json()
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text']
        return f"❌ Error: {data}"
    except Exception as e:
        return f"❌ Error: {e}"

# ============================================================
#  FEATURE 1: WEB CLONER
# ============================================================
def web_cloner():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  🌐  WEB CLONER                                 │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    url = input(f"{C}   ➜ Target URL: {N}")
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    depth = input(f"{C}   ➜ Depth (1-3): {N}")
    depth = int(depth) if depth.isdigit() else 1
    
    folder = input(f"{C}   ➜ Output folder: {N}")
    if not folder:
        folder = url.replace('https://', '').replace('http://', '').replace('/', '_')
    
    print()
    load_spin(f"Cloning {url} to {folder}...")
    
    os.makedirs(folder, exist_ok=True)
    
    try:
        response = requests.get(url, timeout=10)
        with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"{G}   ✓ index.html saved{N}")
        
        css_links = re.findall(r'href=[\'"]?([^\'" >]+\.css)', response.text)
        js_links = re.findall(r'src=[\'"]?([^\'" >]+\.js)', response.text)
        
        for css in css_links[:5]:
            try:
                css_url = url + css if css.startswith('/') else css
                css_resp = requests.get(css_url, timeout=5)
                css_file = css.split('/')[-1]
                with open(os.path.join(folder, css_file), 'w', encoding='utf-8') as f:
                    f.write(css_resp.text)
                print(f"{G}   ✓ {css_file} saved{N}")
            except:
                pass
        
        print(f"\n{G}   ✅ Clone completed!{N}")
        print(f"   📂 Saved to: {os.path.abspath(folder)}{N}")
    except Exception as e:
        print(f"{R}   ✗ Error: {e}{N}")

# ============================================================
#  FEATURE 2: CODE CHAT
# ============================================================
def code_chat():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  💬  CODE CHAT                                  │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    print(f"   {Y}Type 'exit' to return{N}\n")
    
    while True:
        user_input = input(f"{C}   ➜ {N}")
        if user_input.lower() == 'exit':
            break
        
        print()
        load_spin("BLUEBOX is thinking...")
        reply = ask_ai(user_input)
        print(f"\n{G}   🤖 BLUEBOX AI:{N}\n{reply}\n")

# ============================================================
#  FEATURE 3: GENERATE CODE
# ============================================================
def generate_code():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  💻  GENERATE CODE                              │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    lang = input(f"{C}   ➜ Language (python/js/bash/go): {N}")
    task = input(f"{C}   ➜ What to build: {N}")
    
    prompt = f"Write complete {lang} code for: {task}. Include imports and main function. Only provide code, no explanation."
    
    print()
    load_spin("BLUEBOX is generating code...")
    reply = ask_ai(prompt)
    print(f"\n{G}   🤖 BLUEBOX AI:{N}\n{reply}\n")
    
    save = input(f"{C}   ➜ Save to file? (y/n): {N}")
    if save.lower() == 'y':
        filename = input(f"{C}   ➜ Filename: {N}")
        ext = {'python': '.py', 'js': '.js', 'bash': '.sh', 'go': '.go'}
        if not filename.endswith(ext.get(lang, '.txt')):
            filename += ext.get(lang, '.txt')
        with open(filename, 'w') as f:
            f.write(reply)
        print(f"{G}   ✓ Saved to {filename}{N}")

# ============================================================
#  FEATURE 4: EXPLAIN CODE
# ============================================================
def explain_code():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  📖  EXPLAIN CODE                              │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    path = input(f"{C}   ➜ File path: {N}")
    try:
        with open(path, 'r') as f:
            code = f.read()
    except Exception as e:
        print(f"{R}   ✗ Error: {e}{N}")
        return
    
    print()
    load_spin("BLUEBOX is analyzing code...")
    reply = ask_ai(f"Explain this code in simple terms:\n{code[:3000]}")
    print(f"\n{G}   🤖 BLUEBOX AI:{N}\n{reply}\n")

# ============================================================
#  FEATURE 5: DEBUG CODE
# ============================================================
def debug_code():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  🐛  DEBUG CODE                                │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    path = input(f"{C}   ➜ File path: {N}")
    try:
        with open(path, 'r') as f:
            code = f.read()
    except Exception as e:
        print(f"{R}   ✗ Error: {e}{N}")
        return
    
    error = input(f"{C}   ➜ Error message (if any): {N}")
    
    print()
    load_spin("BLUEBOX is debugging...")
    reply = ask_ai(f"Debug this code:\n{code[:3000]}\n\nError: {error if error else 'None'}")
    print(f"\n{G}   🤖 BLUEBOX AI:{N}\n{reply}\n")

# ============================================================
#  FEATURE 6: CODE COMPLETION
# ============================================================
def code_completion():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  ✨  CODE COMPLETION                           │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    code = input(f"{C}   ➜ Paste your code (or type 'done'): {N}")
    if code.lower() == 'done':
        return
    
    print()
    load_spin("BLUEBOX is completing code...")
    reply = ask_ai(f"Complete this code:\n{code}")
    print(f"\n{G}   🤖 BLUEBOX AI:{N}\n{reply}\n")

# ============================================================
#  FEATURE 7: FILE OPERATIONS
# ============================================================
def file_ops():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  📁  FILE OPERATIONS                           │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    print(f"   {G}1{N}  Create file")
    print(f"   {G}2{N}  Edit file")
    print(f"   {G}3{N}  Delete file")
    print(f"   {G}4{N}  List files")
    print(f"   {G}5{N}  Search in files")
    print()
    choice = input(f"{C}   ➜ select (1-5): {N}")
    
    if choice == '1':
        path = input(f"{C}   ➜ File name: {N}")
        content = input(f"{C}   ➜ Content: {N}")
        with open(path, 'w') as f:
            f.write(content)
        print(f"{G}   ✓ Created {path}{N}")
    
    elif choice == '2':
        path = input(f"{C}   ➜ File name: {N}")
        try:
            with open(path, 'r') as f:
                print(f"{Y}   Current content:{N}\n{f.read()}\n")
        except:
            pass
        content = input(f"{C}   ➜ New content: {N}")
        with open(path, 'w') as f:
            f.write(content)
        print(f"{G}   ✓ Updated {path}{N}")
    
    elif choice == '3':
        path = input(f"{C}   ➜ File name: {N}")
        os.remove(path)
        print(f"{G}   ✓ Deleted {path}{N}")
    
    elif choice == '4':
        files = os.listdir('.')
        for f in files:
            size = os.path.getsize(f)
            print(f"   {G}📄{N} {f} ({size} bytes)")
    
    elif choice == '5':
        term = input(f"{C}   ➜ Search term: {N}")
        for root, dirs, files in os.walk('.'):
            for f in files:
                try:
                    with open(os.path.join(root, f), 'r') as file:
                        if term in file.read():
                            print(f"   {G}🔍{N} {os.path.join(root, f)}")
                except:
                    pass

# ============================================================
#  FEATURE 8: RUN COMMAND
# ============================================================
def run_command():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  🖥️  RUN COMMAND                               │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    cmd = input(f"{C}   ➜ Command: {N}")
    if not cmd:
        return
    
    print()
    load_spin("Executing command...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout:
            print(f"\n{G}   Output:{N}\n{result.stdout}")
        if result.stderr:
            print(f"\n{R}   Error:{N}\n{result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"{R}   ✗ Timeout (30s){N}")
    except Exception as e:
        print(f"{R}   ✗ Error: {e}{N}")

# ============================================================
#  FEATURE 9: FULL-STACK AGENT
# ============================================================
def fullstack_agent():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  🚀  FULL-STACK AGENT                         │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    idea = input(f"{C}   ➜ Describe your project idea: {N}")
    
    print()
    load_spin("BLUEBOX is planning your project...")
    
    plan = ask_ai(f"""Create a full-stack project plan for: {idea}
    Include:
    1. Tech stack (frontend, backend, database)
    2. Folder structure
    3. Main components
    4. API endpoints
    5. Deployment steps
    Format as structured plan.""")
    
    print(f"\n{G}   🤖 BLUEBOX AI - Project Plan:{N}\n{plan}\n")
    
    build = input(f"{C}   ➜ Generate boilerplate code? (y/n): {N}")
    if build.lower() == 'y':
        lang = input(f"{C}   ➜ Language (python/js): {N}")
        print()
        load_spin("Generating boilerplate...")
        code = ask_ai(f"Generate boilerplate {lang} code for: {idea}")
        print(f"\n{G}   🤖 BLUEBOX AI:{N}\n{code}\n")
        
        save = input(f"{C}   ➜ Save to project? (y/n): {N}")
        if save.lower() == 'y':
            folder = input(f"{C}   ➜ Project folder: {N}")
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, 'main.' + ('py' if lang == 'python' else 'js')), 'w') as f:
                f.write(code)
            print(f"{G}   ✓ Project created in {folder}{N}")

# ============================================================
#  FEATURE 10: AI TERMINAL
# ============================================================
def ai_terminal():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  💬  AI TERMINAL                               │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    print(f"   {Y}Type your command or ask anything{N}")
    print(f"   {Y}Type 'exit' to return{N}\n")
    
    while True:
        user_input = input(f"{C}   ➜ {N}")
        if user_input.lower() == 'exit':
            break
        
        print()
        load_spin("BLUEBOX is processing...")
        reply = ask_ai(user_input)
        print(f"\n{G}   🤖 BLUEBOX:{N}\n{reply}\n")

# ============================================================
#  FEATURE 11: TOOL RUNNER (Clone & Install)
# ============================================================
def tool_runner():
    print()
    print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
    print(f"{C}   │  🔧  TOOL RUNNER (Clone & Install)               │{N}")
    print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
    
    repo = input(f"{C}   ➜ GitHub URL: {N}")
    if not repo:
        print(f"{R}   ✗ URL required!{N}")
        return
    
    print()
    load_spin(f"Cloning {repo}...")
    
    repo_name = repo.split('/')[-1].replace('.git', '')
    
    try:
        subprocess.run(['git', 'clone', repo], check=True)
        print(f"{G}   ✓ Cloned to {repo_name}{N}")
    except Exception as e:
        print(f"{R}   ✗ Clone failed: {e}{N}")
        return
    
    os.chdir(repo_name)
    
    install_cmd = None
    if os.path.exists('install.sh'):
        install_cmd = ['bash', 'install.sh']
    elif os.path.exists('setup.sh'):
        install_cmd = ['bash', 'setup.sh']
    elif os.path.exists('requirements.txt'):
        install_cmd = ['pip', 'install', '-r', 'requirements.txt']
    elif os.path.exists('package.json'):
        install_cmd = ['npm', 'install']
    elif os.path.exists('Makefile'):
        install_cmd = ['make']
    elif os.path.exists('setup.py'):
        install_cmd = ['python', 'setup.py', 'install']
    
    if install_cmd:
        print(f"{Y}   📦 Detected: {' '.join(install_cmd)}{N}")
        confirm = input(f"{C}   ➜ Run install? (y/n): {N}")
        if confirm.lower() == 'y':
            print()
            load_spin("Installing...")
            try:
                subprocess.run(install_cmd, check=True)
                print(f"{G}   ✓ Installation complete!{N}")
            except Exception as e:
                print(f"{R}   ✗ Install failed: {e}{N}")
    else:
        print(f"{Y}   ⚠️ No install script detected. Manual install required.{N}")
    
    print(f"\n{G}   ✅ Tool ready at: {os.path.abspath(repo_name)}{N}")
    print(f"   {C}➜ cd {repo_name} && python main.py (or run script){N}")
    os.chdir('..')
    input(f"\n{C}   Press Enter to continue...{N}")

# ============================================================
#  MAIN MENU
# ============================================================
def main():
    while True:
        banner()
        
        print(f"{C}   ┌─────────────────────────────────────────────────────┐{N}")
        print(f"{C}   │  📌  MAIN MENU                                   │{N}")
        print(f"{C}   └─────────────────────────────────────────────────────┘{N}")
        print()
        print(f"   {G}1{N}  🌐 Web Cloner (Clone Website)")
        print(f"   {G}2{N}  💬 Code Chat (BLUEBOX AI)")
        print(f"   {G}3{N}  💻 Generate Code")
        print(f"   {G}4{N}  📖 Explain Code")
        print(f"   {G}5{N}  🐛 Debug Code")
        print(f"   {G}6{N}  ✨ Code Completion")
        print(f"   {G}7{N}  📁 File Operations")
        print(f"   {G}8{N}  🖥️ Run Command")
        print(f"   {G}9{N}  🚀 Full-Stack Agent")
        print(f"   {G}10{N} 💬 AI Terminal")
        print(f"   {G}11{N} 🔧 Tool Runner (Clone & Install)")
        print(f"   {G}12{N} 🔧 Set API Key")
        print(f"   {R}0{N}  Exit")
        print()
        print(f"{C}   ─────────────────────────────────────────────────────{N}")
        choice = input(f"{C}   ➜ select (0-12): {N}")
        
        if choice == '1':
            web_cloner()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '2':
            code_chat()
        elif choice == '3':
            generate_code()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '4':
            explain_code()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '5':
            debug_code()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '6':
            code_completion()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '7':
            file_ops()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '8':
            run_command()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '9':
            fullstack_agent()
            input(f"\n{C}   Press Enter to continue...{N}")
        elif choice == '10':
            ai_terminal()
        elif choice == '11':
            tool_runner()
        elif choice == '12':
            new_key = input(f"{C}   ➜ Enter Gemini API Key: {N}")
            if new_key:
                global GEMINI_API_KEY, GEMINI_URL
                GEMINI_API_KEY = new_key
                GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
                print(f"{G}   ✓ API Key updated!{N}")
                time.sleep(1)
        elif choice == '0':
            print(f"\n{G}   BLUEBOX - Control everything. 🔥{N}")
            sys.exit(0)
        else:
            print(f"{R}   ✗ Invalid choice!{N}")
            time.sleep(1)

if __name__ == '__main__':
    main()
