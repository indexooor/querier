# querier

querier service to query contract data indexed by indexooor core 😄


Setup

```
virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

run command

```

source venv/Scripts/activate
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 5010

```