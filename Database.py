import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='fujama'
        )
        if connection.is_connected():
            print("Conexão estabelecida com o banco de dados.")
        return connection
    except Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return -1

def create_all_tables(connection):
    if connection is not None:

        sql_table_animal = (
            "CREATE TABLE IF NOT EXISTS ANIMAL("
            "IDANIMAL INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
            "NOME_ANIMAL VARCHAR(100) NOT NULL,"
            "SEXO ENUM('M', 'F') NOT NULL,"
            "RACA ENUM('GATO', 'CACHORRO') NOT NULL,"
            "PORTE ENUM('PEQUENO', 'MEDIA', 'GRANDE') NOT NULL,"
            "OBS VARCHAR(200)"
            ")"
        )

        sql_table_veterinario = (
            "CREATE TABLE IF NOT EXISTS VETERINARIO("
            "IDVETERINARIO INT PRIMARY KEY AUTO_INCREMENT,"
            "NOME_VET VARCHAR(100)"
            ")"
        )

        sql_table_endereco = (
            "CREATE TABLE IF NOT EXISTS ENDERECO("
            "IDENDERECO INT PRIMARY KEY AUTO_INCREMENT,"
            "CEP VARCHAR(9),"
            "RUA VARCHAR(100),"
            "NUMERO VARCHAR(6),"
            "BAIRRO VARCHAR(100),"
            "CIDADE VARCHAR(100),"
            "ESTADO CHAR(2)"
            ")"
        )

        sql_table_telefone = (
            "CREATE TABLE IF NOT EXISTS TELEFONE("
            "IDTELEFONE INT PRIMARY KEY AUTO_INCREMENT,"
            "NUMERO VARCHAR(17)"
            ")"
        )

        sql_table_tutor = (
            "CREATE TABLE IF NOT EXISTS TUTOR("
            "IDTUTOR INT PRIMARY KEY AUTO_INCREMENT,"
            "NOME_TUTOR VARCHAR(100),"
            "ENDERECO_ID INT,"
            "FOREIGN KEY(ENDERECO_ID) REFERENCES ENDERECO(IDENDERECO)"
            ")"
        )

        sql_table_atendimento = (
            "CREATE TABLE IF NOT EXISTS ATENDIMENTO("
            "IDATENDIMENTO INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
            "DATA DATE NOT NULL,"
            "HORA TIME NOT NULL,"
            "ANIMAL_ID INT NOT NULL,"
            "VETERINARIO_ID INT NOT NULL,"
            "ENDERECO_ID INT NOT NULL,"
            "TUTOR_ID INT NOT NULL,"
            "TELEFONE_ID INT NOT NULL,"
            "FOREIGN KEY (ANIMAL_ID) REFERENCES ANIMAL(IDANIMAL),"
            "FOREIGN KEY (VETERINARIO_ID) REFERENCES VETERINARIO(IDVETERINARIO),"
            "FOREIGN KEY (ENDERECO_ID) REFERENCES ENDERECO(IDENDERECO),"
            "FOREIGN KEY (TUTOR_ID) REFERENCES TUTOR(IDTUTOR),"
            "FOREIGN KEY (TELEFONE_ID) REFERENCES TELEFONE(IDTELEFONE)"
            ")"
        )

        create_table(connection, sql_table_animal)
        create_table(connection, sql_table_veterinario)
        create_table(connection, sql_table_endereco)
        create_table(connection, sql_table_telefone)
        create_table(connection, sql_table_tutor)
        create_table(connection, sql_table_atendimento)
        print("Tabelas criadas com sucesso!")

def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        print(f"Error while creating table: {e}")
    finally:
        if cursor:
            cursor.close()


def insert_into_table(connection, sql, params):
    try:
        cursor = connection.cursor()

        cursor.execute(sql, params)

        connection.commit()

        print("Dados inseridos com sucesso!")
    except Error as e:
        print(f"Erro ao inserir dados: {e}")
        raise
    finally:
        if cursor:
            cursor.close()