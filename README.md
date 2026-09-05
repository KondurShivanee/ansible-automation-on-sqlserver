# Ansible SQL Server Query Automation

A V1/V1.1 automation project that uses **Ansible** to execute read-only SQL queries against **Microsoft SQL Server** and export the results to Excel.

The project is designed for database administration tasks where a DBA can provide a SQL `SELECT` query and have Ansible validate and execute it securely against SQL Server.

---

## Project Overview

This project demonstrates how Ansible can be used to automate SQL Server database operations while applying basic security and least-privilege principles.

The automation accepts a SQL `SELECT` query, validates the query, executes it against SQL Server using a dedicated read-only account, displays the results, and exports the results to an Excel workbook.

---

## Architecture

```text
                    ┌──────────────────────┐
                    │      User / DBA      │
                    │                      │
                    │    SQL SELECT Query  │
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
                    │    Ansible Vault     │
                    │                      │
                    │ Encrypted DB Password│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ODBC Driver 18     │
                    │      + pyodbc        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     SQL Server       │
                    │                      │
                    │  AdventureWorks2022  │
                    │   ansible_reader     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Query Results     │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ Ansible Terminal │   │ Python +          │
          │ Output           │   │ openpyxl          │
          └──────────────────┘   └────────┬─────────┘
                                          │
                                          ▼
                                ┌──────────────────┐
                                │ query_results.xlsx│
                                └──────────────────┘
```

---

## Features

### V1 — SQL Query Automation

- Execute SQL Server `SELECT` queries using Ansible
- Connect to SQL Server through ODBC
- Use a dedicated SQL read-only login
- Store the database password using Ansible Vault
- Validate that only `SELECT` queries are accepted
- Reject multiple SQL statements
- Display query results in Ansible output
- Prevent database changes through least-privilege SQL permissions

### V1.1 — Excel Export

- Export SQL query results to `.xlsx`
- Automatically generate Excel column headers from SQL metadata
- Write SQL query results into Excel rows
- Automatically adjust Excel column widths
- Support different SQL queries and database tables
- Generate Excel files dynamically using Python `openpyxl`

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Ansible | Automation and orchestration |
| Ansible Vault | Secure credential storage |
| Microsoft SQL Server | Database platform |
| AdventureWorks2022 | Sample SQL Server database |
| ODBC Driver 18 | SQL Server connectivity |
| pyodbc | ODBC connectivity |
| Python | Excel export automation |
| openpyxl | Excel workbook generation |
| Ubuntu / WSL | Automation environment |
| Git | Version control |
| GitHub | Source code repository |

---

## Project Structure

```text
ansible-sql-automation/
│
├── .git/
├── .gitignore
├── README.md
├── run_query.yml
├── export_to_excel.py
├── test_sql_connection.py
└── vault.yml
```

### File Description

| File | Description |
|---|---|
| `run_query.yml` | Main Ansible playbook |
| `export_to_excel.py` | Python script that creates the Excel workbook |
| `test_sql_connection.py` | Standalone SQL Server connectivity test |
| `vault.yml` | Encrypted Ansible Vault containing the database password |
| `.gitignore` | Prevents secrets and generated files from being committed |
| `README.md` | Project documentation |

---

## Security

Security is implemented using multiple layers.

### 1. Dedicated Read-Only SQL Account

The automation uses a dedicated SQL Server login:

```text
ansible_reader
```

The account is mapped to:

```text
AdventureWorks2022
```

and uses the SQL Server:

```text
db_datareader
```

database role.

The account does not have write permissions.

An attempted `UPDATE` operation was tested and SQL Server rejected it with a permission-denied error.

---

### 2. SELECT-Only Validation

Before the SQL query is executed, Ansible validates the supplied query.

A valid query must begin with:

```sql
SELECT
```

Example:

```sql
SELECT TOP 10
    BusinessEntityID,
    FirstName,
    LastName
FROM Person.Person
```

Write operations such as:

```sql
UPDATE
DELETE
INSERT
```

are rejected by the Ansible validation.

Multiple SQL statements are also rejected.

For example:

```sql
SELECT TOP 5 * FROM Person.Person;
UPDATE Person.Person SET FirstName = 'Test';
```

is rejected before the database execution task.

---

### 3. Ansible Vault

The SQL Server password is stored in:

```text
vault.yml
```

The file is encrypted using Ansible Vault.

The plaintext password is therefore not stored in the Git repository.

The Vault file is also included in `.gitignore`:

```text
vault.yml
```

---

### 4. Generated Files

The following files are generated locally during execution:

```text
query_results.json
query_results.xlsx
```

They are excluded from Git using `.gitignore`.

This prevents query output or generated data from being accidentally committed to the repository.

---

## How It Works

The automation follows these steps:

