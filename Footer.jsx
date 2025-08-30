import { Heart, Mail, MapPin } from 'lucide-react'
import logoImage from '../assets/logo-histoires-magiques.png'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Logo et description */}
          <div className="md:col-span-2 space-y-4">
            <img 
              src={logoImage} 
              alt="Histoires Magiques" 
              className="h-12 w-auto brightness-0 invert"
            />
            <p className="text-gray-400 max-w-md leading-relaxed">
              Créez des moments magiques avec vos enfants grâce à nos histoires audio personnalisées. 
              Chaque histoire est unique et adaptée à votre petit héros.
            </p>
            <div className="flex items-center space-x-2 text-sm text-gray-400">
              <Heart className="w-4 h-4 text-[var(--magic-pink)]" />
              <span>Fait avec amour pour les familles</span>
            </div>
          </div>

          {/* Liens rapides */}
          <div>
            <h3 className="font-semibold text-lg mb-4 text-white">Liens rapides</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-400 hover:text-[var(--magic-pink)] transition-colors">Comment ça marche</a></li>
              <li><a href="#" className="text-gray-400 hover:text-[var(--magic-pink)] transition-colors">Exemples d'histoires</a></li>
              <li><a href="#" className="text-gray-400 hover:text-[var(--magic-pink)] transition-colors">Tarifs</a></li>
              <li><a href="#" className="text-gray-400 hover:text-[var(--magic-pink)] transition-colors">FAQ</a></li>
              <li><a href="#" className="text-gray-400 hover:text-[var(--magic-pink)] transition-colors">Blog</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="font-semibold text-lg mb-4 text-white">Support</h3>
            <ul className="space-y-3">
              <li>
                <a href="mailto:contact@histoires-magiques.com" className="text-gray-400 hover:text-[var(--magic-mint)] transition-colors flex items-center space-x-2">
                  <Mail className="w-4 h-4" />
                  <span>contact@histoires-magiques.com</span>
                </a>
              </li>
              <li>
                <div className="text-gray-400 flex items-center space-x-2">
                  <MapPin className="w-4 h-4" />
                  <span>Suisse</span>
                </div>
              </li>
            </ul>
          </div>
        </div>

        {/* Séparateur */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-gray-400 text-sm">
              © 2024 Histoires Magiques. Tous droits réservés.
            </div>
            <div className="flex space-x-6 text-sm">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Conditions d'utilisation</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Politique de confidentialité</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Mentions légales</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

