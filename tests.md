# Testes

## Unidade e Integração (unittests + django)

- Estão em `paperpaper/tests.py`

#### Resultados dos testes
```bash
python manage.py test paperpaper.tests -v2
```

#### Cobertura
```bash
python -m coverage run --branch --omit="paperpaper/tests.py,tests_e2e_selenium.py,tests_e2e.py" manage.py test paperpaper.tests -v2
python -m coverage report
```

## End-to-End (E2E) (Selenium)
- Estão em `tests_e2e_selenium.py`

OBS: Necessita do browser FireFox
```bash
python manage.py test tests_e2e_selenium -v 2
```
 


