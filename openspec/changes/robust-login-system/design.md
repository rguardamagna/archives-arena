# Design: Robust Login System

## Context
The TubeRPG application currently relies on a mock authentication system in the frontend, which hinders the implementation of meaningful player progression and persistence. To align with our "Security First" and "Absolute Architect" principles, we need a robust, backend-verified identity system. We will use the Firebase Local Emulator Suite encapsulated in Docker to provide a production-like environment without cloud dependency.

## Goals / Non-Goals

**Goals:**
- **Local Isolation**: All auth and database operations run via Docker Emulators.
- **Server-Side Verification**: Backend must verify every request using Firebase ID Tokens.
- **Dual Login**: Users can identify themselves via Email (standard) or Username (custom mapping).
- **Profile Consistency**: Every user must have a corresponding `PlayerProfile` in Firestore.

**Non-Goals:**
- **Social Auth**: No Google, Apple, or Facebook login in this phase.
- **Password Recovery**: Standard "Forgot Password" flow is excluded from the local MVP.
- **Deployment to Cloud**: This design focuses exclusively on the local development environment.

## Decisions

### 1. Firebase Emulator Suite (Docker)
We will add a specialized service to `docker-compose.yml` to orchestrate Auth and Firestore emulators. 
*Rationale*: This provides a zero-cost, persistent, and portable backend for all developers.

### 2. Backend Middleware & JWT Verification
FastAPI dependencies will extract the `Bearer` token and use the `firebase-admin` Python SDK to verify it.
*Rationale*: Moving auth logic to the server prevents "Client-Only" security holes and follows the Hexagonal Architecture pattern where the Auth Provider is an interchangeable Adapter.

### 3. Username-to-Email Resolution
Since Firebase Auth is email-centric, we will implement a "Username Registry" in Firestore.
*Flow*: 
1. If the user enters a non-email identifier, the Backend searches the `usernames` collection for the corresponding email.
2. The Backend then proceed with standard Firebase verification.

### 4. Post-Registration Onboarding
To keep Sign-Up frictionless (Email/Pass only), we will implement a "Pending Profile" state.
*Rationale*: Users can jump in quickly and choose their "Class" and "Username" in a second screen, which then hydrates the Firestore profile.

## Risks / Trade-offs

- **Risk**: Port conflicts on the host machine for the Emulator ports (9099, 8080, 4000).
  - *Mitigation*: Map these ports explicitly in `docker-compose.yml` and add a health check.
- **Trade-off**: Slightly higher latency during login due to the additional Firestore lookup for usernames.
  - *Decision*: Acceptable for a gamified MVP to achieve the desired UX.
