<img width="521" height="613" alt="image" src="https://github.com/user-attachments/assets/9181ecf1-1cbb-46e2-82cc-ca4b0c4b8dbd" />


# 🧹 BioClean

> Limpeza inteligente para Windows — libere espaço e deixe seu PC mais rápido com um único clique.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green?style=flat-square&logo=qt)
![Windows](https://img.shields.io/badge/Windows-10%2F11-lightblue?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📸 Preview

> Interface limpa, moderna e intuitiva — feita para qualquer pessoa usar sem dificuldade.

---

## ✨ Funcionalidades

| Recurso | Descrição |
|---|---|
| ⚡ Limpeza Completa | Remove temporários, cache, prefetch, logs e lixo do Windows Update |
| 🛡 Sem Prefetch | Mesma limpeza, preservando o Prefetch para sistemas mais sensíveis |
| 📊 Barra de progresso | Acompanhe cada etapa em tempo real |
| 💾 Espaço liberado | Exibe exatamente quantos MB/GB foram recuperados |
| 📄 Log no Desktop | Salva um relatório completo da limpeza com timestamp |
| 🔒 Elevação automática | Solicita permissão de administrador automaticamente |
| 🎬 Splash Screen | Tela de abertura animada com identidade visual própria |

---

## 🗂 Estrutura do Projeto

```
BioClean/
│
├── main.py          # Entrada do app, splash screen e controle de admin
├── cleaner.py       # Lógica de limpeza, cálculo de espaço e progresso
├── ui.py            # Interface gráfica (PySide6)
├── utils.py         # Funções auxiliares (admin, paths, log)
└── assets/
    ├── splash.gif   # Animação de abertura
    └── icone.ico    # Ícone do aplicativo
```

---

## 🧰 O que é limpo

- ✅ Arquivos temporários do usuário e do sistema (`%TEMP%`, `C:\Windows\Temp`)
- ✅ Histórico de arquivos recentes (preservando atalhos fixados)
- ✅ Cache DNS (`ipconfig /flushdns`)
- ✅ Prefetch do Windows
- ✅ Cache do Windows Update (`SoftwareDistribution\Download`)
- ✅ Logs do sistema (`CBS`, `DISM`)
- ✅ Minidumps de travamentos
- ✅ Limpeza de disco (`cleanmgr`)
- ✅ Otimização de disco (`defrag`)

---

## 🚀 Como executar

### Pré-requisitos

- Python 3.10+
- Dependências:

```bash
pip install PySide6
```

### Rodando em desenvolvimento

```bash
python main.py
```

> O app solicita permissão de administrador automaticamente.

---

## 📦 Gerando o executável

```bash
pyinstaller --onedir --noconsole --icon=assets/icone.ico --name BioClean --add-data "assets;assets" main.py
```

O executável final estará em `dist\BioClean\BioClean.exe`.  
Para distribuir, compacte a pasta `dist\BioClean\` inteira em `.zip`.

---

## 🖥 Compatibilidade

| Sistema | Suporte |
|---|---|
| Windows 10 | ✅ |
| Windows 11 | ✅ |
| macOS / Linux | ❌ (exclusivo Windows) |

---

## 👨‍💻 Autor

Desenvolvido por **Felipe Cardoso**

[![GitHub](https://img.shields.io/badge/GitHub-Felipe-black?style=flat-square&logo=github)](https://github.com/seu-usuario)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
