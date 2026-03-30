# 📋 Agile Agent Backlog (TubeRPG)

## EPIC 1: Foundation & Domain (Phase: Completed)
**Objective**: Establish the core domain logic for battle mechanics independent of external dependencies.
- [x] **Story 1.1:** As an architect, I want the Domain layer for Battle Mechanics (`battle.py` and tests) to handle HP math without dependencies.
  - *Acceptance Criteria:*
    - `Player` and `Enemy` classes exist with HP attributes.
    - `evaluate_answer` function calculates damage correctly based on `is_correct`.
    - Zero external dependencies in the domain.
  - *Required Tests (Unit):*
    - `test_evaluate_answer_correct`: Asserts that an enemy takes expected damage when the player answers correctly.
    - `test_evaluate_answer_incorrect`: Asserts that the player takes expected damage when the answer is wrong.
    - `test_evaluate_answer_hp_cannot_be_negative`: Asserts that HP stops at exactly 0 and never goes negative.

- [x] **Story 1.2:** As a backend, I want a YouTube Subtitles adapter to fetch raw text for the LLM.
  - *Acceptance Criteria:*
    - `YoutubeTranscriptAdapter` created and implements a port.
    - Can successfully fetch and concatenate transcripts from a valid YouTube video ID.
    - Handles unavailable language errors gracefully.
  - *Required Tests (Unit/Mock):*
    - `test_get_transcript_success`: Mocks the YouTube API to return a list of text snippets and asserts they are concatenated into a single string.
    - `test_get_transcript_failure`: Mocks an API error (e.g., subtitles disabled) and asserts the adapter raises a handled exception.

## EPIC 2: The E2E Data Contracts & Interfaces (Phase: Done)
**Objective**: Define the Pydantic schemas and interface protocols (Ports) to enforce strong typing and Hexagonal Architecture.
- [x] **Story 2.1:** As an Agent, I need to define the exact `Pydantic` schemas for the Game State (`PlayerProfile`, `EnemyState`) and the AI Output (`QuestionSchema`).
  - *Acceptance Criteria:*
    - `schemas.py` contains all required models.
    - Models match the specification defined in `spec_ai_brain.md`.
    - `QuestionSchema` includes 4 options and a correct option ID.
  - *Required Tests (Unit):*
    - `test_question_schema_validation`: Asserts that Pydantic rejects a `QuestionSchema` if it has fewer than 2 options or a missing correct ID.

- [x] **Story 2.2:** As an Agent, I need to define the abstract `Protocols` (Ports) for the LLM Orchestrator and the Database Repository.
  - *Acceptance Criteria:*
    - Protocols defined using Python's `Protocol` class.
    - Methods signatures are strictly typed.
  - *Required Tests:*
    - *(Structural/Static Checking)*: Pyright must pass, ensuring that any adapter implementing these protocols correctly matches the signatures. No explicit runtime tests required.

## EPIC 3: The AI Brain (Phase: Done)
**Objective**: Implement the AI adapter using Google Gemini to generate dynamic questions based on YouTube transcripts.
- [x] **Story 3.1:** As an Agent, I want to implement the `GeminiAdapter` using the `QuestionSchema` to guarantee structured JSON outputs.
  - *Acceptance Criteria:*
    - `GeminiAdapter` implements the `ILLMOrchestrator` port.
    - Configured to use structured outputs (JSON schema) conforming to `QuestionSchema`.
  - *Required Tests (Integration/Mock):*
    - `test_generate_question_parses_json`: Asserts the adapter successfully converts the raw LLM JSON string into a valid `QuestionSchema` object.

- [x] **Story 3.2:** As a developer, I need to mock the Gemini API in `test_gemini_adapter.py` to ensure robust error handling.
  - *Acceptance Criteria:*
    - Tests verify handling of invalid JSON schemas via `pydantic.ValidationError`.
  - *Required Tests (Unit):*
    - `test_generate_question_handles_malformed_json`: Mocks the LLM returning broken JSON and asserts the adapter catches `ValidationError` or `JSONDecodeError` to prevent application crashes.

## EPIC 4: The Database (Phase: Done)
**Objective**: Build out the Data Access layer and corresponding Google Cloud Infrastructure.
- [x] **Story 4.1:** As an Agent, I want to implement the `FirestoreRepository` to persist the Game State.
  - *Acceptance Criteria:*
    - Prepared Terraform to provision Firestore in GCP.
    - Adapter uses `google-cloud-firestore` async client and handles the `GOOGLE_CLOUD_PROJECT` env var connection.
  - *Required Tests:*
    - *(IaC)*: `terraform plan` succeeds without errors, verifying infrastructure definition.

