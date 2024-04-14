import boto3
import sys

BUCKET_NAME = "my-app-files-bucket"
AWS_S3_REGION = "us-east-1"
BUCKET_PATH = "https://my-app-files-bucket.s3.amazonaws.com"

def carrega_s3(access_key_id, secret_access_key):
    try: 
        if access_key_id is None or secret_access_key is None:
            raise ValueError('Credenciais inválidas!')

        # Componente para acessar o AWS S3
        my_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        print("Componente de acesso ao S3 carregado com sucesso!")
        return my_s3
    except Exception as ex:
        print(f"Erro ao carregar o componente do S3: {str(ex)}")
        sys.exit(1)