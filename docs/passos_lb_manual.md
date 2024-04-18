# Usando uma instância como Proxy Server para a(s) instâncias da Aplicação Web

## 1. No AWS EC2 crie uma instância Linux Ubuntu 22.04

- VPC default
- Grupode de segurança default
- Atualize o repositório de pacotes linux
```bash
sudo apt update
```
- Instale o pacote net-tools
```bash
sudo apt install net-tools
```
- Instale o pacote nmap
```bash
sudo apt install nmap
```

## 2. Instale o Nginx para funcionar como seu Proxy Server

```bash
sudo apt install nginx
```

## 3. Verifique se o serviço do Nginx está funcionando

```bash
sudo systemctl status nginx
```

Mais detalhes em http://nginx.org/en/docs

## 4. Revise o arquivo de configuração em /etc/nginx/nginx.conf

```bash
vim /etc/nginx/nginx.conf
```

## 5. Faça a configuração do Load Balance (LB) 

Você deve inserir pelo menos duas instâncias ativas da webapp. Além disso, deixe a configuração de controle de sessão (ip_hash) pelo proxy server, pois desta forma, para cada sessão de usuário autenticada, o balanceador de carga procura manter as requisições na instância original.

Configuração para guardar a sessão do usuário (Session persistence)

```bash
http {
    upstream mywebapp {
    	ip_hash;
        server IP1:5000; # Instancia 1 do WebApp 
        server IP2:5000; # Instancia 2 do WebApp
    }

    server {
        listen 8000; # Porta do Proxy Server que vai atender pelas requiscicoes das instancias do Web APP

        location / {
            proxy_pass http://mywebapp;
        }
    }
}
```

Mais detalhes em https://nginx.org/en/docs/http/load_balancing.html#nginx_load_balancing_methods
