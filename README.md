# Ansible SQL Server Query Automation

A V1 automation project that uses **Ansible** to execute read-only SQL queries against **Microsoft SQL Server**.

The project is designed for database administration tasks where a DBA can provide a SQL `SELECT` query and have Ansible validate and execute it securely against SQL Server.

---

## Architecture

```text
                    ┌──────────────────────┐
                    │       User / DBA     │
                    │                      │
                    │   SQL SELECT Query   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Ansible        │
                    │                      │
                    │  Query Validation    │
                    │  SELECT-only check   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Ansible Vault        │
                    │                      │
                    │ Encrypted DB Password│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     pyodbc / ODBC    │
                    │                      │
                    │ ODBC Driver 18       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    SQL Server        │
                    │                      │
                    │ AdventureWorks2022   │
                    │ ansible_reader       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Query Results     │
                    │                      │
                    │ Displayed by Ansible │
                    └──────────────────────┘
