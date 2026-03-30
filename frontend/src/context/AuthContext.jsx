import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  signInWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  createUserWithEmailAndPassword
} from 'firebase/auth';
import { auth } from '../lib/firebase';
import axios from 'axios';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Sync auth state with Firebase
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        // Fetch full profile from backend
        try {
          const token = await firebaseUser.getIdToken();
          const response = await axios.get('/api/v1/auth/me', {
            headers: { Authorization: `Bearer ${token}` }
          });
          
          // Merge Firebase identifiers with backend profile explicitly
          setUser({
            uid: firebaseUser.uid,
            email: firebaseUser.email,
            ...response.data,
            token
          });
        } catch (err) {
          // Profile might not exist yet (onboarding flow)
          setUser({ 
            uid: firebaseUser.uid, 
            email: firebaseUser.email, 
            token: await firebaseUser.getIdToken(), 
            needsOnboarding: true 
          });
        }
      } else {
        setUser(null);
      }
      setIsLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const login = async (identifier, password) => {
    setIsLoading(true);
    setError(null);
    try {
      let email = identifier;
      
      // If identifier doesn't look like an email, try resolving it as a username
      if (!identifier.includes('@')) {
        const res = await axios.get(`/api/v1/auth/email?username=${identifier}`);
        email = res.data.email;
      }

      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      return userCredential.user;
    } catch (err) {
      setError(err.message || 'Login failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (email, password) => {
    setIsLoading(true);
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      // Backend initialization happens after this via onboarding
      return userCredential.user;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => signOut(auth);

  const value = {
    user,
    isLoading,
    error,
    login,
    logout,
    register
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
