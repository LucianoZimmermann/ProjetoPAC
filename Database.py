import pymysql
from pymysql import Error
import streamlit as st

def get_connection():
    try:
        connection = pymysql.connect(
            host="fujama.c1auuo444yeh.us-east-1.rds.amazonaws.com",
            user="root",
            port=3306,
            password="fujama1234",
            database="fujama",
            cursorclass=pymysql.cursors.DictCursor
            host='localhost',
            user='root',
            passwd='1234',
            database='fujama'
        )
        if connection:
            print("Conexão estabelecida com o banco de dados.")
        return connection
    except pymysql.MySQLError as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")
    except Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None

def create_all_tables(connection):
    queries = [
        """
        CREATE TABLE IF NOT EXISTS VETERINARIO (
            IDVETERINARIO INT AUTO_INCREMENT PRIMARY KEY,
            NOME_VET VARCHAR(255) NOT NULL
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
        """,
        """
        CREATE TABLE IF NOT EXISTS ANIMAL (
            IDANIMAL INT AUTO_INCREMENT PRIMARY KEY,
            NOME_ANIMAL VARCHAR(255) NOT NULL,
            SEXO ENUM('M', 'F') NOT NULL,
            RACA VARCHAR(255) NOT NULL,
            PORTE VARCHAR(255) NOT NULL,
            OBS TEXT

        sql_table_veterinario = (
            "CREATE TABLE IF NOT EXISTS VETERINARIO("
            "IDVETERINARIO INT PRIMARY KEY AUTO_INCREMENT,"
            "NOME_VET VARCHAR(100)"
            ")"
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ENDERECO (
            IDENDERECO INT AUTO_INCREMENT PRIMARY KEY,
            CEP VARCHAR(20),
            RUA VARCHAR(255),
            NUMERO VARCHAR(20),
            BAIRRO VARCHAR(255) NOT NULL

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
        """,
        """
        CREATE TABLE IF NOT EXISTS TELEFONE (
            IDTELEFONE INT AUTO_INCREMENT PRIMARY KEY,
            NUMERO VARCHAR(20) NOT NULL

        sql_table_telefone = (
            "CREATE TABLE IF NOT EXISTS TELEFONE("
            "IDTELEFONE INT PRIMARY KEY AUTO_INCREMENT,"
            "NUMERO VARCHAR(17)"
            ")"
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS TUTOR (
            IDTUTOR INT AUTO_INCREMENT PRIMARY KEY,
            NOME_TUTOR VARCHAR(255) NOT NULL,
            ENDERECO_ID INT,
            FOREIGN KEY (ENDERECO_ID) REFERENCES ENDERECO(IDENDERECO)

        sql_table_tutor = (
            "CREATE TABLE IF NOT EXISTS TUTOR("
            "IDTUTOR INT PRIMARY KEY AUTO_INCREMENT,"
            "NOME_TUTOR VARCHAR(100),"
            "ENDERECO_ID INT,"
            "FOREIGN KEY(ENDERECO_ID) REFERENCES ENDERECO(IDENDERECO)"
            ")"
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ATENDIMENTO (
            IDATENDIMENTO INT AUTO_INCREMENT PRIMARY KEY,
            DATA DATE NOT NULL,
            HORA TIME NOT NULL,
            ANIMAL_ID INT,
            VETERINARIO_ID INT,
            ENDERECO_ID INT,
            TUTOR_ID INT,
            TELEFONE_ID INT,
            FOREIGN KEY (ANIMAL_ID) REFERENCES ANIMAL(IDANIMAL),
            FOREIGN KEY (VETERINARIO_ID) REFERENCES VETERINARIO(IDVETERINARIO),
            FOREIGN KEY (ENDERECO_ID) REFERENCES ENDERECO(IDENDERECO),
            FOREIGN KEY (TUTOR_ID) REFERENCES TUTOR(IDTUTOR),
            FOREIGN KEY (TELEFONE_ID) REFERENCES TELEFONE(IDTELEFONE)

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
        """]

        create_table(queries)

def create_table(connection, sql):
    try:
        with connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except pymysql.MySQLError as e:
        st.error(f"Erro ao criar tabelas: {e}")
        connection.rollback()
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

def select_table(connection, query):
    try:
@@ -92,4 +127,4 @@ def select_table(connection, query):
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        st.error(f"Erro ao executar consulta: {e}")
        return None
        return None