import Database as db
from Database import *
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    st.title("🐾 Rede de Atenção Animal")

with col3:
    st.write("")

connection = get_connection()

if connection is None:
    st.error("Erro ao conectar com o banco de dados. Verifique as configurações e tente novamente.")
else:
    db.create_all_tables(connection)

bairrosJgua = [
    "Água Verde", "Águas Claras", "Amizade", "Barra do Rio Cerro", "Barra do Rio Molha",
    "Boa Vista", "Braço Ribeirão Cavalo", "Centenário", "Centro", "Chico de Paulo",
    "Czerniewicz", "Estrada Nova", "Ilha da Figueira", "Jaraguá 84", "Jaraguá 99",
    "Jaraguá Esquerdo", "João Pessoa", "Nereu Ramos", "Nova Brasília",
    "Rau", "Ribeirão Cavalo", "Rio Cerro I", "Rio Cerro II", "Rio da Luz",
    "Rio Molha", "Santa Luzia", "Santo Antônio", "São Luís",
    "Tifa Martins", "Tifa Monos", "Três Rios do Norte", "Três Rios do Sul", "Vieira",
    "Vila Baependi", "Vila Lalau", "Vila Lenzi", "Vila Nova"
]

causas = ["Atropelamento", "Miiase", "Dermatite", "Tumor", "Lesão Ocular", "Lesões de Pele Ulcerada", "Outros"]

def get_clinicas():
    with connection.cursor() as cursor:
        cursor.execute("SELECT NOME_CLINICA FROM CLINICA")
        return [cli[0] for cli in cursor.fetchall()]

global clinicas
clinicas = get_clinicas()

def main():

    page = option_menu(
        "Navegação",
        ["Página Inicial", "Programa Emergencial Cães e Gatos"],
        icons=['house', 'check'],
        menu_icon="globe",
        default_index=0,
        orientation="vertical"
    )

    if page == "Página Inicial":
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("")

        with col2:
            st.write("Bem-vindo à Página Inicial do Fujama")
            st.image("https://assets.infra.grancursosonline.com.br/projeto/fujama-sc-1685036431.jpg")

        with col3:
            st.write("")

    elif page == "Programa Emergencial Cães e Gatos":

        subpage = option_menu(
            "Atendimento Emergencial",
            ["Cadastrar Atendimento"],
            icons=['house', 'check', 'check'],
            menu_icon="menu",
            default_index=0,
            orientation="vertical"
        )

        if subpage == "Cadastrar Atendimento":
            st.title("Cadastrar Atendimento")
            with st.form("atendimento_form"):
                st.subheader("Cadastrar Animal")
                nomeAnimal = st.text_input(label="Nome do Animal", key="nomeAnimal")
                sexo = st.selectbox(label="Sexo [Obrigatório]", options=["M", "F"], key="sexo")
                especie = st.selectbox(label="Espécie [Obrigatório]", options=["CACHORRO", "GATO"], key="especie")
                porte = st.selectbox(label="Porte [Obrigatório]", options=["PEQUENO", "MÉDIO", "GRANDE"], key="porte")
                obs = st.text_area(label="Observações", key="obs")

                st.subheader("Motivo do Atendimento")
                causa = st.selectbox(label="Causas [Obrigatório]", options=causas, key="causa")

                st.subheader("Cadastrar Clínica")
                clinica_choice = st.selectbox(
                    label="Nome da Clínica [Obrigatório]",
                    options=["Selecionar existente"] + clinicas
                )

                if clinica_choice == "Selecionar existente":
                    nomeClinica = st.text_input("Nome da nova clínica", key="nomeNovaClinica")
                    cadastrar_nova_clinica = True
                else:
                    nomeClinica = clinica_choice
                    cadastrar_nova_clinica = False

                st.subheader("Local da Ocorrência")
                rua = st.text_input(label="Rua")
                bairro = st.selectbox(label="Bairro [Obrigatório]", options=bairrosJgua, key="bairro")

                st.subheader("Data do Atendimento")
                data_atendimento = st.date_input("Data do Atendimento [Obrigatório]", key="data_atendimento")

                submit = st.form_submit_button("Salvar")

                if submit:
                    if all([sexo, especie, porte, nomeClinica, causa, bairro]):
                        try:
                            with connection.cursor() as cursor:
                                if cadastrar_nova_clinica:
                                    cursor.execute("INSERT INTO CLINICA (NOME_CLINICA) VALUES (%s)", (nomeClinica,))
                                    connection.commit()
                                    cli_id = cursor.lastrowid
                                    clinicas.append(nomeClinica)
                                else:
                                    cursor.execute("SELECT IDCLINICA FROM CLINICA WHERE NOME_CLINICA = %s",
                                                   (nomeClinica,))
                                    result = cursor.fetchone()
                                    if result:
                                        cli_id = result[0]
                                    else:
                                        st.error("Erro: Clínica selecionada não encontrada.")
                                        cli_id = None

                                if cli_id:
                                    animal_sql = "INSERT INTO ANIMAL (NOME_ANIMAL, SEXO, ESPECIE, PORTE, CAUSA, OBS) VALUES (%s, %s, %s, %s, %s, %s)"
                                    animal_params = (nomeAnimal, sexo, especie, porte, causa, obs)
                                    cursor.execute(animal_sql, animal_params)
                                    animal_id = cursor.lastrowid

                                    endereco_sql = "INSERT INTO ENDERECO (RUA, BAIRRO) VALUES (%s, %s)"
                                    bairro_params = (rua, bairro)
                                    cursor.execute(endereco_sql, bairro_params)
                                    endereco_id = cursor.lastrowid

                                    atendimento_sql = "INSERT INTO ATENDIMENTO (DATA, ANIMAL_ID, CLINICA_ID, ENDERECO_ID) VALUES (%s, %s, %s, %s)"
                                    atendimento_params = (data_atendimento, animal_id, cli_id, endereco_id)
                                    cursor.execute(atendimento_sql, atendimento_params)
                                    connection.commit()
                                    st.success("Atendimento cadastrado com sucesso!")
                        except Exception as e:
                            connection.rollback()
                            st.error(f"Erro ao inserir dados no banco de dados: {e}")
                    else:
                        st.warning("Por favor, preencha todos os campos obrigatórios.")

if __name__ == "__main__":
    main()
