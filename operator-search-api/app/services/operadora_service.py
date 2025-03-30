from app.database.connection import get_db_connection
from psycopg2.extras import RealDictCursor


class OperadoraService:
    @staticmethod
    def search_operadoras(search_term, page, per_page=5):
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            offset = (page - 1) * per_page
            
            query = """
                SELECT 
                    id, 
                    Nome_Fantasia as nome_fantasia, 
                    Razao_Social as razao_social,
                    Registro_ANS as registro_ans,
                    CNPJ as cnpj,
                    Modalidade as modalidade,
                    Cidade as cidade,
                    UF as uf,
                    Telefone as telefone
                FROM operator_registration 
                WHERE LOWER(Nome_Fantasia) LIKE LOWER(%s) 
                OR LOWER(Razao_Social) LIKE LOWER(%s) 
                LIMIT %s OFFSET %s
            """
            params = (f'%{search_term}%', f'%{search_term}%', per_page, offset)
            
            cur.execute(query, params)
            results = cur.fetchall()

            count_query = """
                SELECT COUNT(*) FROM operator_registration 
                WHERE LOWER(Nome_Fantasia) LIKE LOWER(%s) 
                OR LOWER(Razao_Social) LIKE LOWER(%s)
            """
            count_params = (f'%{search_term}%', f'%{search_term}%')
            
            cur.execute(count_query, count_params)
            total = cur.fetchone()['count']
            total_pages = (total + per_page - 1) // per_page

            cur.close()
            conn.close()
            
            return {
                'results': results,
                'pagination': {
                    'total': total,
                    'per_page': per_page,
                    'current_page': page,
                    'total_pages': total_pages
                }
            }
            
        except Exception as e:
            raise e 