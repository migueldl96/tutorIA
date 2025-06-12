from learningFunction import *
from simStudent import Student
from skill import Skill
import yaml
import json
from pathlib import Path

def main():
    # Ruta al YAML con los casos de estudiante
    cases_path = Path(__file__).parent / "student_sim" / "student_cases.yml"
    with open(cases_path, "r") as f:
        cases = yaml.safe_load(f)
    hist = []
    entries = []
    # Para cada estudiante y cada skill, simulamos 200 iteraciones
    for student_id, conf in cases.items():
        for _, skill_conf in conf["skills"].items():
            b = skill_conf.get("b", 2)  # Valor por defecto de b
            skill = Skill(
                skill_name=skill_conf["name"],
                subject=skill_conf.get("subject", ""),
                prob_guess=skill_conf.get("prob_guess", 0.0)

            )
            sigmoid_func = sigmoidLearningFunction(a=0.5, b=b)
            lernfunc = learningFunction(func=sigmoid_func)
            student = Student(
                user_id=student_id,
                learning_func=lernfunc,
                prob_slip=conf.get("prob_slip", 0.0)
            )
            
            history = student.learn(skill=skill, time=500)
            
            for entry in history:
                if skill_conf["name"] == "caida_libre":
                  hist.append(entry.correct)
                entries.append({
                    "order_id": entry.order_id,
                    "user_id": entry.user_id,
                    "skill_name": entry.skill_name,
                    "correct": entry.correct,
                    "item_id": entry.item_id,
                    "subject_id": entry.subject_id
                })

    # Volcar a JSON para update_dataset()
    dataset_path = Path(__file__).parent / "dataset.json"
    with open(dataset_path, "w") as f:
        json.dump(entries, f, indent=2)
    print(f"Dataset guardado en {dataset_path}")
if __name__ == "__main__":
    main()