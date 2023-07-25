# modulo para pegar comandos usados na chamada do programa
import argparse
from getpass import getpass
# modulo para aplicar sha256
import hashlib
import pyperclip
from rich import print as printc
# importando modulos desenvolvidos nos passos anteriors e salvos na pasta utils
import utils.add
import utils.retrieve
import utils.generate
from utils.dbconfig import dbconfig


parser = argparse.ArgumentParser(description='Description')


parser.add_argument('option', help='(a)dd / (e)xtract / (g)enerate')
parser.add_argument("-s", "--name", help="Nome do site")
parser.add_argument("-u", "--url", help="URL do site")
parser.add_argument("-e", "--email", help="Email")
parser.add_argument("-l", "--login", help="Usuário")
parser.add_argument("--length", help="Tamanho da senha a ser gerada",type=int)
parser.add_argument("-c", "--copy",
action='store_true',
help='Copy password to clipboard')


args = parser.parse_args()


# funcao para validar senha mestre
def inputAndValidateMasterPassword():
    mp = getpass("SENHA MESTRA: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM pm.secrets"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    if hashed_mp != result[0]:
        printc("[red][!] ERRADO! [/red]")
        return None
    
    return [mp,result[1]]


def main():
    if args.option in ["add","a"]:
        if args.name == None or args.url == None or args.login == None:
            if args.name == None:
                printc("[red][!][/red] Nome do site (-s) obrigatório ")
            if args.url == None:
                printc("[red][!][/red] URL do site (-u) obrigatório ")
            if args.login == None:
                printc("[red][!][/red] Usuário do site (-l) obrigatório ")
            return
        
        if args.email == None:
            args.email = ""

        res = inputAndValidateMasterPassword()
        if res is not None:
            utils.add.addEntry(res[0],
            res[1],
            args.name,
            args.url,
            args.email,
            args.login,
            None)

    if args.option in ["extract","e"]:
        res = inputAndValidateMasterPassword()

        search = {}
        if args.name is not None:
            search["sitename"] = args.name
        if args.url is not None:
            search["siteurl"] = args.url
        if args.email is not None:
            search["email"] = args.email
        if args.login is not None:
            search["username"] = args.login
        if res is not None:
            utils.retrieve.retrieveEntries(res[0],
                                            res[1],
                                            search,
                                            decryptPassword = args.copy)
    if args.option in ["generate","g"]:
        if args.length == None:
            printc("[red][+][/red] Escreva o tamanho da senha (--length)")
            return
        if args.name == None or args.url == None or args.login == None:
            if args.name == None:
                printc("[red][!][/red] Nome do site (-s) obrigatório ")
            if args.url == None:
                printc("[red][!][/red] URL do site (-u) obrigatório ")
            if args.login == None:
                printc("[red][!][/red] Usuário do site (-l) obrigatório ")
            return
        if args.email == None:
            args.email = ""
        res = inputAndValidateMasterPassword()
        if res is not None:
            password = utils.generate.generatePassword(args.length)
            utils.add.addEntry(res[0],
            res[1],
            args.name,
            args.url,
            args.email,
            args.login,
            password,
            is_generated=True)
        pyperclip.copy(password)
        printc("[green][+][/green] Senha gerada e copiada")
main()
