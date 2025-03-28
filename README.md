# 2024_RP_3E_N3XT
N3XT - Jaromír Obitko, Matěj Kryštof Zich, Michal Drápal 

[Prezentace 1](https://docs.google.com/presentation/d/1JVJeRS3xDeapZDWGwykHUfxAE9_kRY2ILhCKTlxtKJ4/edit?usp=sharing)

[Prezentace 2](https://docs.google.com/presentation/d/1lx2NM3tQIRyjscBn8-69G_tDTQ_a8WnBYybl524v9OQ/edit?usp=sharing)

[Obhajoba SOČ](https://docs.google.com/presentation/d/1NoC7e-Ibjq2_CpCtp5y8QGFANqurjdLrVnFvech1Zno/edit?usp=sharing)

Pro přepsání do WASM máme vedlejší repozitář, ve kterém se nachází také statická verze stránky. [N3XT WASM](https://github.com/Jaromir007/n3xt_wasm)

## Konvence 

Každá "django" složka má v sobě podsložku, která definuje pro co je její obsah určený. (Jména souborů se budou často opakovat, tímto se zamezí souvisejícím problémům.)

#### Příklad: 

✅ **Správně:**

`static/global/css/main.css`
`templates/global/layout.html`
`static/web/css/main.css`

⚠️ **Špatně:**

`static/css/main.css`
`templates/layout.html`

## How to run:

1. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment:**

    **On Windows (Git bash):**
    ```bash
    source .venv/Scripts/activate
    ```

    **On Linux/MacOS:**
    ```bash
    source .venv/bin/activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Change to the app directory:**
    ```bash
    cd app
    ```

6. **Run:**
    ```bash
    python manage.py runserver
    ```
