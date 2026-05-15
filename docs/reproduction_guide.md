\# Reproduction Guide



\## 1. Requirements



\- Python 3.10

\- IBM ILOG CPLEX Optimization Studio 22.1

\- Git

\- Windows 10/11 recommended



\---



\## 2. Clone repository



```bash

git clone https://github.com/Jose-Angel12/timetabling-itcm.git

cd timetabling-itcm

```



\---



\## 3. Create virtual environment



```bash

python -m venv .venv

```



Windows:



```bash

.venv\\Scripts\\activate

```



\---



\## 4. Install dependencies



```bash

pip install -r requirements.txt

```



\---



\## 5. Configure environment variables



Copy:



```bash

copy .env.example .env

```



Edit `.env` and configure:



```env

CPLEX\_BIN=C:\\Program Files\\IBM\\ILOG\\CPLEX\_Studio221\\cplex\\bin\\x64\_win64\\cplex.exe

```



\---



\## 6. Build model data



```bash

python src/Datos\_Modelo.py

```



\---



\## 7. Solve model



```bash

python src/Modelo.py

```



\---



\## 8. Run dashboard



```bash

streamlit run src/dashboard\_isc.py

```



\---



\## 9. Example outputs



Example outputs are available in:



```text

outputs/

```



Including:



\- Timetables

\- Classroom assignments

\- Teacher assignments



\---



\## 10. Notes



The original institutional datasets may require anonymization before publication.



The repository includes representative outputs and reproducible configurations for experimentation.

