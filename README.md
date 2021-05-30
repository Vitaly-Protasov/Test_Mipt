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
```

### Classify your text query:
* 1) Use notebook example: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1p94bCRCVdqfh4RaRRceSTeOE4TTdcrGA?usp=sharing)
* 2) Launch Python script: ```python main.py --request '<your request>' ```

### Example of how it works:
* __Launch__:
    ```
    python main.py --request 'Как вырастить помидор дома'
    ```
    
* __Output__:
    ```
    ('Овощные растения', 0.0020507489917480654)
    ('Анализ почвы', 0.0009848688333781)
    ('Плодовые растения', 0.0008842514811212309)
    ('Агрохимия ( удобрения, защита растений)', 0.00043219881145326847)
    ('Зерновые культуры', 0.00013675080096897711)
    ```
   