from flask import Blueprint, jsonify, request
from app.services.operadora_service import OperadoraService
import psycopg2


operadora_bp = Blueprint('operadora', __name__)

@operadora_bp.route('/operadoras/search')
def search_operadoras():
    try:
        search_term = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        
        if page < 1:
            return jsonify({'error': 'Page number must be greater than 0'}), 400
            
        result = OperadoraService.search_operadoras(search_term, page)
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({'error': 'Invalid page number'}), 400
    except psycopg2.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500 