1. User provides a SQL `SELECT` query.
2. Ansible verifies that a query was provided.
3. Ansible validates that the query begins with `SELECT`.
4. Multiple SQL statements are rejected.
5. Ansible Vault provides the encrypted database password.
6. `community.general.odbc` connects to SQL Server.
7. The query is executed with `commit: false`.
8. Query results and column metadata are collected.
9. Ansible prepares the data for Excel export.
10. Python `openpyxl` creates the Excel workbook.
11. Query results are displayed in the terminal.
12. The Excel file is generated as:

```text
query_results.xlsx
```

---

## Excel Export

The Excel export workflow is:

```text
SQL SELECT Query
       │
       ▼
    Ansible
       │
       ▼
   SQL Server
       │
       ▼
 Query Results
       │
       ▼
query_results.json
       │
       ▼
export_to_excel.py
       │
       ▼
query_results.xlsx
```

The Excel column names are generated dynamically from SQL query metadata.

The project is therefore not hardcoded to a specific table or set of columns.

---

## Example 1 — Person Data

Command:

```bash
ansible-playbook run_query.yml \
  -e '{"sql_query":"SELECT TOP 5 BusinessEntityID, FirstName, LastName FROM Person.Person"}' \
  --ask-vault-pass
```

Example Excel output:

| BusinessEntityID | FirstName | LastName |
|---:|---|---|
| 285 | Syed | Abbas |
| 293 | Catherine | Abel |
| 295 | Kim | Abercrombie |
| 2170 | Kim | Abercrombie |
| 38 | Kim | Abercrombie |

---

## Example 2 — Product Data

The automation was also tested against a different SQL Server table:

```bash
ansible-playbook run_query.yml \
  -e '{"sql_query":"SELECT TOP 5 ProductID, Name, ProductNumber FROM Production.Product"}' \
  --ask-vault-pass
```

Example output:

| ProductID | Name | ProductNumber |
|---:|---|---|
| 1 | Adjustable Race | AR-5381 |
| 2 | Bearing Ball | BA-8327 |
| 3 | BB Ball Bearing | BE-2349 |
| 4 | Headset Ball Bearings | BE-2908 |
| 316 | Blade | BL-2036 |

This confirms that the Excel export is dynamic and works with different queries and tables.

---

## Running the Automation

### Basic Command

```bash
ansible-playbook run_query.yml \
  -e '{"sql_query":"SELECT TOP 5 BusinessEntityID, FirstName, LastName FROM Person.Person"}' \
  --ask-vault-pass
```

Ansible will prompt for the **Vault password**.

The SQL query is then validated and executed against SQL Server.

---

## Testing SQL Connectivity

A standalone Python script is included to test SQL Server connectivity independently from Ansible.

Run:

```bash
python3 test_sql_connection.py
```

This verifies:

- SQL Server connectivity
- ODBC driver configuration
- Database connectivity
- SQL credentials
- Basic query execution

---

## Ansible Syntax Check

Before running the playbook, the syntax can be checked with:

```bash
ansible-playbook --syntax-check run_query.yml --ask-vault-pass
```

Expected result:

```text
playbook: run_query.yml
```

---

## Excel File

After a successful execution, the generated file is:

```text
query_results.xlsx
```

The workbook contains:

- Column headers
- SQL Server query results
- Automatically adjusted column widths

The generated workbook can be opened directly using Microsoft Excel.

---

## Git and GitHub

The project is maintained using Git and hosted on GitHub.

Current commits include:

```text
6c2db2  Initial V1 - Ansible SQL query automation
ce767e2  Add project documentation
dc38da6  Add Excel export for SQL query results
```

The repository uses the `main` branch.

Sensitive files such as `vault.yml` are excluded from version control.

---

## Current Project Status

```text
V1
├── SQL Server connectivity       ✓
├── Read-only SQL account         ✓
├── Ansible automation            ✓
├── SELECT validation             ✓
├── Multi-statement protection    ✓
├── Ansible Vault                 ✓
└── Query result display          ✓

V1.1
├── Excel export                  ✓
├── Dynamic column headers        ✓
├── Dynamic query/table support   ✓
└── Generated output protection   ✓
```

---

## Future Enhancements

Possible future improvements include:

- Add reusable Ansible roles
- Improve SQL query validation using a SQL parser
- Add structured logging
- Add better error handling
- Make SQL Server connection parameters configurable
- Add automated testing
- Add CI/CD validation
- Add Excel formatting and filters
- Add timestamped Excel output
- Add optional CSV export
- Add support for scheduled DBA reports

---

## Project Goal

The goal of this project is to demonstrate practical **Database Administration + Automation + DevOps** skills by combining:

```text
SQL Server
     +
Ansible
     +
Python / ODBC
     +
Ansible Vault
     +
Git / GitHub
```

The project focuses on automating repetitive DBA operations while applying **least-privilege access, credential protection, query validation, and repeatable automation**.
