import json

class EmailDataLoader:
    """Class responsible for loading email data from a JSON file."""

    @staticmethod
    def load_data(json_file):
        """
        Loads purchase data from a JSON file.

        Args:
            json_file (str): The path to the JSON file containing purchase data.

        Returns:
            dict: The loaded data from the JSON file.
        """
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

class EmailBodyGenerator:
    """Class responsible for generating the email body from a template."""

    def __init__(self, template_file):
        """
        Initializes the EmailBodyGenerator with a specified template file.

        Args:
            template_file (str): The path to the email template file.
        """
        self.template_file = template_file

    def generate(self, data):
        """
        Generates the email body by formatting the template with the provided data.

        Args:
            data (dict): A dictionary containing the information needed to populate the template.

        Returns:
            str: The formatted email body.
        """
        with open(self.template_file, 'r', encoding='utf-8') as file:
            template = file.read()

        buyer = data['comprador']
        products = data['produtos']
        payment = data['pagamento']
        delivery = data['entrega']
        
        email_body = template.format(
            nome=buyer['nome'],
            numero_nota=data['nota_fiscal']['numero'],
            serie=data['nota_fiscal']['serie'],
            data_emissao=data['nota_fiscal']['data_emissao'],
            descricao_produto=products[0]['descricao'],
            quantidade=products[0]['quantidade'],
            valor_unitario=products[0]['valor_unitario'],
            valor_total=products[0]['valor_total'],
            forma_pagamento=payment['forma'],
            valor_pagamento=payment['valor_total'],
            numero_parcelas=payment['numero_parcelas'],
            valor_parcela=payment['valor_parcela'],
            bandeira_cartao=payment['bandeira_cartao'],
            cartao_mascarado=payment['cartao_mascarado'],
            status_pagamento=payment['status'],
            data_entrega=delivery['data_prevista'],
            endereco_entrega=f"{delivery['endereco_entrega']['logradouro']}, "
                             f"{delivery['endereco_entrega']['numero']}, "
                             f"{delivery['endereco_entrega']['complemento']}, "
                             f"{delivery['endereco_entrega']['bairro']}, "
                             f"{delivery['endereco_entrega']['cidade']}, "
                             f"{delivery['endereco_entrega']['uf']} - "
                             f"{delivery['endereco_entrega']['cep']}"
        )
        
        return email_body