- [x] **Story 4.2:** CRUD for Player Profiles.
  - *Acceptance Criteria:*
    - `get_user` and `save_user` methods are fully implemented using `merge=True`.
  - *Required Tests (Unit/AsyncMock):*
    - `test_get_user_returns_profile`: Mocks the Firestore DocumentReference to return valid data and asserts it parses into a `PlayerProfile`.
    - `test_get_user_returns_none`: Mocks a non-existent document and asserts it returns `None`.

- [x] **Story 4.3:** CRUD for Game Sessions.
  - *Acceptance Criteria:*
    - `get_session` and `save_session` methods are fully implemented.
  - *Required Tests (Unit/AsyncMock):*
    - `test_save_session_calls_set`: Asserts that `Firestore.collection.document.set` is called exactly once with the serialized `GameSession` data.

## EPIC 5: Core Application & API Delivery (Phase: Done)
**Objective**: Orchestrate the components into Use Cases and expose them via FastAPI endpoints.
- [x] **Story 5.1:** As an Agent, I want to create the Master `StartGameUseCase` and `PlayTurnUseCase` that ties YouTube, Gemini, and the Domain together.
  - *Acceptance Criteria:*
    - Use cases are instantiated with injected dependencies (Ports).
    - Session tracking and HP changes apply correctly.
  - *Required Tests (Unit/Mocks):*
    - `test_start_game_use_case_flow`: Mocks repositories and LLM; asserts a new session is correctly generated and saved.
    - `test_play_turn_correct_answer`: Asserts that a correct answer damages the enemy and triggers the AI to generate the *next* question.
    - `test_play_turn_game_over`: Asserts that if player HP drops to 0, the session is marked as inactive and no further questions are requested.

- [x] **Story 5.2:** As an Agent, I want to expose the Use Cases via FastAPI Endpoints (`/api/v1/game/start`, `/api/v1/game/play`).
  - *Acceptance Criteria:*
    - FastAPI app configures CORS and environment variables via python-dotenv.
    - Endpoints respond with HTTP 200 OK.
  - *Required Tests (E2E Integration):*
    - `test_api_game_flow_full_sequence`: Uses `fastapi.testclient.TestClient` to send a `POST /game/start` followed by a `POST /game/play`. Asserts the full HTTP -> Application -> Domain -> HTTP cycle, mocking *only* external I/O (Database, LLM, YouTube).

## EPIC 6: Frontend MVP (Phase: Pending)
**Objective**: Build the user interface using React and Vite, applying a Cyber-RPG aesthetic.
- [ ] **Story 6.1:** As an Agent, I want to scaffold the React + Vite E2E UI consuming our endpoints.
  - *Acceptance Criteria:*
    - Project created with React, Vite.
    - API client (`gameClient.js`) hits endpoints dynamically.
  - *Required Tests (Component/Integration):*
    - `test_api_client_calls_backend`: Mocks `fetch`/`axios` to ensure the correct payload is sent to the backend URL.
    - `test_arena_renders_question`: Asserts the Combat Arena component successfully renders the JSON question text and 4 button options received from the API.

- [ ] **Story 6.2:** Build the Core Interface Components.
  - *Acceptance Criteria:*
    - Establish design tokens (CSS Vars) for dark backgrounds and neon accents.
    - The Player HUD displays current and max HP.
  - *Required Tests (Component):*
    - `test_health_bar_width`: Asserts that a player with 50/100 HP renders a health bar `div` at exactly 50% width.

## EPIC 7: Sistema de Autenticación (Login)
**Contexto**: ["Identificar al usuario unívocamente, permitir acceso a sus datos, mantener persistencia de la sesión y del progreso"]
**Restricciones**: [
  * Es necesario tener en cuenta siempre Securty First, por lo que se debe implementar un sistema de autenticación robusto, que respete OWASP Top 10
  * Uso de Firebase Authentication para delegar la gestión de contraseñas y cumplir con los estándares de seguridad sin reinventar la rueda
  * El Frontend debe manejar las Sesiones mediante un JWT en HttpOnly Cookies o local storage, y las llamadas a la API deben usar un Interceptor HTTP (Axios) para inyectar el token
  * Patrón Protector de Rutas (Protected Routes) en React para evitar accesos a /arena sin autenticación
]

