import subprocess
import sys
import os

def check_python_version():
    if sys.version_info < (3, 7):
        print("Python 3.7 ou superior é necessário")
        sys.exit(1)

def install_python_dependencies():
    print("Instalando dependências Python...")
    requirements = [
        "requests",
        "beautifulsoup4",
        "pandas",
        "tabula-py",
        "jpype1",
        "psycopg2-binary",
        "flask",
        "flask-cors"
    ]
    for package in requirements:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_java():
    try:
        subprocess.check_call(["java", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Java está instalado!")
    except:
        print("AVISO: Java não encontrado! Por favor, instale o Java Runtime Environment (JRE)")
        print("Instruções de instalação do Java:")
        print("Ubuntu/Debian: sudo apt-get install default-jre")
        print("Windows: Baixe e instale de https://www.java.com/download/")
        print("macOS: brew install --cask java")

def setup_node_project():
    if os.path.exists("operator-search"):
        print("Configurando projeto Vue.js...")
        os.chdir("operator-search")
        try:
            subprocess.check_call(["npm", "install"])
            print("Dependências Node.js instaladas com sucesso!")
        except:
            print("AVISO: Erro ao instalar dependências Node.js")
            print("Certifique-se de ter o Node.js instalado: https://nodejs.org/")
        os.chdir("..")

def create_directories():
    directories = [
        "scraper/downloads/pdfs",
        "scraper/downloads/zips",
        "transformer/temp",
        "transformer/output",
        "resultados"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("Diretórios do projeto criados!")

def main():
    print("Iniciando setup do projeto...")
    check_python_version()
    check_java()
    install_python_dependencies()
    create_directories()
    setup_node_project()
    print("\nSetup concluído!")
    print("\nPróximos passos:")
    print("1. Configure o banco de dados PostgreSQL")
    print("2. Execute os scripts SQL em Teste_3/create_tables.sql")
    print("3. Para iniciar o frontend: cd operator-search && npm run serve")

if __name__ == "__main__":
    main() 