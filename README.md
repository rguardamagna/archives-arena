# 🎮 TubeRPG: E2E Learning Arena

## 📝 Resumen del Proyecto
**TubeRPG** es una plataforma de aprendizaje gamificada que transforma videos de YouTube en niveles de un RPG. Utiliza un motor de IA (Gemini 3.0 Flash/Pro) para analizar transcripciones en tiempo real y generar desafíos de combate basados estrictamente en el contenido del video. 

El objetivo es acelerar la retención de conocimientos mediante el ciclo de "Estudio -> Combate -> Progreso".

---

## 🚀 Key Features (Implementado)
- **Identity Nexus (Auth)**: Sistema de autenticación robusto integrado con Firebase (Emails + Usernames).
- **Onboarding Flow**: Selección de clase de personaje (Warrior, Mage, Rogue) con estética "Dark Academia".
- **YouTube Combat Arena**: Extracción de video IDs y preparación para la generación dinámica de preguntas.
- **Full-Stack Orchestration**: Todo el entorno (Frontend, Backend, Firebase Emulator) corre en un solo comando de Docker.

---

## 🏗️ Arquitectura Técnica (Hexagonal)

El proyecto sigue una arquitectura de **Puertos y Adaptadores** para garantizar la desacoplación total de los servicios de nube:

- **Frontend**: React + Vite + Tailwind 4. Estética premium con Glassmorphism y tipografía Cinzel/Lora.
- **Backend**: FastAPI (Python 3.10+). Manejo asíncrono de peticiones e inyección de dependencias.
- **Data Layer**: Firestore (NoSQL) para perfiles y sesiones.
- **Auth Layer**: Firebase Auth (Local Emulator para desarrollo, Cloud para producción).
- **AI Engine**: Gemini SDK para el procesamiento de lenguaje natural.

---

## 🛠️ Guía de Inicio Rápido (Local Development)

### 1. Requisitos Previos
- Docker & Docker Desktop.
- Una `GEMINI_API_KEY` (configurada en el `.env`).

### 2. Configuración del Entorno
Cloná el repo y creá un archivo `.env` en la raíz (usá `.env.example` como base si existe):
```bash
PROJECT_ID=tuber-rpg
GEMINI_API_KEY=tu_api_key_aca
```

### 3. Levantar el Stack
```bash
docker-compose up --build -d
```

### 4. Acceso a los Servicios
- **Frontend App**: [http://localhost:5173](http://localhost:5173)
- **Backend API (Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Firebase Emulator UI**: [http://localhost:4000](http://localhost:4000)

---

## 🚢 Roadmap & Deployment
- [x] Full-Stack Orchestration con Docker.
- [x] Firebase Auth Backend Verification.
- [/] AI Question Generator (Gemini Integration).
- [ ] CI/CD Pipeline (GitHub Actions).
- [ ] Producción: Despliegue en Hetzner VPS.

---

## 👨‍🏫 Mentor Notes (Rioplatense Style)
Che, loco, fijate que la arquitectura está pensada para que seas un **Absolute Architect**. Usamos Docker no solo porque es "cool", sino porque te da **aislamiento total**. El día de mañana, si querés cambiar Firebase por MongoDB, solo tenés que cambiar un *Adapter* en `infrastructure/` sin tocar una sola línea de lógica de negocio. ¡Eso es SOLID de verdad! 🧉🔥

---

## 📜 Licencia
Este proyecto es parte del camino de transición a **Technical Expert**. Uso libre para fines educativos.
