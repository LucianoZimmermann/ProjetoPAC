import streamlit as st
import pymysql
from pymysql import Error


def get_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            passwd='',
            database='fujama'
        )
        if connection:
            print("Conexão estabelecida com o banco de dados.")
        return connection
    except Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None


def create_all_tables(connection):
    if connection is not None:
        sql_table_animal = (
            "CREATE TABLE IF NOT EXISTS ANIMAL("
            "IDANIMAL INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
            "NOME_ANIMAL VARCHAR(100) NOT NULL,"
            "SEXO ENUM('M', 'F') NOT NULL,"
            "ESPECIE ENUM('GATO', 'CACHORRO') NOT NULL,"
            "PORTE ENUM('PEQUENO', 'MEDIO', 'GRANDE') NOT NULL,"
            "CAUSA VARCHAR(255) NOT NULL,"
            "DELETED BOOLEAN NOT NULL DEFAULT FALSE,"
            "OBS VARCHAR(255)"
            ")"
        )

        sql_table_clinica = (
            "CREATE TABLE IF NOT EXISTS CLINICA("
            "IDCLINICA INT PRIMARY KEY AUTO_INCREMENT,"
            "DELETED BOOLEAN NOT NULL DEFAULT FALSE,"
            "NOME_CLINICA VARCHAR(100)"
            ")"
        )

        sql_table_endereco = (
            "CREATE TABLE IF NOT EXISTS ENDERECO("
            "IDENDERECO INT PRIMARY KEY AUTO_INCREMENT,"
            "RUA VARCHAR(255) NOT NULL,"
            "BAIRRO VARCHAR(100)"
            ")"
        )

        sql_table_atendimento = (
            "CREATE TABLE IF NOT EXISTS ATENDIMENTO("
            "IDATENDIMENTO INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
            "DATA DATE NOT NULL,"
            "DELETED BOOLEAN NOT NULL DEFAULT FALSE,"
            "ANIMAL_ID INT NOT NULL,"
            "CLINICA_ID INT NOT NULL,"
            "ENDERECO_ID INT NOT NULL,"
            "FOREIGN KEY (ANIMAL_ID) REFERENCES ANIMAL(IDANIMAL),"
            "FOREIGN KEY (CLINICA_ID) REFERENCES CLINICA(IDCLINICA),"
            "FOREIGN KEY (ENDERECO_ID) REFERENCES ENDERECO(IDENDERECO)"
            ")"
        )



        create_table(connection, sql_table_animal)
        create_table(connection, sql_table_clinica)
        create_table(connection, sql_table_endereco)
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


def select_table(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        st.error(f"Erro ao executar consulta: {e}")
        return None
