# Project Architecture: Current vs. Final State

Here is the breakdown of the project's structure, focusing on the **Hexagonal Architecture** (Ports and Adapters).

## 1. Current Architecture (Hexagonal Focus)
This diagram shows how the Core Domain is isolated and interacts with external services via Ports and Adapters.

```mermaid
graph TD
    subgraph "External World"
        GAI["Google AI (Gemini)"]
        YTA["YouTube API (Subtitles)"]
        GCP["GCP Firestore (Data)"]
    end

    subgraph "Infrastructure Layer (Adapters)"
        GAD["GeminiAdapter.py"]
        YTD["YoutubeAdapter.py"]
        FSD["FirestoreRepository.py"]
    end

    subgraph "Application Layer (Ports)"
        ILLM[["ILLMOrchestrator (Protocol)"]]
        IVTP[["IVideoTranscriptProvider (Protocol)"]]
        IUR[["IUserRepository (Protocol)"]]
    end

    subgraph "Domain Layer (Core)"
        BTL["Battle.py (Logic/HP Math)"]
        SCH["Schemas.py (Pydantic Models)"]
    end

    %% Interactions
    GAD -.-> ILLM
    YTD -.-> IVTP
    FSD -.-> IUR

    ILLM --> SCH
    IVTP --> SCH
    IUR --> SCH
    BTL --> SCH
```

## 2. Final E2E Target Architecture
The complete flow from the React frontend to the storage layer through the orchestration use cases.

```mermaid
graph TD
    subgraph "Client Layer (Frontend)"
        RFE["React + Vite (UI)"]
    end

    subgraph "Infrastructure Layer (API & Adapters)"
        FAR["FastAPI Router"]
        GAD["GeminiAdapter.py"]
        YTD["YoutubeAdapter.py"]
        FSD["FirestoreRepository.py"]
    end

    subgraph "Application Layer (Use Cases)"
        PTU["PlayTurnUseCase.py"]
        GSU["GetSessionUseCase.py"]
    end

    subgraph "Domain Layer (Core)"
        BTL["Battle.py (Combat Log)"]
        SCH["Schemas.py (Model Contract)"]
    end

    %% Final E2E Flow
    RFE --> FAR
    FAR --> PTU
    PTU --> BTL
    PTU --> GAD
    PTU --> YTD
    PTU --> FSD
    GAD -.-> GAI_EXT["Gemini API"]
    YTD -.-> YT_EXT["YouTube"]
    FSD -.-> FS_EXT["Firestore"]
```

## 🏗️ Key Principles Applied
- **Dependency Rule:** All dependencies point inwards. The **Domain** knows nothing about FastAPI, Firestore, or Gemini.
- **Isolation:** If we want to change from Gemini to GPT-4, we only replace one adapter (`GeminiAdapter.py`).
- **Testability:** We can test the entire **Application Layer** using mocks for the ports, exactly as I did in the Firestore tests.

---
**Current Progress:** We are finishing the **Infrastructure & Ports** (Gray/Blue boxes).
**Next Step:** Building the **Application Layer** (Green boxes) to drive the game logic.