- [ ] **Story 7.1: UI del Componente Login** - "Como jugador, quiero un formulario claro y estético para ingresar mi email y contraseña, para no frustrarme al iniciar sesión."
  - *Contratos Técnicos:*
    - Props Entrantes: `onSubmit: (email, password) => Promise<void>`, `isLoading: boolean`, `errorMessage: string | null`
    - Estado Local (React useState): `email: string`, `password: string`
    - API Mock: N/A (Este componente es "Dummy", delega la lógica en el componente padre mediante `onSubmit`).
  - *Acceptance Criteria (BDD):*
    - **Escenario 1: Validación de campos vacíos**
      - `Dado que` el usuario está en el formulario.
      - `Cuando` intenta enviar el formulario sin completar email y password.
      - `Entonces` la función `onSubmit` NO debe llamarse.
      - `Y` los inputs vacíos deben obtener la clase `.neon-magenta` (borde de error).
    - **Escenario 2: Feedback de estado Loading**
      - `Dado que` el componente recibe la prop `isLoading=true`.
      - `Cuando` se renderiza.
      - `Entonces` el botón "Ingresar" debe estar deshabilitado.
      - `Y` debe mostrarse un indicador visual de carga (Spinner).
  - *Required Tests (Component UI):*
    - `test_login_form_validates_empty_fields`: Asegura que el submit se bloquee con campos vacíos.
    - `test_login_form_displays_loading`: Asegura que el botón se desactive correctamente.

- [ ] **Story 7.2: Integración de Auth y Estado Global** - "Como sistema frontend, quiero procesar las credenciales mediante la API y guardar el JWT globalmente, para que la app sepa quién soy en todo momento sin perder la sesión."
  - *Contratos Técnicos:*
    - Props/State: Contexto de React (`AuthContext`) que exporte `{ user, login(email, pass), logout(), isLoading }`.
    - API Mock: `POST /api/v1/auth/login` con payload `{ email, password }` respondiendo `{ access_token, user_id }`.
  - *Acceptance Criteria (BDD):*
    - **Escenario 1: Login Exitoso**
      - `Dado que` la API responde HTTP 200 con un token.
      - `Cuando` se ejecuta la función `login()` desde la UI.
      - `Entonces` el JWT se debe guardar (localStorage o cookies).
      - `Y` el contexto de React debe actualizar la variable `user`.
    - **Escenario 2: Credenciales Inválidas**
      - `Dado que` la API responde HTTP 401.
      - `Cuando` se ejecuta la función `login()`.
      - `Entonces` la Promesa debe retornar o lanzar el error.
      - `Y` el estado `user` del Contexto debe seguir siendo nulo.
  - *Required Tests (Integration/Hook):*
    - `test_auth_context_login_success`: Mapear mock de Axios a 200 OK y verificar que el hook retorna el usuario.
    - `test_auth_context_login_failure`: Mapear mock a 401 y asegurar lanzamiento de excepción.

- [ ] **Story 7.3: Rutas Protegidas (Guards)** - "Como jugador, quiero que si intento ir al juego sin estar logueado, me redirija al login automáticamente, para proteger el flujo del juego."
  - *Contratos Técnicos:*
    - Props/State: Componente `<ProtectedRoute children={<Outlet/>} />` que consume `AuthContext`.
    - UI Mock: React Router con wrap alrededor de `/arena`.
  - *Acceptance Criteria (BDD):*
    - **Escenario 1: Redirección sin Token**
      - `Dado que` el `user` es nulo en el `AuthContext`.
      - `Cuando` el usuario navega manualmente por URL a `/arena`.
      - `Entonces` el sistema debe redirigir a `/login`.
    - **Escenario 2: Acceso Permitido**
      - `Dado que` el `user` NO es nulo.
      - `Cuando` el usuario navega a `/arena`.
      - `Entonces` el componente hijo debe renderizarse sin interrupciones.
  - *Required Tests (Component/Router):*
    - `test_protected_route_redirects_unauthenticated`.
    - `test_protected_route_allows_authenticated`.

- [ ] **Story 7.4: Pantalla de Lobby Dashboard** - "Como jugador logueado, quiero aterrizar en un Lobby donde vea una bienvenida y mis opciones para jugar, en lugar ir ciego a la arena de combate."
  - *Contratos Técnicos:*
    - Props/State: Usa `user_id` del `AuthContext`.
    - API Mock: (Simulado) Botón que hace `navigate("/arena")` o input para `video_id`.
  - *Acceptance Criteria (BDD):*
    - **Escenario 1: Render del Layout Inicial**
      - `Dado que` el usuario aterriza en `/lobby`.
      - `Cuando` la vista carga.
      - `Entonces` debe verse su nombre de usuario/email.
      - `Y` el input para ingresar el Video de YouTube debe estar listo.
  - *Required Tests (Component):*
    - `test_lobby_renders_user_info`: Verifica que el texto del usuario extraido del contexto se muestre.
