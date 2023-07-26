""" My personal Telegram BOT usyng python language. """

############################################################# CREDITS ##############################################################
# MY PERSONAL BOT TELEGRAM
# Developed by Leonardo Travagini Delboni
# Version 1.0 - Since July 2023
#####################################################################################################################################

############################
# LIBRARIES AND IMPORTINGS #
############################

# Libraries and modules:
import pandas as pd
import sys
import warnings
import os
import logging
import datetime
import telebot
import setproctitle
from typing import List

# Common folder settings:
from config import common_path
sys.path.insert(0, common_path)

# Importings from common folder:
from functions import record, bot_telegram_sendtext, get_db
from settings import warning_telegram_id, telegram_token

################################
# LOGGING AND WARNING SETTINGS #
################################

# Turning off the iloc and mixed types in the same column warnings:
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)

# Turning off the chained assignment warnings:
pd.options.mode.chained_assignment = None

# Setting the logging file:
log_files = 'logging'
filename = os.path.basename(__file__)
nome_arquivo, extensao_arquivo = os.path.splitext(filename)

# Creating the logging folder if not exists:
if not os.path.exists(log_files):
    os.makedirs(log_files)

# Removing the default logging (avoidind future logging handlers warnings):
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Setting the logging format:
format_logging = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
logging.basicConfig(level = logging.INFO, filename = f'{log_files}/{nome_arquivo}.log', format = format_logging)

################################
# MAIN FUNCTION - MAIN PROGRAM #
################################

# Main function:
def bot_telegram_main():

    # Recording the start time:
    full_moment = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    bot_telegram_sendtext(f'BOT TELEGRAM START: {full_moment}', warning_telegram_id)
    record(f'--- STARTING THE TELEGRAM BOT - {full_moment} ---', 'yellow')

    # Importing bot_token:
    bot = telebot.TeleBot(telegram_token)

    # Getting the full data from the database:
    df_full, status = get_db('tbl_graduacao_gratuita')
    if df_full.empty or not status:
        record(f'ERROR - Dataframe is coming empty!', 'red')
        return False
    else:
        data_extracao = df_full['data_ref'].unique()[0]
        data_extracao = data_extracao.strftime("%d/%m/%Y")
        df_full = df_full[['nome_curso', 'grau', 'modalidade', 'sigla', 'instituicao']]
        df_full = df_full.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)

    # Checking the xlsx folder:
    xlsx_files_folder_name = 'xlsx_files'
    if not os.path.exists(xlsx_files_folder_name):
        os.makedirs(xlsx_files_folder_name)

    # Menu to return to the main menu:
    @bot.message_handler(commands=['Menu'])
    def return_menu(message):
        menu(message)

    # Filtering by bachelor's degree on-site courses:
    @bot.message_handler(commands=['Bacharelado_Presencial'])
    def bacharelado_presencial(message):
        df_bacharelado_presencial = df_full.copy()
        df_bacharelado_presencial = df_bacharelado_presencial[df_bacharelado_presencial['grau'] == 'Bacharelado']
        df_bacharelado_presencial = df_bacharelado_presencial[df_bacharelado_presencial['modalidade'] == 'Presencial']
        df_bacharelado_presencial = df_bacharelado_presencial.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Bacharelado Presencial gratuitos no Brasil.""".format(len(df_bacharelado_presencial)))
        df_bacharelado_presencial.to_excel(f'{xlsx_files_folder_name}/bacharelado_presencial.xlsx', index=False)
        bot.send_document(message.chat.id, open(f'{xlsx_files_folder_name}/bacharelado_presencial.xlsx', 'rb'))
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Filtering by bachelor's degree online courses:
    @bot.message_handler(commands=['Bacharelado_Distancia'])
    def bacharelado_distancia(message):
        df_bacharelado_distancia = df_full.copy()
        df_bacharelado_distancia = df_bacharelado_distancia[df_bacharelado_distancia['grau'] == 'Bacharelado']
        df_bacharelado_distancia = df_bacharelado_distancia[df_bacharelado_distancia['modalidade'] == 'A Distância']
        df_bacharelado_distancia = df_bacharelado_distancia.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Bacharelado À Distância gratuitos no Brasil.""".format(len(df_bacharelado_distancia)))
        df_bacharelado_distancia.to_excel(f'{xlsx_files_folder_name}/bacharelado_distancia.xlsx', index=False)
        bot.send_document(message.chat.id, open(f'{xlsx_files_folder_name}/bacharelado_distancia.xlsx', 'rb'))
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Filtering by bachelor's degree courses:
    @bot.message_handler(commands=['Bacharelado'])
    def bacharelado(message):
        df_bacharelado = df_full.copy()
        df_bacharelado = df_bacharelado[df_bacharelado['grau'] == 'Bacharelado']
        df_bacharelado = df_bacharelado.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Bacharelado gratuitos no Brasil.""".format(len(df_bacharelado)))
        bot.send_message(message.chat.id, """Vamos agora filtrar por modalidade:
