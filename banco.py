from flask_sqlalchemy import SQLAlchemy
import sys
from flask_login import UserMixin
from sqlalchemy import ForeignKey

INSTANCIA_DB_AWS_RDS = 'mydbfilesteste.cdwkkuakqpji.us-east-1.rds.amazonaws.com'
BANCO_AWS_RDS = 'mydbfiles'

# componente de banco de dados
db = SQLAlchemy()

user_files = db.Table('user_files', 
    db.Column('user_id', db.Integer(), ForeignKey('users.id')), 
    db.Column('file_id', db.Integer(), ForeignKey('files.id')) 
)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False) 
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    my_files = db.relationship('File', secondary=user_files, backref='myfiles')

# Classe que representa os dados de um arquivo
class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))

class UserDAO:
    def __init__(self, db):
        self.db = db

    def create_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def user_by_id(self, user_id):
        return User.query.get(user_id)

    def user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def update_user(self, user):
        self.db.session.merge(user)
        self.db.session.commit()

    def delete_user_by_id(self, user_id):
        user = self.user_by_id(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()

    def list_users(self):
        return User.query.all()

    def link_to_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            file = File.query.filter_by(id=file.id).first()
            user.my_files.append(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during file to user - {ve}')

    def link_to_files(self, user_id, files):
        try:
            user = User.query.filter_by(id=user_id).first()
            for each in files:
                file = File.query.filter_by(id=each.id).first()
                user.my_files.append(file)    
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during files to user - {ve}')

    def unlink_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            file = File.query.filter_by(id=file.id).first()
            user.my_files.remove(file)
            self.db.session.commit()
        except Exception as e:
            raise Exception(f'Error during remove file from user - {e}')

    def list_all_files(self, user_id):
        user = User.query.filter_by(id=user_id).first()        
        return user.my_files

    def get_file_by_user(self, name):        
        return User.my_files.query.get(name)

class FilesDAO:
    def __init__(self, db):
        self.db = db

    def insert_file(self, file):
        try:
            self.db.session.add(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during insert file - {ve}')

    def query_file_by_name(self, p_name):
        file = File.query.filter_by(name=p_name).first()
        return file

    def query_file_by_id(self, p_id):
        file = File.query.filter_by(id=p_id).first()
        return file
    
    def list_all_files(self):
        return File.query.all()

    def delete_file(self, file):
        try:
            file = File.query.filter_by(id=file.id).first()
            self.db.session.delete(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during delete file - {ve}')

# Cria as tabelas do banco
def create_tables(app, drop_data_base):
    try:
        with app.app_context():
            print('Carrega as tabelas do banco')
            if drop_data_base: 
                db.drop_all()
                db.create_all()
                db.session.commit()
            print('Tabelas carregadas com sucesso!')
    except Exception as ex:
        print(f'Erro ao carregar o banco! {str(ex)}')
        sys.exit(1)