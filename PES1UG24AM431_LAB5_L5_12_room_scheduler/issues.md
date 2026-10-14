# Lab 5: Static Code Analysis — Issue Report

| Issue | Type | Line(s) Before Fix | Description | Fix Approach |
|---|---|---|---|---|
| Shell command execution using `os.system` | Security — High | 43 | Running a shell command with a constructed string can allow command injection and is not portable to Windows. | Removed shell execution and used Python file handling to read and display the conflict log. |
| Broad exception handling with `except: pass` | Code quality / Security | 23–28 | Suppressed all exceptions, hiding unexpected failures and making debugging difficult. | Used explicit reservation lookup and handled missing reservations without suppressing unrelated errors. |
| Mutable default argument `equipment_list=[]` | Potential bug | 11 | A mutable default list can be shared across function calls. | Changed the default to `None` and created a fresh list for each call. |
| File operations without context managers or encoding | Code quality | 34–43 | Files were manually opened and closed, with no explicit encoding. | Used `with open(...)` and `encoding="utf-8"`. |
| Invalid time slots | Functional bug | 30–32, 48–49 | Invalid slots such as `14-12` and integer values could produce incorrect or inconsistent results. | Added validation for string format and start/end hour ranges. |
| Missing docstrings and inconsistent naming | Code quality | Multiple | Functions lacked documentation, and `logConflicts` did not follow snake_case naming. | Added module/function docstrings and renamed the method to `log_conflicts`. |
| Long lines, whitespace violations, and unused variables | Style | Multiple | Violated PEP 8 and triggered Flake8 and Pylint warnings. | Reformatted the code and removed unused assignments. |
| Equipment availability was not validated | Functional bug | 16–18 | Repeated or unknown equipment requests could produce incorrect inventory counts. | Validated equipment names and quantities before updating inventory. |

## Verification

- Original Pylint score: 5.60/10.
- Updated Pylint score: 9.88/10 before the final minor cleanup.
- Original Bandit report: one High-severity and one Low-severity finding.
- Updated Bandit report: no issues identified.
- Updated Flake8 report: no violations reported.

The reports are saved in the `reports/` directory. Final verification should be performed again after the last code change.