import os
import sys
import ctypes
import datetime


def asset(relative_path):
    """Resolve caminhos de assets tanto no dev quanto no exe compilado."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


def is_admin():
    """Verifica se está rodando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def relaunch_as_admin():
    """Reinicia o script como administrador."""
    script = os.path.abspath(sys.argv[0])
    params = f'"{script}"'

    result = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 1
    )

    if result > 32:
        sys.exit(0)


def get_desktop_path():
    """Retorna o caminho da área de trabalho."""
    return os.path.join(os.path.expanduser("~"), "Desktop")


def generate_log_filename():
    """Gera nome de log com timestamp."""
    now = datetime.datetime.now()
    return f"BioClean_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"