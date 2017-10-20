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

3. To use TEXTERRA API in your project, simply import it like this: 
```python
import texterra
```

4. Now you can create an access object using your Apikey:
```python
t = texterra.API('YOURKEY')
```

5. To access different tools just call corresponding method:
```python
tags = t.posTaggingAnnotate('Hello World') 
# You can also invoke Texterra with custom request: 
result = t.customQuery(path, query) # for GET request 
result = t.customQuery(path, query, form) # for POST request
```
