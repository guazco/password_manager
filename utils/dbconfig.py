# importação das bases
import mysql.connector
from rich import print as printc
from rich.console import Console


console = Console()


# Configuração da conexão
def dbconfig():
    try:
        db = mysql.connector.connect(
                    host ="localhost",
                    user ="pm",
                    passwd ="password"
                    )
    # Conexão com erro
    except Exception as e:
        printc("[red][!] Houve um erro ao conectar com a base[/red]")
        console.print_exception(show_locals=True)
    return db
