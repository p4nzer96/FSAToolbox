from fsa import FSA

f=FSA()
f.fromfile('file.json')

print(f.X)