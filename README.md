# Test task

### Firstly
```
pip install -r requirements.txt
```

### From queries to files
```python3
from parse_data import TextParser
queries: List[str] = <your queries>
parser = TextParser(queries)