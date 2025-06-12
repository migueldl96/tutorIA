from pyBKT.models import Model, Roster, StateType
import numpy as np

# Paso 1: Entrenamos el modelo en una habilidad concreta
model = Model(seed=42)
model.fit(data_path='../data/as_red.csv')

# Paso 2: Creamos el Roster con estudiantes y la habilidad que se va a seguir
roster = Roster(students=['78564'], skills='Volume Cylinder', model=model)

# Paso 3: Estado inicial de Olmo (antes de responder nada)
print("Estado inicial:")
print(f"¿Domina?: {roster.get_state_type('Volume Cylinder', '78564')}")
print(f"P(dominio): {roster.get_mastery_prob('Volume Cylinder', '78564'):.4f}")
print(f"P(respuesta correcta): {roster.get_correct_probs('Volume Cylinder')['78564']:.4f}")
print()

# Paso 4: Secuencia simulada de respuestas (1 = acierto, 0 = fallo)
respuestas = [1, 0, 1, 1, 1]  # Puedes cambiar esta lista

print("Actualizando estado tras cada respuesta:")
for i, respuesta in enumerate(respuestas, 1):
    state = roster.update_state('Volume Cylinder', '78564', respuesta)
    print(f"Paso {i} - Respuesta: {'✔️' if respuesta == 1 else '❌'}")
    print(f"  P(dominio): {state.get_mastery_prob():.4f}")
    print(f"  P(correcto): {state.get_correct_prob():.4f}")
    print(f"  ¿Domina?: {roster.get_state_type('Volume Cylinder', '78564') == StateType.MASTERED}")
    print()

# Paso 5: Comprobación final
if roster.get_state_type('Volume Cylinder', '78564') == StateType.MASTERED:
    print("🎉 ¡Olmo ha dominado la habilidad!")
else:
    print("🔄 Olmo aún no domina la habilidad.")
