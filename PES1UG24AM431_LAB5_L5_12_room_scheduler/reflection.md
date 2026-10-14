# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, maintainability problems, and coding-style violations early in development. This makes software easier to review and maintain.

### 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks overall code quality, naming, documentation, and potential programming mistakes. Bandit identifies common security risks, such as unsafe shell execution. Flake8 checks Python style and formatting according to PEP 8 and reports issues such as long lines and unused variables.

### 3. What issues did you identify and fix?

The original scheduler used a mutable default list, a bare exception handler, and `os.system()` to execute a shell command. It also had file-handling, naming, documentation, formatting, and input-validation problems. I replaced unsafe shell execution with normal file operations, improved exception handling, added input validation, and corrected the code style.

### 4. How did static analysis improve the program, and what are its limitations?

Static analysis improved the program's readability, security, and maintainability. Pylint improved from 5.60/10 to 9.88/10, Bandit reported no remaining issues, and Flake8 reported no violations. However, static analysis cannot prove that a program is functionally correct. Runtime testing is still necessary to verify booking conflicts, cancellation, equipment allocation, and invalid user input.