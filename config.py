# importação das bases
from utils.dbconfig import dbconfig
from rich import print as printc
import sys
from getpass import getpass
import random
import string
import hashlib
from rich.console import Console


def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

console = Console()

def config():

    # Criando base de dados
    db = dbconfig()
    cursor = db.cursor()

    printc("[green][+] Criando nova configuração[/green]")

    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc("[red][!] Erro criando db")
        console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] Banco de dados 'pm' criado")


    # Criando tabelas
    query = """CREATE TABLE pm.secrets
    (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"""

    res = cursor.execute(query)

    printc("[green][+][/green] Tabela 'secrets' criada")

    query = """CREATE TABLE pm.entries
    (sitename TEXT NOT NULL, site_url TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"""

    res = cursor.execute(query)
    printc("[green][+][/green] Tabelas 'entries' criada")


    mp=""
    while 1:
        mp = getpass("Escolha um senha mestre: ")
        if mp==getpass("Re-escreva:") and mp!="":
            break
        printc("[yellow][-] Tente novamente [/yellow]")


    # Hasheando a senha mestre
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()


    # Gerando segredo do dispositivo
    ds = generateDeviceSecret()
    printc("[green][+][green] Gerou-se hash de senha mestre")


    # Adicionando eles para a base de dados
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values (%s,%s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Salvo no banco de dados")

    printc("[green][+] Configuração feita![/green]")
    
    db.close()

config()
