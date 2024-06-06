import Database as db
from Database import *
import streamlit as st

st.set_page_config(layout="wide")
st.title("Fujama - Castrometro")

connection = get_connection()

if connection is None:
    st.error("Erro ao conectar com o banco de dados. Verifique as configurações e tente novamente.")
else:
    db.create_all_tables(connection)

bairrosJgua = [
    "Água Verde", "Águas Claras", "Amizade", "Barra do Rio Cerro", "Barra do Rio Molha",
    "Boa Vista", "Braço Ribeirão Cavalo", "Centenário", "Centro", "Chico de Paulo",
    "Czerniewicz", "Estrada Nova", "Ilha da Figueira", "Jaraguá 84", "Jaraguá 99",
    "Jaraguá Esquerdo", "João Pessoa", "Nereu Ramos", "Nova Brasília", "Parque Malwee",
    "Rau", "Ribeirão Cavalo", "Rio Cerro I", "Rio Cerro II", "Rio da Luz",
    "Rio Molha", "Santa Luzia", "Santo Antônio", "São Luís",
    "Tifa Martins", "Tifa Monos", "Três Rios do Norte", "Três Rios do Sul", "Vieira",
    "Vila Baependi", "Vila Lalau", "Vila Lenzi", "Vila Nova"
]

def get_veterinarios():
    with connection.cursor() as cursor:
        cursor.execute("SELECT NOME_VET FROM VETERINARIO")
        return [vet[0] for vet in cursor.fetchall()]

global veterinarios
veterinarios = get_veterinarios()

def main():
    page = st.sidebar.radio(
        "Navegação",
        options=["Página Inicial", "Cadastrar castração", "Dados", "Filtrar Atendimentos"]
    )

    if page == "Página Inicial":
        st.write("Bem-vindo à Página Inicial do Fujama")
        st.image("https://assets.infra.grancursosonline.com.br/projeto/fujama-sc-1685036431.jpg")

    elif page == "Cadastrar castração":
        st.title("Cadastrar Atendimento")
        with st.form("atendimento_form"):
            st.subheader("Cadastrar Animal")
            nomeAnimal = st.text_input(label="Nome do Animal", key="nomeAnimal")
            sexo = st.selectbox(label="Sexo [Obrigatório]", options=["M", "F"], key="sexo")
            raca = st.selectbox(label="Raça [Obrigatório]", options=["GATO", "CACHORRO"], key="raca")
            porte = st.selectbox(label="Porte [Obrigatório]", options=["PEQUENO", "MÉDIO", "GRANDE"], key="porte")
            obs = st.text_area(label="Observações", key="obs")

            st.subheader("Cadastrar Veterinário")
            veterinario_choice = st.selectbox(
                label="Nome do Veterinário [Obrigatório]",
                options=["Selecionar existente"] + veterinarios
            )

            if veterinario_choice == "Selecionar existente":
                nomeVeterinario = st.text_input("Nome do novo veterinário", key="nomeNovoVeterinario")
                cadastrar_novo_vet = True
            else:
                nomeVeterinario = veterinario_choice
                cadastrar_novo_vet = False

            st.subheader("Cadastrar Endereco")
            cep = st.text_input(label="CEP", key="cep")
            ruaEndereco = st.text_input(label="Rua do Endereco", key="ruaEndereco")
            numeroEndereco = st.text_input(label="Número do Endereco", key="numeroEndereco")
            bairro = st.selectbox(label="Bairro [Obrigatório]", options=bairrosJgua, key="bairro")

            st.subheader("Cadastrar Telefone")
            numeroTelefone = st.text_input(label="Número", key="numeroTelefone")

            st.subheader("Cadastrar Tutor")
            nomeTutor = st.text_input(label="Nome do Tutor", key="nomeTutor")

            st.subheader("Data e Hora do Atendimento")
            data_atendimento = st.date_input("Data do Atendimento [Obrigatório]", key="data_atendimento")
            hora_atendimento = st.time_input("Hora do Atendimento [Obrigatório]", key="hora_atendimento")

            submit = st.form_submit_button("Salvar")

            if submit:
                if all([sexo, raca, porte, nomeVeterinario, bairro]):
                    try:
                        with connection.cursor() as cursor:
                            if cadastrar_novo_vet:
                                cursor.execute("INSERT INTO VETERINARIO (NOME_VET) VALUES (%s)", (nomeVeterinario,))
                                connection.commit()
                                vet_id = cursor.lastrowid
                                veterinarios.append(nomeVeterinario)
                            else:
                                cursor.execute("SELECT IDVETERINARIO FROM VETERINARIO WHERE NOME_VET = %s", (nomeVeterinario,))
                                result = cursor.fetchone()
                                if result:
                                    vet_id = result[0]
                                else:
                                    st.error("Erro: Veterinário selecionado não encontrado.")
                                    vet_id = None

                            if vet_id:
                                animal_sql = "INSERT INTO ANIMAL (NOME_ANIMAL, SEXO, RACA, PORTE, OBS) VALUES (%s, %s, %s, %s, %s)"
                                animal_params = (nomeAnimal, sexo, raca, porte, obs)
                                cursor.execute(animal_sql, animal_params)
                                animal_id = cursor.lastrowid

                                endereco_sql = "INSERT INTO ENDERECO (CEP, RUA, NUMERO, BAIRRO) VALUES (%s, %s, %s, %s)"
                                endereco_params = (cep, ruaEndereco, numeroEndereco, bairro)
                                cursor.execute(endereco_sql, endereco_params)
                                endereco_id = cursor.lastrowid

                                telefone_sql = "INSERT INTO TELEFONE (NUMERO) VALUES (%s)"
                                telefone_params = (numeroTelefone,)
                                cursor.execute(telefone_sql, telefone_params)
                                telefone_id = cursor.lastrowid

                                tutor_sql = "INSERT INTO TUTOR (NOME_TUTOR, ENDERECO_ID) VALUES (%s, %s)"
                                tutor_params = (nomeTutor, endereco_id)
                                cursor.execute(tutor_sql, tutor_params)
                                tutor_id = cursor.lastrowid

                                atendimento_sql = "INSERT INTO ATENDIMENTO (DATA, HORA, ANIMAL_ID, VETERINARIO_ID, ENDERECO_ID, TUTOR_ID, TELEFONE_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                atendimento_params = (data_atendimento, hora_atendimento, animal_id, vet_id, endereco_id, tutor_id, telefone_id)
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


