import { Button } from '@/components/ui/button.jsx'
import logoImage from '../assets/logo-histoires-magiques.png'

export default function Header() {
  return (
    <header className="bg-white/80 backdrop-blur-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <img 
              src={logoImage} 
              alt="Histoires Magiques" 
              className="h-10 w-auto"
            />
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a 
              href="#" 
              className="text-gray-700 hover:text-[var(--magic-blue)] transition-colors font-medium"
            >
              Comment ça marche
            </a>
            <a 
              href="#" 
              className="text-gray-700 hover:text-[var(--magic-blue)] transition-colors font-medium"
            >
              Exemples
            </a>
            <a 
              href="#" 
              className="text-gray-700 hover:text-[var(--magic-blue)] transition-colors font-medium"
            >
              Tarifs
            </a>
          </nav>

          {/* Boutons d'action */}
          <div className="flex items-center space-x-4">
            <Button 
              variant="ghost" 
              className="hidden sm:inline-flex text-gray-700 hover:text-[var(--magic-blue)]"
            >
              Se connecter
            </Button>
            <Button 
              className="bg-[var(--magic-pink)] hover:bg-[var(--magic-pink)]/90 text-white px-6 py-2 rounded-full font-medium shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            >
              Essayer gratuitement
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}

