# 📘 Guía de Referencia: Spec as Source (Frontend)

> **"Specification as Source" (SpaS) o Spec-Driven Development** significa que el documento no es solo "una idea de lo que queremos hacer", sino **la fuente de verdad absoluta**. El código que se escribe (React, Vite, CSS) es simplemente un medio para satisfacer los contratos estrictos, mocks y casos de prueba definidos en la especificación. Si no está en la Spec, no se programa. Si el código no cumple la Spec, el PR se rechaza.

Para pasar de PM a Arquitecto/Data-DevOps, adoptar esta mentalidad te separa de los programadores junior que "codifican por intuición".

---

## 1. La Anatomía Pura de la Especificación

Una Spec as Source en Frontend debe contener **cuatro capas innegociables**:

### A. La Épica (El "Para Qué" de Negocio)
Define el objetivo de alto nivel y el impacto en el usuario.
- **Formato:** `EPIC [ID]: [Nombre del Feature Completo]`
- **Contexto:** ¿Qué problema resuelve?
- **Restricciones Globales:** ¿Afecta ruteo? ¿Requiere Auth? ¿Impacta en SEO?

### B. Las User Stories (El "Qué")
Divide la historia en fragmentos testeables e independientes.
- **Formato Clásico:** *"Como [Usuario/Rol], quiero [Acción] para [Beneficio/Razón]."*
- **Scope Estricto:** Si la historia es sobre el layout, no incluye lógica de API. Si es sobre integración de API, asume que el layout ya existe.

### C. Los Contratos Técnicos (El "Con Qué")
Aquí es donde aplicamos la verdadera Arquitectura. En Frontend, los contratos son:
- **Interfaces / Props:** (Qué recibe el componente React).
- **Esquemas de Estado:** (Zustand, Redux, o Estado Local JSON).
- **Mock de la API:** (El JSON exacto que espera enviar/recibir).

### D. Los Criterios de Aceptación (El "Cómo validarlo")
Usamos el formato **BDD (Behavior-Driven Development) / Gherkin**. Esto se puede traducir DIRECTAMENTE a tests de Cypress/Playwright o React Testing Library.
- `Dado que (Given)`: Contexto inicial.
- `Cuando (When)`: Acción del usuario.
- `Entonces (Then)`: Resultado esperado y validable en la UI.

---

## 2. Ejemplo Práctico: Página de Login

A continuación, un ejemplo de cómo se escribe una Spec as Source perfecta para implementar un Login.

---

# 📝 SPEC: EPIC 7 - Sistema de Autenticación (Login)

**Contexto:** Necesitamos que los jugadores ingresen a TubeRPG usando su cuenta (por ahora simularemos un login con User ID, preparando el terreno para Firebase Auth).
**Restricciones:** El acceso a la ruta `/arena` debe estar bloqueado si el usuario no tiene un token activo. Todo el diseño debe seguir nuestro Cyber-RPG Design System.

## 📌 Contratos Técnicos Base (Fuente de Verdad)

**Payload Esperado por el Backend (Simulado / Futuro):**
```json
// POST /api/v1/auth/login
{
  "email": "player@tuberpg.com",
  "password": "hashed_string"
}

// Response (200 OK)
{
  "access_token": "jwt_ey...",
  "user": {
    "user_id": "test_player_01",
    "username": "CyberKnight"
  }
}
```

**Props del Componente `<LoginForm />`:**
```typescript
interface LoginFormProps {
  onSubmit: (credentials: LoginState) => Promise<void>;
  isLoading: boolean;
  errorMessage: string | null;
}
```

---

## 📖 Historia de Usuario 7.1: UI del Formulario de Login
**"Como jugador sin autenticar, quiero ver un formulario de login con estilo Cyber-RPG para poder ingresar mis credenciales."**

### Criterios de Aceptación (BDD)

**Escenario 1: Renderizado Inicial**
* **Dado que** el usuario navega a la ruta `/login`.
* **Entonces** debe ver un contenedor `.glass-panel`.
* **Y** debe ver un input para `Email` y un input para `Password`.
* **Y** el botón de "Ingresar" debe estar deshabilitado hasta que ambos campos tengan texto.

**Escenario 2: Validación de Input de Email**
* **Dado que** el usuario está en `/login`.
* **Cuando** escribe un texto sin formato de email (ej: `hola123`).
* **Entonces** el input de email debe mostrar un borde de clase `.neon-magenta` (error) al perder el foco (`onBlur`).
* **Y** debe aparecer un texto diminuto indicando "Email inválido".

---

## 📖 Historia de Usuario 7.2: Integración y Estado de Autenticación
**"Como jugador, quiero que mis credenciales sean enviadas al sistema y que la UI me dé feedback mientras carga o si fallo."**

### Criterios de Aceptación (BDD)

**Escenario 1: Feedback de Carga (Loading State)**
* **Dado que** el formulario tiene credenciales válidas.
* **Cuando** el usuario hace click en "Ingresar" (Submit).
* **Entonces** el botón "Ingresar" debe deshabilitarse.
* **Y** se debe mostrar un spinner de carga (`.animate-spin`).
* **Y** el componente React debe llamar a prop `onSubmit`.

**Escenario 2: Login Fallido (Error Handling)**
* **Dado que** el usuario intentó loguearse.
* **Cuando** la promesa `onSubmit` devuelve una excepción (ej: `HTTP 401 Unauthorized`).
* **Entonces** la UI de carga se detiene.
* **Y** se renderiza un div con la prop `errorMessage` ("Credenciales incorrectas") en color `text-magenta`.

**Escenario 3: Login Exitoso y Redirección**
* **Dado que** la promesa `onSubmit` se resuelve con éxito (`HTTP 200 OK`).
* **Cuando** la función termina.
* **Entonces** el Contexto Global de React (`AuthContext`) debe guardar el `user_id`.
* **Y** la aplicación debe forzar una redirección mediante React Router hacia `/arena`.

---

## 3. ¿Por qué esto te hace un Arquitecto?

Si un frontend developer toma este documento, **no tiene que tomar ninguna decisión de diseño lógico**. 
1. Sabe exactamente qué Props debe tener el componente.
2. Sabe exactamente cómo es el payload JSON (sin tener que adivinar o explorar Swagger a ciegas).
3. Sabe exactamente qué tests debe escribir (Cypress o React Testing Library). Si el Test para el *Escenario 2 de la US 7.2* falla, el ticket se rechaza. 

Esto es **Spec as Source**. El código se somete a la especificación, no al revés.