\n/Bacharelado_Presencial
/Bacharelado_Distancia""")

    # Filtering by associate's degree on-site courses:
    @bot.message_handler(commands=['Licenciatura_Presencial'])
    def licenciatura_presencial(message):
        df_licenciatura_presencial = df_full.copy()
        df_licenciatura_presencial = df_licenciatura_presencial[df_licenciatura_presencial['grau'] == 'Licenciatura']
        df_licenciatura_presencial = df_licenciatura_presencial[df_licenciatura_presencial['modalidade'] == 'Presencial']
        df_licenciatura_presencial = df_licenciatura_presencial.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Licenciatura Presencial gratuitos no Brasil.""".format(len(df_licenciatura_presencial)))
        df_licenciatura_presencial.to_excel(f'{xlsx_files_folder_name}/licenciatura_presencial.xlsx', index=False)
        bot.send_document(message.chat.id, open(f'{xlsx_files_folder_name}/licenciatura_presencial.xlsx', 'rb'))
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Filtering by associate's online degree courses:
    @bot.message_handler(commands=['Licenciatura_Distancia'])
    def licenciatura_distancia(message):
        df_licenciatura_distancia = df_full.copy()
        df_licenciatura_distancia = df_licenciatura_distancia[df_licenciatura_distancia['grau'] == 'Licenciatura']
        df_licenciatura_distancia = df_licenciatura_distancia[df_licenciatura_distancia['modalidade'] == 'A Distância']
        df_licenciatura_distancia = df_licenciatura_distancia.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Licenciatura À Distância gratuitos no Brasil.""".format(len(df_licenciatura_distancia)))
        df_licenciatura_distancia.to_excel(f'{xlsx_files_folder_name}/licenciatura_distancia.xlsx', index=False)
        bot.send_document(message.chat.id, open(f'{xlsx_files_folder_name}/licenciatura_distancia.xlsx', 'rb'))
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Filtering by associate's degree courses:
    @bot.message_handler(commands=['Licenciatura'])
    def licenciatura(message):
        df_licenciatura = df_full.copy()
        df_licenciatura = df_licenciatura[df_licenciatura['grau'] == 'Licenciatura']
        df_licenciatura = df_licenciatura.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Licenciatura gratuitos no Brasil.""".format(len(df_licenciatura)))
        bot.send_message(message.chat.id, """Vamos agora filtrar por modalidade:
\n/Licenciatura_Presencial
/Licenciatura_Distancia""")

    # Filtering by technical's degree on-site courses:
    @bot.message_handler(commands=['Tecnologico_Presencial'])
    def tecnologico_presencial(message):
        df_tecnologico_presencial = df_full.copy()
        df_tecnologico_presencial = df_tecnologico_presencial[df_tecnologico_presencial['grau'] == 'Tecnológico']
        df_tecnologico_presencial = df_tecnologico_presencial[df_tecnologico_presencial['modalidade'] == 'Presencial']
        df_tecnologico_presencial = df_tecnologico_presencial.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Tecnológico Presencial gratuitos no Brasil.""".format(len(df_tecnologico_presencial)))
        df_tecnologico_presencial.to_excel(f'{xlsx_files_folder_name}/tecnologico_presencial.xlsx', index=False)
        bot.send_document(message.chat.id, open(f'{xlsx_files_folder_name}/tecnologico_presencial.xlsx', 'rb'))
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Filtering by technical's online degree courses:
    @bot.message_handler(commands=['Tecnologico_Distancia'])
    def tecnologico_distancia(message):
        df_tecnologico_distancia = df_full.copy()
        df_tecnologico_distancia = df_tecnologico_distancia[df_tecnologico_distancia['grau'] == 'Tecnológico']
        df_tecnologico_distancia = df_tecnologico_distancia[df_tecnologico_distancia['modalidade'] == 'A Distância']
        df_tecnologico_distancia = df_tecnologico_distancia.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos de Tecnológico À Distância gratuitos no Brasil.""".format(len(df_tecnologico_distancia)))
        df_tecnologico_distancia.to_excel(f'{xlsx_files_folder_name}/tecnologico_distancia.xlsx', index=False)
        bot.send_document(message.chat.id, open(f'{xlsx_files_folder_name}/tecnologico_distancia.xlsx', 'rb'))
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Filtering by technical's degree courses:
    @bot.message_handler(commands=['Tecnologico'])
    def tecnologico(message):
        df_tecnologico = df_full.copy()
        df_tecnologico = df_tecnologico[df_tecnologico['grau'] == 'Tecnológico']
        df_tecnologico = df_tecnologico.drop_duplicates().sort_values(by=['nome_curso', 'instituicao', 'grau']).reset_index(drop=True)
        bot.send_message(message.chat.id, """Existem atualmente {} cursos distintos Tecnológicos gratuitos no Brasil.""".format(len(df_tecnologico)))
        bot.send_message(message.chat.id, """Vamos agora filtrar por modalidade:
\n/Tecnologico_Presencial
/Tecnologico_Distancia""")

    # Option 1 - Data Analysis personal project:
    @bot.message_handler(commands=['Opt1'])
    def option1(message):
        bot.send_message(message.chat.id, """Essa é uma pequena amostra de um projeto pessoal. A base de dados contém todas as graduações gratuitas oficialmente reconhecidas pelo Ministério da Educação (MEC).""")
        bot.send_message(message.chat.id, """Os dados são obtidos diretamente do sistema E-MEC, salvos em máquina virtual VPS, estruturados via PostgreSQL, com posterior manipulação e análise via Python e suas bibliotecas.""")
        bot.send_message(message.chat.id, """Os dados aqui presentes são de {}. Para essa pequena amostra, primeiramente escolha o grau de ensino desejado a filtrar:
\n/Bacharelado
/Licenciatura
/Tecnologico""".format(data_extracao))
    
    # Option 2 - Web Development personal project:
    @bot.message_handler(commands=['Opt2'])
    def option2(message):
        bot.send_message(message.chat.id, """Seguem-se dois pequenos projetos de web desenvolvimento pessoais usando HTML, CSS, JavaScript e PHP.""")
        bot.send_message(message.chat.id, """O primeiro é um site pessoal, com informações sobre mim, meus projetos e meus contatos: https://www.leonardodelboni.com.br""")
        bot.send_message(message.chat.id, """O segundo é uma doação realizaca para a ONG Pequeno Ninja, para a divulgação do projeto e para a arrecadação de doações: https://www.pequenoninja.online""")
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Option 3 - Get my CV in PDF:
    @bot.message_handler(commands=['Opt3'])
    def option3(message):
        bot.send_message(message.chat.id, """Segue abaixo meu CV em PDF:""")
        bot.send_document(message.chat.id, open('/root/main/projects/bot_telegram/Curriculum - Leonardo Travagini Delboni.pdf', 'rb'))
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Getting my Personal Portolfio (Opt4):
    @bot.message_handler(commands=['Meu_Portolio'])
    def meu_portfolio(message):
        bot.send_message(message.chat.id, """Segue abaixo o link para acessar meu Portfólio Pessoal:\nhttps://leonardodelboni.com.br/\n/Menu para voltar ao menu inicial.""")
        bot.send_message(message.chat.id, """/Opt4 para voltar ao menu anterior\n/Menu para voltar ao menu inicial""")
    
    # Getting my Whatsapp (Opt4):
    @bot.message_handler(commands=['Meu_WhatsApp'])
    def meu_whatsapp(message):
        bot.send_message(message.chat.id, """Segue abaixo o link para me contatar via WhatsApp:\nhttps://api.whatsapp.com/send/?phone=5511994421880""")
        bot.send_message(message.chat.id, """/Opt4 para voltar ao menu anterior\n/Menu para voltar ao menu inicial""")
    
    # Getting my LinkedIn (Opt4):
    @bot.message_handler(commands=['Meu_LinkedIn'])
    def meu_linkedin(message):
        bot.send_message(message.chat.id, """Segue abaixo o link do meu LinkedIn:\nhttps://www.linkedin.com/in/leonardo-travagini-delboni-6b8a48bb""")
        bot.send_message(message.chat.id, """/Opt4 para voltar ao menu anterior\n/Menu para voltar ao menu inicial""")

    # Getting my GitHub (Opt4):
    @bot.message_handler(commands=['Meu_GitHub'])
    def meu_github(message):
        bot.send_message(message.chat.id, """Segue abaixo o link do meu GitHub:\nhttps://github.com/leonardo-travagini-delboni""")
        bot.send_message(message.chat.id, """/Opt4 para voltar ao menu anterior\n/Menu para voltar ao menu inicial""")
    
    # Getting my e-mail (Opt4):
    @bot.message_handler(commands=['Meus_emails'])
    def meu_email(message):
        bot.send_message(message.chat.id, """Segue abaixo meu e-mail principal:\nleonardodelboni@gmail.com\nOu caso prefira, segue abaixo meu e-mail acadêmico:\nl172102@dac.unicamp.br""")
        bot.send_message(message.chat.id, """/Opt4 para voltar ao menu anterior\n/Menu para voltar ao menu inicial""")

    # Getting my phone number (Opt4):
    @bot.message_handler(commands=['Meu_Telefone'])
    def meu_telefone(message):
        bot.send_message(message.chat.id, """Segue abaixo meu número de telefone:\n(11) 99442-1880""")
        bot.send_message(message.chat.id, """/Opt4 para voltar ao menu anterior\n/Menu para voltar ao menu inicial""")

    # Option 4 - Get my contact data:
    @bot.message_handler(commands=['Opt4'])
    def option5(message):
        bot.reply_to(message,"""Selecione uma das opcoes abaixo:
\n/Meu_Portolio para acessar meu website pessoal
/Meu_WhatsApp para acessar meu WhatsApp
/Meu_LinkedIn para acessar meu LinkedIn
/Meu_GitHub para acessar meu GitHub
/Meus_emails para acessar meus e-mails
/Meu_Telefone para acessar meu telefone""")
        bot.send_message(message.chat.id, """/Menu para voltar ao menu inicial.""")

    # Welcoming the user:
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, """Bem-vindo(a) ao meu BOT pessoal do Telegram.""")
        menu(message)

    # Menu function:
    @bot.message_handler(func=lambda message: True)
    def menu(message):
        bot.send_message(message.chat.id, """Clique em uma das opções abaixo:
\n/Opt1 Projeto pessoal de Data Analysis
/Opt2 Projetos de Web Development
/Opt3 Obtenha meu CV em PDF
/Opt4 Dados de Contato""")

    # Sending the message:
    record(f'Starting the bot...','yellow')
    bot.polling()

    # Recording the end time:
    full_moment = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    bot_telegram_sendtext(f'BOT TELEGRAM ENDED: {full_moment}', warning_telegram_id)
    record(f'--- FINISHING THE TELEGRAM BOT - {full_moment} ---', 'yellow')

################################
# EXECUTING THE MAIN FUNCTION  #
################################

# Naming process in HTOP (Linux):
setproctitle.setproctitle(f'monitor_bot_telegram')

# Executing the main function:
if __name__ == '__main__':
    bot_telegram_main()
    bot_telegram_sendtext(f'BOT TELEGRAM ENDED: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', warning_telegram_id)
