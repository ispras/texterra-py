## ISPRAS API Python

### Installation

1. To install this SDK run 
```
python setup.py install
```
or you can install using pip:
```
pip install texterra
```

2. You can use pydoc to list available services
```
pydoc texterra
```
and check documentation of methods for each service
```
pydoc texterra.texterra
```

3. To use Texterra API in your project, simply import it like this: 
```python
import texterra
```

4. Now you can create an access object using your API key:
```python
t = texterra.API('YOURKEY')
```

5. To access different tools just call the corresponding method:
```python
tags = t.pos_tagging('Hello World') 
# You can also invoke Texterra with custom request: 
result = t.custom_query(path, params) # for GET request 
result = t.custom_query(path, params, headers, json) # for POST request
```
