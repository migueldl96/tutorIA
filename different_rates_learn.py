from pyBKT.models import Model
import pandas as pd
import numpy as np
# # Creamos un pequeño dataset de ejemplo
data = pd.DataFrame({
    'user_id': ['alice', 'alice', 'bob', 'bob', 'carol', 'carol',
                'alice', 'alice', 'bob', 'bob', 'carol', 'carol',
                'alice', 'bob', 'carol'],
    'skill_name': ['add_fractions']*6 + ['simplify_fraction']*6 + ['mixed_numbers']*3,
    'correct': [0, 1, 0, 0, 1, 1,  1, 0, 1, 1, 0, 1, 1, 0, 1],
})

# Añadimos order_id por estudiante y skill
data['order_id'] = data.groupby(['user_id', 'skill_name']).cumcount() + 1

# # Inicializamos el modelo y entrenamos con learn rate individual por estudiante
model = Model()
model.fit(data=data, skills='add_fractions', multiprior="user_id")

# Mostramos los parámetros aprendidos para cada estudiante
print(model.params())

model2 = Model()

# Entrenamos usando multilearn para forzar diferenciación por estudiante
model2.fit(data=data, defaults={
    'order_id': 'order_id',
    'skill_name': 'skill_name',
    'correct': 'correct',
    'user_id': 'user_id'
}, multilearn='user_id', fixed=True)

print("🎯 PRUEBA 2 - Parámetros con prior personalizado:")
print(model2.params())
