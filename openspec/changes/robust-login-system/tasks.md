## 1. Infrastructure & Dependencies

- [x] 1.1 Add `firebase-emulator` service to `docker-compose.yml` with ports 9099, 8080, and 4000
- [x] 1.2 Add `firebase-admin` and `python-dotenv` to `backend/requirements.txt`
- [x] 1.3 Ensure `firebase` and `axios` are in `frontend/package.json`
- [x] 1.4 Add `frontend` service to `docker-compose.yml` for unified orchestration

## 2. Backend: Auth Adapter & Middleware

- [x] 2.1 Create `app/infrastructure/adapters/firebase_auth_adapter.py` for token verification
- [x] 2.2 Implement `app/infrastructure/api/dependencies.py` with `get_current_user` logic
- [x] 2.3 Add `UserRepository.get_by_username` to support login via alias
- [x] 2.4 Create `app/infrastructure/api/auth_router.py` and register it in `main.py`

## 3. Frontend: SDK Integration & Context

- [x] 3.1 Create `src/lib/firebase.js` to initialize the SDK and connect to local emulators
- [x] 3.2 Refactor `src/context/AuthContext.jsx` to replace mocks with `signInWithEmailAndPassword` and `onAuthStateChanged`
- [x] 3.3 Update `src/components/ProtectedRoute.jsx` to redirect "unprofiled" users to onboarding
- [x] 3.4 Implement a "Character Selection" component for picking a Class and Username

## 4. Verification & Polish

- [x] 4.1 Verify Firebase Emulator UI is accessible at `http://localhost:4000`
- [x] 4.2 Manual test: Register -> Character Selection -> Session Start
- [x] 4.3 Add a verification test in `backend/tests/test_auth.py`
