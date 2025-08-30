import { Button } from '@/components/ui/button.jsx'
import { Play, Sparkles } from 'lucide-react'
import heroImage from '../assets/hero-fox-moon.png'

export default function HeroSection() {
  return (
    <section className="relative py-20 lg:py-32 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 overflow-hidden">
      {/* Éléments décoratifs de fond */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-4 h-4 bg-[var(--magic-yellow)] rounded-full opacity-60 animate-bounce"></div>
        <div className="absolute top-40 right-20 w-6 h-6 bg-[var(--magic-mint)] rounded-full opacity-40 animate-pulse"></div>
        <div className="absolute bottom-20 left-20 w-3 h-3 bg-[var(--magic-pink)] rounded-full opacity-50 animate-bounce" style={{animationDelay: '1s'}}></div>
        <div className="absolute top-60 left-1/3 w-5 h-5 bg-[var(--magic-purple)] rounded-full opacity-30 animate-pulse" style={{animationDelay: '2s'}}></div>
      </div>

      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Contenu textuel */}
          <div className="space-y-8">
            <div className="space-y-4">
              <div className="inline-flex items-center space-x-2 bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full border border-white/40">
                <Sparkles className="w-4 h-4 text-[var(--magic-yellow)]" />
                <span className="text-sm font-medium text-gray-700">Nouveau : Histoires personnalisées en 60 secondes</span>
              </div>
              
              <h1 className="text-4xl lg:text-6xl font-bold leading-tight">
                <span className="text-[var(--magic-blue)]">Des histoires</span>
                <br />
                <span className="text-[var(--magic-pink)]">magiques</span>
                <br />
                <span className="text-gray-800">pour vos enfants</span>
              </h1>
              
              <p className="text-xl text-gray-600 leading-relaxed max-w-lg">
                Créez des histoires audio personnalisées avec les héros préférés de votre enfant. 
                Une nouvelle aventure chaque soir pour des rêves enchantés.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                size="lg"
                className="bg-[var(--magic-pink)] hover:bg-[var(--magic-pink)]/90 text-white px-8 py-4 rounded-full font-semibold text-lg shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
              >
                <Play className="w-5 h-5 mr-2" />
                Créer ma première histoire
              </Button>
              
              <Button 
                variant="outline" 
                size="lg"
                className="border-2 border-[var(--magic-blue)] text-[var(--magic-blue)] hover:bg-[var(--magic-blue)] hover:text-white px-8 py-4 rounded-full font-semibold text-lg transition-all duration-300"
              >
                Voir un exemple
              </Button>
            </div>

            {/* Statistiques */}
            <div className="flex items-center space-x-8 pt-8">
              <div className="text-center">
                <div className="text-2xl font-bold text-[var(--magic-blue)]">10,000+</div>
                <div className="text-sm text-gray-600">Histoires créées</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-[var(--magic-pink)]">5,000+</div>
                <div className="text-sm text-gray-600">Familles heureuses</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-[var(--magic-mint)]">4.9/5</div>
                <div className="text-sm text-gray-600">Note moyenne</div>
              </div>
            </div>
          </div>

          {/* Image hero */}
          <div className="relative">
            <div className="relative z-10">
              <img 
                src={heroImage} 
                alt="Renard magique lisant sur la lune" 
                className="w-full max-w-md mx-auto drop-shadow-2xl animate-float"
              />
            </div>
            
            {/* Cercles décoratifs */}
            <div className="absolute inset-0 -z-10">
              <div className="absolute top-10 right-10 w-32 h-32 bg-[var(--magic-yellow)]/20 rounded-full blur-xl"></div>
              <div className="absolute bottom-10 left-10 w-40 h-40 bg-[var(--magic-mint)]/20 rounded-full blur-xl"></div>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-60 bg-[var(--magic-pink)]/10 rounded-full blur-2xl"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

