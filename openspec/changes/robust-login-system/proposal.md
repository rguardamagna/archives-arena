# Proposal: Robust Login System

## Goal
Implement a production-grade authentication and user profiling system using the Firebase Local Emulator Suite. This will provide a "real" database-backed identity layer for the TubeRPG game without incurring cloud costs or requiring an internet connection during development.

## Motivation
As we transition from a mock-up to a functional MVP, the lack of a persistent identity layer is a blocker for player progression (HP, XP, Levels). Implementing this now ensures the project has a solid architectural foundation ("Security First") and leverages modern DevOps practices with Docker, aligning with the goal of building a premium, scalable application.

## Requirements
- **Authentication**: Sign-up and Log-in using Email and Password via Firebase Auth.
- **Identity Mapping**: Support for "Login with Username" by mapping aliases to Firebase emails on the server side.
- **User Profiling**: Automated creation of a `PlayerProfile` in Firestore upon registration.
- **Onboarding Flow**: Post-signup "Character Selection" to define the player's Class and Username.
- **Security**: All authentication and data access must be mediated by the FastAPI backend (Server-side verification) to prevent unauthorized Firestore access from the client.

## Impact
- **Backend**: New `FirebaseAuthAdapter`, `auth` router, and security middleware.
- **Frontend**: Integration of the Firebase JS SDK and Refactor of `AuthContext`.
- **Infra**: Addition of the Firebase Emulator service to `docker-compose.yml`.
- **Database**: New `players` and `usernames` collections in Firestore.
