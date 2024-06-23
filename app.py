import os
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Configurações do S3
S3_BUCKET = 'gramato'
S3_ACCESS_KEY = '689675422637'  # Substitua com sua própria chave de acesso
S3_SECRET_KEY = 'AKIA2BE63ZOW5HJRUVVO'  # Substitua com sua própria chave secreta

# Função para realizar o upload para o S3
def upload_to_s3(file, bucket_name, acl='public-read'):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                'ACL': acl,
                'ContentType': file.content_type
            }
        )

    except ClientError as e:
        return str(e)

    return f'https://{bucket_name}.s3.amazonaws.com/{file.filename}'

# Rota para realizar o upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Verifica se existe um arquivo na requisição
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        # Verifica se o arquivo tem um nome
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400

        # Realiza o upload para o S3
        file_url = upload_to_s3(file, S3_BUCKET)

        return jsonify({'file_url': file_url}), 200

if __name__ == '__main__':
    app.run(debug=True)
