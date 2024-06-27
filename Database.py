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

        sql_table_silvestre = (
            "CREATE TABLE IF NOT EXISTS SILVESTRE("
            "IDSILVESTRE INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
            "ESPECIE VARCHAR(255) NOT NULL,"
            "BAIRRO VARCHAR(100) NOT NULL,"
            "DATA DATE NOT NULL,"
            "OBS VARCHAR(255),"
            "DELETED BOOLEAN NOT NULL DEFAULT FALSE"
            ")"
        )

        sql_table_anual = (
            "CREATE TABLE IF NOT EXISTS anual("
            "IDANO INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
            "ANO VARCHAR(4) NOT NULL,"
            "ATENDIMENTOS INT NOT NULL,"
            "DELETED BOOLEAN NOT NULL DEFAULT FALSE"
            ")"
        )

        sql_table_mes = (
            "CREATE TABLE IF NOT EXISTS mes("
            "IDMES INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
            "CLINICA_ID INT NOT NULL,"
            "MOMENT DATE NOT NULL,"
            "DELETED BOOLEAN NOT NULL DEFAULT FALSE,"
            "ATENDIMENTOS_CAO INT NOT NULL,"
            "ATENDIMENTOS_GATO INT NOT NULL,"
            "FOREIGN KEY (CLINICA_ID) REFERENCES CLINICA(IDCLINICA)"
            ")"
        )

        create_table(connection, sql_table_animal)
        create_table(connection, sql_table_clinica)
        create_table(connection, sql_table_endereco)
        create_table(connection, sql_table_atendimento)
        create_table(connection, sql_table_silvestre)
        create_table(connection, sql_table_anual)
        create_table(connection, sql_table_mes)
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

def soft_delete_record_silvestre(connection, table_name, record_id):
    try:
        cursor = connection.cursor()
        delete_sql = f"UPDATE {table_name} SET DELETED = TRUE WHERE IDSILVESTRE = %s"
        print(f"Registro com ID {record_id} marcado como deletado na tabela {table_name}.")
        cursor.execute(delete_sql, (record_id,))
        connection.commit()
    except Error as e:
        print(f"Erro ao marcar registro como deletado na tabela {table_name}: {e}")
    finally:
        if cursor:
            cursor.close()

def soft_delete_record_atendimento(connection, table_name, record_id):
    try:
        cursor = connection.cursor()
        delete_sql = f"UPDATE {table_name} SET DELETED = TRUE WHERE IDATENDIMENTO = %s"
        print(f"Registro com Ano {record_id} marcado como deletado na tabela {table_name}.")
        cursor.execute(delete_sql, (record_id,))
        connection.commit()
    except Error as e:
        print(f"Erro ao marcar registro como deletado na tabela {table_name}: {e}")
    finally:
        if cursor:
            cursor.close()

def soft_delete_record_anual(connection, table_name, record_id):
    try:
        cursor = connection.cursor()
        delete_sql = f"UPDATE {table_name} SET DELETED = TRUE WHERE ANO = %s"
        print(f"Registro com ANO {record_id} marcado como deletado na tabela {table_name}.")
        cursor.execute(delete_sql, (record_id,))
        connection.commit()
    except Error as e:
        print(f"Erro ao marcar registro como deletado na tabela {table_name}: {e}")
    finally:
        if cursor:
            cursor.close()
