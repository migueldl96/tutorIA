# tests/test_student_model.py
import os
import pickle
import yaml
import pandas as pd
import pytest
import sys
# Añadimos como path la ruta superior
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Ajusta esta importación al módulo donde hayas definido StudentModel
from src.student_eval.app.evaluation.models import StudentModel  

from pyBKT.models import Model, Roster

@pytest.fixture
def tmp_env(tmp_path):
    """
    Crea un entorno temporal con evaluation_path, model_path y CSVs en tmp_path.
    Devuelve un StudentModel configurado para usar esas rutas.
    """
    sm = StudentModel()
    # paths dentro de tmp_path
    sm.csv_path = str(tmp_path / "dataset.csv")
    sm.evaluation_csv_path_non_trained = str(tmp_path / "eval_non_trained.csv")
    sm.evaluation_csv_path_trained     = str(tmp_path / "eval_trained.csv")
    sm.evaluation_path                 = str(tmp_path / "eval_rosters")
    os.makedirs(sm.evaluation_path)
    sm.model_path                      = str(tmp_path / "model.pkl")
    return sm, tmp_path

def test_update_dataset_creates_and_trains(tmp_env):
    sm, tmp_path = tmp_env

    # Si no hay dataset.csv, update_dataset debe crear uno nuevo y entrenar
    out = sm.update_dataset(
        order_id=[10],
        user_id=["alice"],
        skill_name=["fractions"],
        correct=[1],
        item_id=["Q1"],
        subject_id=["MATH"]
    )

    # Se debe haber creado dataset.csv
    assert os.path.exists(sm.csv_path)
    df = pd.read_csv(sm.csv_path)
    assert len(df) == 1
    assert df.loc[0, "user_id"] == "alice"
    assert df.loc[0, "skill_name"] == "fractions"

    # La salida debe contener estados de estudiantes y habilidades
    assert "students_states" in out and "skills_states" in out

    students = out["students_states"]
    skills   = out["skills_states"]
    # Debe tener exactamente la entrada de 'alice'
    assert "alice" in students
    # Dentro de skills, la asignatura 'MATH' debe mapear a la skill 'fractions'
    assert "MATH" in skills and "fractions" in skills["MATH"]

def test_update_dataset_appends_existing(tmp_env):
    sm, tmp_path = tmp_env

    # Prepara un dataset previo con alice
    initial = pd.DataFrame([{
        "order_id": 1,
        "user_id": "alice",
        "skill_name": "fractions",
        "correct": 0,
        "item_id": "Q1",
        "subject_id": "MATH"
    }])
    initial.to_csv(sm.csv_path, index=False)

    # Llamamos de nuevo con alice y bob
    out = sm.update_dataset(
        order_id=[2],
        user_id=["bob"],
        skill_name=["equations"],
        correct=[1],
        item_id=["Q2"],
        subject_id=["MATH"]
    )

    df = pd.read_csv(sm.csv_path)
    # Ahora debe haber dos filas
    assert set(df["user_id"]) == {"alice", "bob"}

    # Comprueba que bob aparece en la salida
    students = out["students_states"]
    skills   = out["skills_states"]
    assert "bob" in students
    
    # Comprobar que la habilidad 'equations' se ha añadido
    assert "MATH" in skills and "equations" in skills["MATH"]
    

def test_update_dataset_evaluation_no_dataset(tmp_env, caplog):
    sm, tmp_path = tmp_env

    # Ni dataset.csv
    res = sm.update_dataset_evaluation()
    assert res["students_states"] is None
    assert res["skills_states"] is None
    assert "Dataset CSV file not found" in caplog.text

def test_update_dataset_evaluation_no_eval_csv(tmp_env, caplog):
    sm, tmp_path = tmp_env

    # Creamos solo dataset.csv, pero no evaluation_csv_path_non_trained
    pd.DataFrame({
        "order_id": [1],
        "user_id": ["alice"],
        "skill_name": ["fractions"],
        "correct": [1],
        "item_id": ["Q1"],
        "subject_id": ["MATH"]
    }).to_csv(sm.csv_path, index=False)

    res = sm.update_dataset_evaluation()
    assert res["students_states"] is None
    assert res["skills_states"] is None
    assert "Evaluation CSV file not found" in caplog.text

