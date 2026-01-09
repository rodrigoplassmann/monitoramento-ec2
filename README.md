## Sistema de monitoramento de instância EC2
Esse projeto utiliza um script em Python que coleta as informações de CPU(%), RAM(%) e disco(GB) de uma instância EC2 na AWS e envia esses dados para uma API Flask, que grava eles em um banco de dados MySQL.

## Arquitetura do projeto
monitoring-system/

├── api/

│   └── app.py  -> Flask (API)

├── agent/

│   └── collector.py -> coleta métricas

├── scripts/

│   └── cleanup.sh -> apaga dados antigos

├── .env -> Variáveis de ambiente (NUNCA VAI PARA O GIT)

├── .env.example -> arquivo exemplo de variáveis de ambiente

├── .my.cnf  -> arquivo de configuração do cliente MySQL (NUNCA VAI PARA O GIT)

├── .my.cnf.example -> arquivo exemplo de configuração do cliente MySQL

├── .gitignore

├── requirements.txt

└── README.md

## Como rodar o projeto na sua instância:

1. Crie uma instância EC2 na AWS e configure as inbound rules para aceitar conexões na porta 22 (SSH) e 5000 (Flask API)

2. Conecte na sua instância via SSH no terminal indo até o diretório em que está armazenada a chave .pem que foi baixada ao criar a instância
```
ssh -i .\sua-chave.pem ubuntu@ip_da_sua_instancia
```

3. Instalar dependências
```
sudo apt update -y
sudo apt install python3-pip mysql-server git -y
```

4. Clonar o projeto
```
git clone git@github.com:rodrigoplassmann/monitoramento-ec2.git
cd monitoramento-ec2
pip3 install --user -r requirements.txt
```

5. Criar um arquivo .env para configurar suas variáveis de ambiente
```
cp .env.example .env
nano .env
```

```
DB_HOST=DB_HOST_AQUI
DB_USER=DB_USER_AQUI
DB_PASSWORD=DB_PASSWORD_AQUI
DB_NAME=DB_NAME_AQUI
API_URL=API_URL_AQUI
```

6. Criar um arquivo .my.cnf para configuração do seu cliente MySQL
```
cp .my.cnf.example ~/.my.cnf
nano ~/.my.cnf
chmod 600 ~/.my.cnf
```

```
[client]
user=DB_USER_AQUI
password=DB_PASSWORD_AQUI
host=DB_HOST_AQUI
database=DB_NAME_AQUI
```

7. Criar o banco de dados e o usuário com os mesmos usuário, senha, nome do banco e host do arquivo .my.cnf e .env. Nesse exemplo o usuário é monitor, o host é localhost, o nome do banco é monitoramento, e a senha é SenhaMuitoForte123
```
sudo mysql
```

```
CREATE DATABASE monitoramento;

CREATE USER 'monitor'@'localhost' IDENTIFIED BY 'SenhaMuitoForte123';

GRANT ALL PRIVILEGES ON monitoramento.* TO 'monitor'@'localhost';

FLUSH PRIVILEGES;
EXIT;
```

```
mysql -u monitor -p monitoramento
```

```
CREATE TABLE metrics (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cpu FLOAT,
  ram FLOAT,
  disk FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EXIT;
```

8. Configurar o crontab
```
crontab -e
```

Definir de quanto em quanto tempo o collector.py vai coletar as métricas, nesse exemplo de 1 em 1 minuto
```
* * * * * cd /home/ubuntu/monitoramento-ec2 && /usr/bin/python3 agent/collector.py
```

Definir de quanto em quanto em tempo o script cleanup.sh vai limpar o banco de dados, nesse exemplo uma vez por mês, todo dia 1 às 2 da manhã
```
0 2 1 * * cd /home/ubuntu/monitoramento-ec2 && ./cleanup.sh
```

9. Inicializar o sistema de monitoramento
Vá para o diretório api dentro da pasta do projeto
```
cd api
nohup python3 app.py > /dev/null 2>&1 &
```

10. Visualizar os dados através do Flask
Abra um novo terminal e digite:
```
curl localhost:5000/metrics
```

11. Visualizar os dados através do MySQL
Acesse o MySQL com usuário e nome do banco que você criou
```
mysql monitoramento
```

Faça queries para verificar os dados, por exemplo:
```
SELECT * FROM metrics ORDER BY created_at DESC LIMIT 10;
```

12. Como parar de rodar o sistema
```
pkill -f app.py
```
