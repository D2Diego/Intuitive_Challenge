from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="db_intuitive_care",
        user="d2dev",
        password="123456"
    )

@app.route('/api/operadoras/search')
def search_operadoras():
    search_term = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 5  # Número de itens por página
    offset = (page - 1) * per_page
    
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Busca os resultados paginados
        cur.execute("""
            SELECT * FROM cadastro_operadoras 
            WHERE nome_fantasia ILIKE %s 
            OR razao_social ILIKE %s 
            LIMIT %s OFFSET %s
        """, (f'%{search_term}%', f'%{search_term}%', per_page, offset))
        
        results = cur.fetchall()

        # Conta o total de resultados para a paginação
        cur.execute("""
            SELECT COUNT(*) FROM cadastro_operadoras 
            WHERE nome_fantasia ILIKE %s 
            OR razao_social ILIKE %s
        """, (f'%{search_term}%', f'%{search_term}%'))
        
        total = cur.fetchone()['count']
        total_pages = (total + per_page - 1) // per_page

        cur.close()
        conn.close()
        
        return jsonify({
            'results': results,
            'pagination': {
                'total': total,
                'per_page': per_page,
                'current_page': page,
                'total_pages': total_pages
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
