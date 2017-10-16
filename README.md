## ISPRAS API Python

### Installation

1. To install this SDK run 
```
python setup.py install
```

2. You can use pydoc to list available services
```
pydoc ispras
```
and check methods for each service
```
pydoc ispras.texterra
```

3. To use any service of ISPRAS API in your project, import subclass of module. For TexterraAPI it looks like this: 
```python
from ispras import texterra
```

4. Now you can create an access object using your Apikey:
```python
t = texterra.API('YOURKEY')
```
You can also specify service name and version:
```python
t = texterra.API('YOURKEY', 'texterra', 'v3.1')
```

5. To access different tools just call corresponding method:
```python
tags = t.posTaggingAnnotate('Hello World') 
# You can also invoke Texterra with custom request: 
result = t.customQuery(path, query) # for GET request 
result = t.customQuery(path, query, form) # for POST request
```

6. Methods return dictionary, so you can navigate through it according to [API documentation](https://api.ispras.ru/dev/rest):
```python
for annotation in tags:
		print annotation['text']
```
Use '@' before atrribute names and '#text' to access own text of nodes. 
Use only node name to access its text if there are no attributes or subnodes:
```python
print an['value']['@class'], an['value']['#text']
```
