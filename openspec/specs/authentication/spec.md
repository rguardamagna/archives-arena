## ADDED Requirements

### Requirement: Email-based Sign-up
The system SHALL allow users to create a new account using only an email address and a password.

#### Scenario: Successful sign-up
- **WHEN** user provides a valid email and a 6+ character password
- **THEN** a Firebase Auth user is created and a redirect to onboarding is triggered

### Requirement: Identity Initialization (Onboarding)
New users SHALL select a unique username and a character class before accessing game features.

#### Scenario: Completing onboarding
- **WHEN** user provides a unique username and selects a valid class
- **THEN** the `PlayerProfile` is updated in Firestore and the user is redirected to the Level Selector

### Requirement: Multi-identifier Login
The system SHALL support authentication using either the registered email address or the unique username.

#### Scenario: Login with Username
- **WHEN** user provides their username and password
- **THEN** the backend resolves the username to an email and authenticates via Firebase Auth

### Requirement: Token-based Session Security
Every API request to protected resources SHALL be verified using a Firebase ID Token (JWT).

#### Scenario: Authenticated API request
- **WHEN** a request includes a valid `Authorization: Bearer <ID_TOKEN>` header
- **THEN** the backend extracts the `uid` and provides access to the resource
