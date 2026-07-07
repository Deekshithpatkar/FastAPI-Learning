import inspect

def student(id: int, name: str):
    return {"id": id, "name": name}

print(student)
print(student.__name__)
print(student.__annotations__)
print(inspect.signature(student))

sig = inspect.signature(student)

for name, parameter in sig.parameters.items():
    print("Parameter:", name)
    print("Type:", parameter.annotation)