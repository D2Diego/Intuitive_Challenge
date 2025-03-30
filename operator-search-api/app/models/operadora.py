class Operadora:
    def __init__(self, data):
        self.id = data.get('id')
        self.nome_fantasia = data.get('nome_fantasia')
        self.razao_social = data.get('razao_social')

    def to_dict(self):
        return {
            'id': self.id,
            'nome_fantasia': self.nome_fantasia,
            'razao_social': self.razao_social
        } 