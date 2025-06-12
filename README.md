# tutorIA (provisional)

⚠️ **Este proyecto está en una fase inicial de exploración y todo su contenido es tentativo.**

## 🧠 Descripción general

`tutorIA` es un proyecto experimental que busca desarrollar un sistema inteligente para **evaluar el estado de aprendizaje de un alumno** universitario y generar un **itinerario formativo personalizado** (learning path), en función de lo que el alumno sabe o no sabe sobre los conocimientos previos necesarios para acceder a una nueva asignatura.

## 📊 Evaluación del conocimiento

Se utilizarán **test estadísticos** (por definir) para determinar el nivel de conocimiento previo del alumno respecto a una asignatura objetivo. Esta evaluación servirá como punto de partida para adaptar la experiencia de aprendizaje.

## 📚 Generación del itinerario adaptado

Una vez evaluado, el sistema construirá un **learning path personalizado** utilizando contenidos ya existentes creados por el profesorado (presentaciones, PDFs, cursos, etc.). Este proceso se apoyará en técnicas de **RAG (Retrieval-Augmented Generation)** mediante IA.

## 🧩 Contenidos y módulos

El contenido generado se organizará en **módulos de aprendizaje**, que podrán adoptar múltiples formatos:
- Cuestionarios tipo Moodle
- Actividades interactivas
- Problemas guiados
- Otros formatos didácticos

## 🧪 Tecnologías previstas

Este es un listado inicial y provisional de tecnologías a utilizar:

- Python
- Docker
- Azure OpenAI
- Azure AI Search
- .NET

## ⚠️ Estado del proyecto


Este repositorio está en **fase de diseño y prototipado temprano**. Toda la funcionalidad, diseño y arquitectura están **sujetos a cambios**. La documentación y el código reflejan únicamente un trabajo exploratorio inicial.

## Usar repositorio
### Requisitos:
- Anaconda (o miniconda)
- Compiladores de C (gcc y g++)
### Instalamos gcc y g++
```bash
sudo apt-get install build-essential
```
### Instalar miniconda
### Configuración de entorno
Importamos el entorno desde el archivo 'environment.yml' con el siguiente comando:
```bash
conda env create -f environment.yml
```
### Activar entorno
```bash
conda activate tutorIA
```
### Lanzar servidor
uvicorn src.student_eval.app.main:app --reload

### Probar archivo Notebooks_BKT/Guía_rápida.ipynb
---