def test_update_dataset_evaluation_success(tmp_env):
    sm, tmp_path = tmp_env

    # dataset.csv existente
    base = pd.DataFrame({
        "order_id": [1],
        "user_id": ["alice"],
        "skill_name": ["fractions"],
        "correct": [1],
        "item_id": ["Q1"],
        "subject_id": ["MATH"]
    })
    base.to_csv(sm.csv_path, index=False)

    # evaluation non_trained
    ext = pd.DataFrame({
        "order_id": [2],
        "user_id": ["bob"],
        "skill_name": ["equations"],
        "correct": [0],
        "item_id": ["Q2"],
        "subject_id": ["MATH"]
    })
    ext.to_csv(sm.evaluation_csv_path_non_trained, index=False)

    # Ejecuta actualización
    res = sm.update_dataset_evaluation()

    # dataset.csv debe ahora tener filas de base + ext
    df_all = pd.read_csv(sm.csv_path)
    assert set(df_all["user_id"]) == {"alice", "bob"}

    # eval_non_trained debe haberse eliminado
    assert not os.path.exists(sm.evaluation_csv_path_non_trained)
    # eval_trained debe existir y contener ext
    trained = pd.read_csv(sm.evaluation_csv_path_trained)
    assert len(trained) == 1 and trained.loc[0, "user_id"] == "bob"

    # La salida debe tener estudiantes y habilidades
    students = res["students_states"]
    skills   = res["skills_states"]
    assert "alice" in students and "bob" in students
    assert "MATH" in skills and "equations" in skills["MATH"]


def test_update_dataset_evaluation_del_roster_clears_folder(tmp_env):
    sm, tmp_path = tmp_env

    # Prepara datos mínimos
    pd.DataFrame({
        "order_id": [1],
        "user_id": ["alice"],
        "skill_name": ["fractions"],
        "correct": [1],
        "item_id": ["Q1"],
        "subject_id": ["MATH"]
    }).to_csv(sm.csv_path, index=False)
    pd.DataFrame({
        "order_id": [2],
        "user_id": ["alice"],
        "skill_name": ["fractions"],
        "correct": [0],
        "item_id": ["Q2"],
        "subject_id": ["MATH"]
    }).to_csv(sm.evaluation_csv_path_non_trained, index=False)

    # Crea un fichero dummy en evaluation_path
    dummy = tmp_path / "eval_rosters" / "foo.tmp"
    dummy.write_text("x")

    # Llamamos con del_roaster=True
    sm.update_dataset_evaluation(del_roaster=True)

    # La carpeta evaluation_path debe quedar vacía
    assert os.listdir(sm.evaluation_path) == []

def test_start_real_time_eval_no_eval_path(tmp_env):
    sm, tmp_path = tmp_env
    # lo forzamos a un path que no existe
    sm.evaluation_path = str(tmp_path / "no_exist")
    resp = sm.start_real_time_evaluation("user1", ["s1"])
    assert resp["status"] == "error"
    assert "Evaluation path does not exist" in resp["message"]


def test_start_real_time_eval_model_not_found(tmp_env):
    sm, tmp_path = tmp_env
    # evaluation_path existe, pero model_path no
    # sm.model_path no existe
    resp = sm.start_real_time_evaluation("user1", ["skill1"])
    assert resp["status"] == "error"
    assert "Model path does not exist" in resp["message"]

def test_start_real_time_eval_creates_roster_and_config(tmp_env):
    sm, tmp_path = tmp_env
    # creamos un modelo BKT válido y lo pickleamos
    m = Model(seed=0)
    # entrenamos con un dataset mínimo para que no pete al crear el Roster
    df = pd.DataFrame({
        "user_id": ["u"], "skill_name": ["s"], "correct": [1], "order_id": [1]
    })
    m.fit(data=df, skills="s")
    with open(sm.model_path, "wb") as f:
        pickle.dump(m, f)

    # llamamos al método
    resp = sm.start_real_time_evaluation("u", ["s", "t"])
    assert resp["status"] == "ok"
    # debe devolver un roster_path para cada skill
    assert set(resp["roster_paths"].keys()) == {"s", "t"}
    # comprobar que los archivos existen
    for p in resp["roster_paths"].values():
        assert os.path.exists(p)

    # comprobar contenido de roster_config.yaml
    cfg_file = os.path.join(sm.evaluation_path, "roster_config.yaml")
    with open(cfg_file) as f:
        cfg = yaml.safe_load(f)
    assert "u" in cfg
    # cada path debe mapearse a la lista correcta de skills
    skill_map = cfg["u"]["skills"]
    for path, skills in skill_map.items():
        # todas las skills que solicitamos deben aparecer en la configuración
        assert set(skills).issubset({"s", "t"})

