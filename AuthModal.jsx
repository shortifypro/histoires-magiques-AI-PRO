import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { X, Mail, Sparkles } from 'lucide-react'
import { useAuth } from '../hooks/useAuth.js'

export default function AuthModal({ isOpen, onClose, title = "Connexion" }) {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [isSuccess, setIsSuccess] = useState(false)
  const { signInWithEmail } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email) return

    setLoading(true)
    setMessage('')
    
    const result = await signInWithEmail(email)
    
    setLoading(false)
    setMessage(result.message)
    setIsSuccess(result.success)
    
    if (result.success) {
      setTimeout(() => {
        onClose()
        setEmail('')
        setMessage('')
        setIsSuccess(false)
      }, 3000)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl relative">
        {/* Bouton fermer */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="w-6 h-6" />
        </button>

        {/* En-tête */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-[var(--magic-pink)]/20 to-[var(--magic-blue)]/20 rounded-2xl flex items-center justify-center">
            <Sparkles className="w-8 h-8 text-[var(--magic-pink)]" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">{title}</h2>
          <p className="text-gray-600">
            Entrez votre email pour recevoir un lien de connexion magique
          </p>
        </div>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Adresse email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="votre@email.com"
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[var(--magic-blue)] focus:border-transparent transition-all"
                required
                disabled={loading}
              />
            </div>
          </div>

          {/* Message de retour */}
          {message && (
            <div className={`p-4 rounded-xl text-sm ${
              isSuccess 
                ? 'bg-green-50 text-green-700 border border-green-200' 
                : 'bg-red-50 text-red-700 border border-red-200'
            }`}>
              {message}
            </div>
          )}

          {/* Bouton de soumission */}
          <Button
            type="submit"
            disabled={loading || !email}
            className="w-full bg-gradient-to-r from-[var(--magic-blue)] to-[var(--magic-pink)] text-white py-3 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:transform-none"
          >
            {loading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                <span>Envoi en cours...</span>
              </div>
            ) : (
              'Envoyer le lien magique'
            )}
          </Button>
        </form>

        {/* Informations supplémentaires */}
        <div className="mt-6 text-center">
          <p className="text-xs text-gray-500">
            En vous connectant, vous acceptez nos{' '}
            <a href="#" className="text-[var(--magic-blue)] hover:underline">
              conditions d'utilisation
            </a>{' '}
            et notre{' '}
            <a href="#" className="text-[var(--magic-blue)] hover:underline">
              politique de confidentialité
            </a>
          </p>
        </div>

        {/* Avantages */}
        <div className="mt-6 bg-gradient-to-r from-[var(--magic-blue)]/5 to-[var(--magic-pink)]/5 rounded-xl p-4">
          <h3 className="font-semibold text-gray-800 mb-2">✨ Avec votre compte :</h3>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• 3 histoires gratuites à l'inscription</li>
            <li>• Sauvegarde de toutes vos créations</li>
            <li>• Accès à votre bibliothèque personnelle</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

