import pytest
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

@pytest.fixture(scope="session")
def test_db():
    # Configurações do banco de teste usando variáveis de ambiente ou valores padrão
    dbname = "test_db_intuitive_care"
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')  # Altere para sua senha real
    host = os.getenv('POSTGRES_HOST', 'localhost')
    
    try:
        # Cria banco de teste
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Dropa o banco se existir e cria novo
        cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
        cur.execute(f"CREATE DATABASE {dbname}")
        
        conn.close()
        
        # Conecta ao banco de teste
        test_conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        
        yield test_conn
        
        # Cleanup
        test_conn.close()
        
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
        conn.close()
        
    except psycopg2.OperationalError as e:
        pytest.skip(f"Não foi possível conectar ao banco de dados: {str(e)}")

def test_create_tables(test_db):
    cur = test_db.cursor()
    
    # Executa o script de criação
    with open('database/create_tables.sql', 'r') as f:
        cur.execute(f.read())
    
    # Verifica se as tabelas foram criadas
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    tables = [row[0] for row in cur.fetchall()]
    assert 'quarterly_balance' in tables
    assert 'operator_registration' in tables

def test_load_data(test_db):
    cur = test_db.cursor()
    
    # Primeiro cria as tabelas
    with open('database/create_tables.sql', 'r') as f:
        cur.execute(f.read())
    
    # Depois carrega os dados
    with open('database/load_data.sql', 'r') as f:
        cur.execute(f.read())
    
    # Verifica se há dados nas tabelas
    cur.execute("SELECT COUNT(*) FROM operator_registration")
    assert cur.fetchone()[0] > 0
    
    cur.execute("SELECT COUNT(*) FROM quarterly_balance")
    assert cur.fetchone()[0] > 0 