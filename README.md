# Technology workshop class's final project

## Preparation:

Using conda or virtualenv is advisable, but not necessary.
The preparation only needs 1 step: `pip install -r requirements.txt`

## How to run:

1. Generate transformation matrix: `cat [link to GCPs file] | python FindTransform.py`
2. Generate picture using transformation matrix: `python PerformTransform.py` then do what the code ask.
3. Test the transformation matrix: `cat [link to test file] | python CheckGCP.py`
