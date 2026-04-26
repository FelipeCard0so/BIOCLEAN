import os
import subprocess
import shutil


class Cleaner:
    STEPS = [
        ("clean_temp",           "Limpando temporários...",        15),
        ("clean_recent",         "Limpando arquivos recentes...",   5),
        ("clean_cache",          "Limpando cache de rede...",      10),
        ("clean_prefetch",       "Limpando Prefetch...",           10),
        ("clean_windows_update", "Limpando Windows Update...",     20),
        ("clean_logs",           "Limpando logs do sistema...",    10),
        ("clean_minidump",       "Limpando Minidump...",            5),
        ("clean_disk",           "Executando limpeza de disco...", 10),
        ("optimize_disk",        "Otimizando disco...",            15),
    ]

    def __init__(self, logger=None, on_progress=None):
        self.logger = logger
        self.on_progress = on_progress
        self._bytes_freed = 0

    def log(self, message):
        if self.logger:
            self.logger(message)

    def _notify_progress(self, percent):
        if self.on_progress:
            self.on_progress(min(percent, 100))

    def run_command(self, command):
        try:
            subprocess.run(
                command, shell=True, check=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.log(f"[OK] {command}")
        except subprocess.CalledProcessError:
            self.log(f"[ERRO] {command}")

    def _folder_size(self, path):
        total = 0
        if not os.path.exists(path):
            return 0
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except Exception:
                    pass
        return total

    def delete_folder_contents(self, path):
        if not os.path.exists(path):
            return

        freed = self._folder_size(path)

        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass
            for directory in dirs:
                try:
                    shutil.rmtree(os.path.join(root, directory), ignore_errors=True)
                except Exception:
                    pass

        self._bytes_freed += freed
        self.log(f"[OK] Limpo: {path}")

    # ── etapas individuais ──────────────────────────────────────────────────

    def clean_temp(self):
        self.delete_folder_contents(os.getenv("TEMP"))
        self.delete_folder_contents(os.path.join(os.getenv("LOCALAPPDATA"), "Temp"))
        self.delete_folder_contents("C:\\Windows\\Temp")

    def clean_recent(self):
        recent = os.path.join(
            os.getenv("APPDATA"), "Microsoft", "Windows", "Recent"
        )
        if not os.path.exists(recent):
            return

        for f in os.listdir(recent):
            if f.lower() in ("automaticdestinations", "customdestinations"):
                continue
            full_path = os.path.join(recent, f)
            try:
                self._bytes_freed += os.path.getsize(full_path)
                os.remove(full_path)
            except Exception:
                pass

        self.log(f"[OK] Limpo: {recent}")

    def clean_cache(self):
        self.run_command("ipconfig /flushdns")

    def clean_disk(self):
        self.run_command("cleanmgr /sagerun:1")

    def clean_prefetch(self):
        self.delete_folder_contents("C:\\Windows\\Prefetch")

    def clean_windows_update(self):
        self.run_command("net stop wuauserv")
        self.delete_folder_contents("C:\\Windows\\SoftwareDistribution\\Download")
        self.run_command("net start wuauserv")

    def clean_logs(self):
        self.delete_folder_contents("C:\\Windows\\Logs\\CBS")
        self.delete_folder_contents("C:\\Windows\\Logs\\DISM")

    def clean_minidump(self):
        self.delete_folder_contents("C:\\Windows\\Minidump")

    def optimize_disk(self):
        self.run_command("defrag /O /U /V")

    # ── runner principal ────────────────────────────────────────────────────

    def run_all(self, include_prefetch=True):
        self._bytes_freed = 0
        accumulated = 0

        steps = [s for s in self.STEPS if include_prefetch or s[0] != "clean_prefetch"]
        total_weight = sum(s[2] for s in steps)

        for method_name, label, weight in steps:
            self.log(label)  # log centralizado aqui — sem duplicatas
            getattr(self, method_name)()
            accumulated += weight
            self._notify_progress(int(accumulated * 100 / total_weight))

        return self._bytes_freed

    def freed_human(self):
        b = self._bytes_freed
        for unit in ["B", "KB", "MB", "GB"]:
            if b < 1024:
                return f"{b:.1f} {unit}"
            b /= 1024
        return f"{b:.1f} TB"