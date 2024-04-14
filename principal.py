from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import banco
import s3_handle
import uuid
import utilidades
import requests
import base64
import io
from forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from flask_login import logout_user, LoginManager

# True para limpar a instancia banco de dados atual
# Obs: o valor deve ser True na 1a execucao da aplicacao
#      para criar um banco limpo a estrutura limpa das tabelas
DROP_DATA_BASE = False

# Carrega os valores das credenciais de acesso da AWS
ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
DB_USER = os.getenv('DB_USER')
PASSWORD_DB_USER = os.getenv('PASSWORD_DB_USER')

# String de conexao para o RDS
SQLALCHEMY_DATABASE_URI_AWS_RDS = f'mysql+pymysql://{DB_USER}:{PASSWORD_DB_USER}@{banco.INSTANCIA_DB_AWS_RDS}/{banco.BANCO_AWS_RDS}'
# String de conexao para banco local
SQLALCHEMY_DATABASE_URI_LOCAL = "sqlite:///users.db" 

# Instancia principal da aplicação
app = Flask(__name__)
app.secret_key = 'thisismysecretkeyfrommywebapplication'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_LOCAL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a instância do banco de dados
banco.db.init_app(app)
banco.create_tables(app, DROP_DATA_BASE)

# Para controle de login do usuario
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Carrega o componente S3
print('Carregando as credenciais da AWS')
s3 = s3_handle.carrega_s3(ACCESS_KEY_ID, SECRET_ACCESS_KEY)

# Carrega os DAOs de usuarios e arquivos
userDAO = banco.UserDAO(banco.db)
filesDAO = banco.FilesDAO(banco.db)

@login_manager.user_loader 
def load_user(user_id):
    return userDAO.user_by_id(user_id)

@login_manager.unauthorized_handler 
def unauthorized_callback():
    return redirect(url_for("login"))

# Lista os recursos disponiveis da web app
@app.route('/recursos')
def hello():
    print('Bem vindo ao Flask!')        
    print('Lista de recursos disponíveis: ')
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = str(rule.endpoint) + ' - '+ str(methods) + ' - '+ str(rule)
        output.append(line)

    for line in sorted(output):
        print(line)

    return render_template('home.html')

# Rota para a pagina home
@app.route("/")
def home_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    id_usuario = session['user_id']
    return render_template("home.html", id=id_usuario)

# Rota para a pagina de uploads
@app.route("/usuarios/<int:id>/upload", methods=["GET", "POST"])
def upload_page(id):
    if 'username' not in session or id != session['user_id']: 
        return redirect(url_for('login'))

    if request.method == "POST":
        try: 
            uploaded_file = request.files["file-to-save"]
            if not utilidades.allowed_file(uploaded_file.filename):
                flash("Tipo de arquivo não permitido!")
                return redirect(url_for('upload_page', id=id))

            new_filename = uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.', 1)[1].lower()
            s3.upload_fileobj(uploaded_file, s3_handle.BUCKET_NAME, new_filename)
            file = banco.File(original_filename=uploaded_file.filename, filename=new_filename,
                bucket=s3_handle.BUCKET_NAME, region=s3_handle.AWS_S3_REGION)
            filesDAO.insert_file(file)
            userDAO.link_to_file(user_id=id, file=file)
        except Exception as ex: 
            flash(f"Erro no upload! {str(ex)}")
            return redirect(url_for('upload_page', id=id))

        return redirect(url_for("upload_page", id=id))

    files = userDAO.list_all_files(id)
    return render_template("upload.html", files=files, id=id)

@app.route("/usuarios/<int:id>/imagens", methods=["GET"])
def lista_imagens_usuario(id):
    if 'username' not in session or id != session['user_id']:
        return redirect(url_for('login'))

    imagens_usuario = userDAO.list_all_files(id)
    if not imagens_usuario: 
        flash('Nenhum arquivo cadastrado!')
        return redirect(url_for('home_page'))

    return render_template("imagens_usuario.html", imagens=imagens_usuario, id=id)

# Recupera os bytes de uma imagem do bucket S3
def get_image_bytes(image_url):
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    return response.content

# Rota que recupera os bytes da imagem e guarda em um formato base64
# para exibir o conteudo na pagina image_form
@app.route("/usuarios/<int:id>/myimage/<nome>")
def show_image(id, nome):
    if 'username' not in session or id != session['user_id']:
        return redirect(url_for('login'))

    image_url = s3_handle.BUCKET_PATH + "/" + nome
    image_bytes = get_image_bytes(image_url)
    extensao = utilidades.get_file_extension(nome)

    encoded_bytes = base64.b64encode(image_bytes).decode('utf-8')  # Encode as base64 and decode for URI
    image_data_uri = f"data:image/{extensao};base64,{encoded_bytes}"

    return render_template("image_view.html", image_data_uri=image_data_uri)

# Recupera os bytes da imagem e guarda em memoria
@app.route("/usuarios/<int:id>/myimage2/<nome>")
def show_image2(nome):
    if 'username' not in session or id != session['user_id']:
        return redirect(url_for('login'))

    image_url = s3_handle.BUCKET_PATH + "/" + nome
    image_bytes = get_image_bytes(image_url)

    extensao = utilidades.get_file_extension(nome)
    my_mimetype = "image" + "/" + extensao
    
    return send_file(io.BytesIO(image_bytes), mimetype=my_mimetype)

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = userDAO.user_by_username(username)
        if not user:
            flash("Usuário não existe, tente novamente.", category='danger')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Senha incorreta, tente novamente.', category='danger') 
            return redirect(url_for('login'))
        msg = 'Usuário logado com sucesso!'
        flash(msg, category='success')
        session['username'] = username
        session['user_id'] = user.id
        return redirect(url_for('home_page'))

    if login_form.errors != {}: #If there are not errors from the validations
        for err_msg in login_form.errors.values():
            flash(f'Existe um erro ao criar o usuário: {err_msg}', category='danger')
    return render_template("login.html", form=login_form)

# Pagina de registro
@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register a new user.
    Validates that the username is not already taken. Hashes the password for security.
    """
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        name = register_form.name.data
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        password2 = register_form.password2.data

        resultado_busca = userDAO.user_by_username(username=username)

        if (resultado_busca):
            error = f"Usuário {username} já registrado."
            flash(error, category='danger')
            return redirect(url_for("register"))

        if password != password2: 
            error = "O password não foi confirmado!" 
            flash(error, category='danger')
            return redirect(url_for("register"))
                
        # the name is available, store it in the database and go to the login page
        hash_and_salted_password = generate_password_hash(password)
        usuario = banco.User(name=name, username=username, email=email, password=hash_and_salted_password)
        userDAO.create_user(user=usuario)
        msg = 'Novo usuário criado com sucesso!'
        flash(msg, category='success')

        return redirect(url_for("login"))

    if register_form.errors != {}:
        for err_msg in register_form.errors.values():
            flash(f'Existe um erro ao criar o usuário: {err_msg}', category='danger')
            return redirect(url_for("register"))

    return render_template("register.html", form=register_form)

@app.route('/logout') 
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)