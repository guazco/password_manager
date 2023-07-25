# importando bibliotecas
# modulo de configuracao da base
from utils.dbconfig import dbconfig
# modulo de funcoes uteis do aes
import utils.aesutil
# importando getpass para esconder a senha ao digitar
from getpass import getpass
# importando biblioteca de criptografia
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64
from rich import print as printc
from rich.console import Console


# calculo da chave mestra
def computeMasterKey(mp,ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


# checando entrada
def checkEntry(sitename, siteurl, email, username):
    db = dbconfig()
    cursor = db.cursor()
    query = f"SELECT * FROM pm.entries WHERE sitename = '{sitename}' AND site_url = '{siteurl}' AND email = '{email}' AND username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results)!=0:
        return True
    return False



# adicionando entrada
def addEntry(mp, ds, sitename, siteurl, email, username):

    # Checa se entrada ja existe
    if checkEntry(sitename, siteurl, email, username):
        printc("[yellow][-][/yellow] Já existem esses dados")
        return

    # Checa senha
    password = getpass("Senha: ")

    # Calcula chave mestre
    mk = computeMasterKey(mp,ds)

    # Criptografa senha com chave mestra
    encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType="bytes")

    # Adiciona a base
    db = dbconfig()
    cursor = db.cursor()

    query = """INSERT INTO pm.entries (sitename,
    site_url,
    email,
    username,
    password) values (%s, %s, %s, %s, %s)"""

    val = (sitename,siteurl,email,username,encrypted)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Entrada salva")