def test_start_real_time_eval_reuses_existing(tmp_env):
    sm, tmp_path = tmp_env
    # preparamos un config con un roster ya existente que cubre 'a'
    eval_cfg = {
        "bob": {
            "skills": {
                str(tmp_path / "roster_bob_a.pkl"): ["a"]
            }
        }
    }
    cfg_path = os.path.join(sm.evaluation_path, "roster_config.yaml")
    with open(cfg_path, "w") as f:
        yaml.safe_dump(eval_cfg, f)

    # creamos el modelo de disco para 'b'
    m = Model(seed=0)
    df = pd.DataFrame({
        "user_id": ["bob"], "skill_name": ["b"], "correct": [1], "order_id": [1]
    })
    m.fit(data=df, skills="b")
    with open(sm.model_path, "wb") as f:
        pickle.dump(m, f)

    # pedimos evaluar ['a','b']
    resp = sm.start_real_time_evaluation("bob", ["a","b"])
    # para 'a' debe reutilizar el path ya existente
    assert resp["roster_paths"]["a"] == str(tmp_path / "roster_bob_a.pkl")
    # para 'b' debe crear uno nuevo
    assert resp["roster_paths"]["b"].endswith("roster_bob_b.pkl")

def test_real_time_evaluation_roster_not_found(tmp_env):
    sm, tmp_path = tmp_env
    # path absurdo
    bad_path = str(tmp_path / "no.pkl")
    out = sm.real_time_evaluation(
        order_id=1,
        user_id="x",
        skill_name="y",
        correct=1,
        item_id="i",
        subject_id="sub",
        roster_path=bad_path
    )
    # al no encontrar el roster devuelve todos None
    assert out == {"state": None, "correct_prob": None, "state_prob": None}

def test_real_time_evaluation_success(tmp_env):
    sm, tmp_path = tmp_env

    # 1) Entrenar un modelo BKT mínimo
    df_train = pd.DataFrame({
        "user_id":     ["u"],
        "skill_name":  ["skillX"],
        "correct":     [1],
        "order_id":    [1]
    })
    m = Model(seed=0)
    m.fit(data=df_train, skills="skillX", multiprior="user_id")
    # Guardamos el modelo en disco
    model_file = tmp_path / "model.pkl"
    with open(model_file, "wb") as f:
        pickle.dump(m, f)
    sm.model_path = str(model_file)

    # 2) Creamos un roster para ese usuario/habilidad y lo persistimos
    roster = Roster(students=["u"], skills="skillX", model=m)
    roster_dir = tmp_path / "eval"
    roster_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    roster_file = roster_dir / "roster_u_skillX.pkl"
    with open(roster_file, "wb") as f:
        pickle.dump(roster, f)

    # 3) Llamamos a real_time_evaluation
    result = sm.real_time_evaluation(
        order_id    = 42,
        user_id     = "u",
        skill_name  = "skillX",
        correct     = 1,
        item_id     = "Q1",
        subject_id  = "MATH",
        roster_path = str(roster_file)
    )

    # 4) Comprobamos la respuesta
    assert set(result.keys()) == {"state", "correct_prob", "state_prob"}
    # state debe ser una de las cadenas del Enum
    assert result["state"] in {"DEFAULT_STATE","MASTERED","UNMASTERED"}
    # probabilidades entre 0 y 1
    assert 0.0 <= result["correct_prob"] <= 1.0
    assert 0.0 <= result["state_prob"]   <= 1.0

    # 5) Y que se ha creado el CSV de evaluación no entrenada
    csv_path = sm.evaluation_csv_path_non_trained
    assert os.path.exists(csv_path)

    df_eval = pd.read_csv(csv_path)
    # Debe contener exactamente una fila con los datos que pasamos
    assert len(df_eval) == 1
    row = df_eval.iloc[0]
    assert row["order_id"]   == 42
    assert row["user_id"]    == "u"
    assert row["skill_name"] == "skillX"
    assert row["correct"]    == 1
    assert row["item_id"]    == "Q1"
    assert row["subject_id"] == "MATH"

def test_real_time_evaluation_roster_missing(tmp_env):
    sm, tmp_path = tmp_env
    # Llamamos con una ruta que no existe
    bad = tmp_path / "eval" / "no_roster.pkl"
    out = sm.real_time_evaluation(
        order_id    = 1,
        user_id     = "x",
        skill_name  = "y",
        correct     = 0,
        item_id     = "Z",
        subject_id  = "S",
        roster_path = str(bad)
    )
    # Cuando falla al cargar el roster, devuelve todo None
    assert out == {"state": None, "correct_prob": None, "state_prob": None}