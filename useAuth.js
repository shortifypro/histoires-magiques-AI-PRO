import { useState, useEffect, createContext, useContext } from 'react'

const AuthContext = createContext({})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(false)

  // Simulation d'authentification pour le développement
  const signInWithEmail = async (email) => {
    try {
      // Simulation d'un délai d'API
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Pour le développement, on simule un succès
      return { 
        success: true, 
        message: 'Lien de connexion envoyé par email ! (Mode développement)' 
      }
    } catch (error) {
      return { success: false, message: 'Erreur lors de l\'envoi de l\'email' }
    }
  }

  const signOut = async () => {
    try {
      setUser(null)
      return { success: true }
    } catch (error) {
      return { success: false, message: error.message }
    }
  }

  const getUserProfile = async () => {
    if (!user) return null
    return {
      id: user.id,
      email: user.email,
      free_credits_used: 0,
      free_credits_total: 3,
      subscription_plan: 'free'
    }
  }

  const checkFreeCredits = async () => {
    const profile = await getUserProfile()
    if (!profile) return 3 // Utilisateur non connecté = 3 crédits par défaut
    return Math.max(0, profile.free_credits_total - profile.free_credits_used)
  }

  const useFreeCredit = async () => {
    const remainingCredits = await checkFreeCredits()
    if (remainingCredits <= 0) {
      return { success: false, message: 'Plus de crédits gratuits disponibles' }
    }
    return { success: true, remainingCredits: remainingCredits - 1 }
  }

  const value = {
    user,
    loading,
    signInWithEmail,
    signOut,
    getUserProfile,
    checkFreeCredits,
    useFreeCredit
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

