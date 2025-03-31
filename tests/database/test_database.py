import pytest
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

@pytest.fixture(scope="session")
def test_db():
    dbname = "test_db_intuitive_care"
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
        cur.execute(f"CREATE DATABASE {dbname}")
        
        conn.close()
        
        test_conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        
        yield test_conn
        
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
    
    with open('database/create_tables.sql', 'r') as f:
        cur.execute(f.read())
    
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
    
    with open('database/create_tables.sql', 'r') as f:
        cur.execute(f.read())
    
    with open('database/load_data.sql', 'r') as f:
        cur.execute(f.read())
    
    cur.execute("SELECT COUNT(*) FROM operator_registration")
    assert cur.fetchone()[0] > 0
    
    cur.execute("SELECT COUNT(*) FROM quarterly_balance")
    assert cur.fetchone()[0] > 0 