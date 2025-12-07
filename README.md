# SQLite Blind SQL Injection (Boolean-Based) Lab

Este repositório contém um laboratório de Estudo de Caso sobre **Blind SQL Injection** em um ambiente **Flask + SQLite**.

O projeto demonstra o ciclo completo de uma vulnerabilidade web:
1.  **Vulnerabilidade:** Uma aplicação web insegura suscetível a injeção de SQL via concatenação de strings.
2.  **Exploração:** Um script Python automatizado para extrair dados sensíveis caractere por caractere (técnica Boolean-Based).
3.  **Remediação:** A versão corrigida da aplicação utilizando *Prepared Statements*.

---

## ⚠️ Disclaimer

**Este código foi desenvolvido para fins estritamente educacionais.**
Nunca utilize os scripts de exploração em sistemas que você não possui permissão explícita para testar.

---

## 📂 Estrutura do Projeto

* `vulnerable_app.py`: O servidor Flask contendo a vulnerabilidade de SQL Injection.
* `exploit.py`: Script de ataque que automatiza a extração da senha do admin via inferência (Blind Boolean-based).
* `secure_app.py`: O servidor Flask corrigido, utilizando consultas parametrizadas (Prepared Statements).

---

## 🚀 Como Executar

### Pré-requisitos
Você precisará do Python 3 e das bibliotecas `flask` e `requests`.

```bash
pip install flask requests
```

## 1. Executando o Cenário Vulnerável
Inicie o servidor vulnerável:

```Bash
python3 vulnerable_app.py
```
O servidor iniciará, geralmente em http://192.168.15.9:5000 (conforme configurado no código) ou http://127.0.0.1:5000.

## 2. Executando o Exploit
Em outro terminal, execute o script de ataque. Certifique-se de que o IP no script corresponde ao do servidor:

```Bash
python3 exploit.py
```
Resultado: O script irá iterar sobre os caracteres e extrair a flag flag{Blind_SQLi_Is_Fun_123} baseando-se nas respostas de "Verdadeiro" (Usuário encontrado) ou "Falso" (Usuário não encontrado) do servidor.

## 3. Verificando a Correção
Pare o servidor vulnerável (Ctrl+C) e inicie a versão segura:

```Bash
python3 secure_app.py
```
Tente rodar o exploit.py novamente. Ele falhará em encontrar caracteres, provando que a vulnerabilidade foi mitigada.

# 🧠 Análise Técnica
## A Vulnerabilidade (Unsanitized Input)
No arquivo vulnerable_app.py, a entrada do usuário é concatenada diretamente na query SQL usando f-strings:
```Python
# CÓDIGO INSEGURO
query = f"SELECT * FROM users WHERE username = '{username}'"
```
Isso permite que um atacante feche as aspas (') e injete lógica SQL arbitrária (ex: ' AND 1=1 --).

## O Exploit (Boolean-Based)
Como a aplicação não retorna erros de SQL na tela (Blind), o exploit faz perguntas de "Sim/Não" ao banco de dados injetando condições lógicas:
```SQL
admin' AND (SELECT substr(password, 1, 1) FROM users WHERE username='admin') = 'f' --
```
- Se Verdadeiro: A query retorna o usuário admin e o site exibe "Usuário encontrado".
- Se Falso: A query não retorna nada e o site exibe "Usuário não encontrado".
O script exploit.py automatiza essas perguntas para reconstruir a senha inteira.

## A Correção (Prepared Statements)
No arquivo secure_app.py, utilizamos o recurso nativo do driver SQLite para parametrizar a consulta:
```Python
# CÓDIGO SEGURO
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```
O banco de dados trata a entrada estritamente como dados literais, neutralizando qualquer tentativa de injeção de comandos, pois o input nunca é interpretado como SQL.
