import pencilIcon from '../assets/icon-pencil.png'
import magicWandIcon from '../assets/icon-magic-wand.png'
import headphonesIcon from '../assets/icon-headphones.png'

export default function HowItWorksSection() {
  const steps = [
    {
      id: 1,
      icon: pencilIcon,
      title: "Racontez-nous",
      description: "Choisissez le héros, le thème et la morale de l'histoire. Notre formulaire magique guide votre créativité en quelques clics.",
      color: "var(--magic-yellow)"
    },
    {
      id: 2,
      icon: magicWandIcon,
      title: "Laissez-nous créer",
      description: "Notre IA écrit une histoire unique, la narre avec une voix chaleureuse et crée un livret PDF personnalisé.",
      color: "var(--magic-pink)"
    },
    {
      id: 3,
      icon: headphonesIcon,
      title: "Écoutez & rêvez",
      description: "Recevez votre histoire audio MP3 et son livret. Parfait pour le coucher ou les trajets en voiture.",
      color: "var(--magic-mint)"
    }
  ]

  return (
    <section className="py-20 lg:py-32 bg-white">
      <div className="container mx-auto px-4">
        {/* En-tête de section */}
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-5xl font-bold mb-6">
            <span className="text-[var(--magic-blue)]">La magie en</span>{' '}
            <span className="text-[var(--magic-pink)]">3 étapes</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            De votre idée à une histoire complète, tout se fait en moins de 60 secondes. 
            Découvrez comme c'est simple de créer des moments magiques.
          </p>
        </div>

        {/* Étapes */}
        <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
          {steps.map((step, index) => (
            <div key={step.id} className="relative group">
              {/* Ligne de connexion (sauf pour le dernier élément) */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-20 left-full w-full h-0.5 bg-gradient-to-r from-gray-200 to-transparent transform translate-x-4 z-0"></div>
              )}
              
              {/* Carte */}
              <div className="relative z-10 bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100 group-hover:border-gray-200">
                {/* Numéro d'étape */}
                <div 
                  className="absolute -top-4 -right-4 w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-lg"
                  style={{ backgroundColor: step.color }}
                >
                  {step.id}
                </div>

                {/* Icône */}
                <div className="mb-6">
                  <div className="w-20 h-20 mx-auto mb-4 p-4 rounded-2xl bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <img 
                      src={step.icon} 
                      alt={step.title}
                      className="w-12 h-12 object-contain"
                    />
                  </div>
                </div>

                {/* Contenu */}
                <div className="text-center">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {step.description}
                  </p>
                </div>

                {/* Effet de brillance au survol */}
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
              </div>
            </div>
          ))}
        </div>

        {/* Call to action */}
        <div className="text-center mt-16">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-[var(--magic-blue)]/10 to-[var(--magic-pink)]/10 px-6 py-3 rounded-full border border-[var(--magic-blue)]/20 mb-6">
            <span className="text-sm font-medium text-gray-700">✨ Prêt à commencer l'aventure ?</span>
          </div>
          <button className="bg-gradient-to-r from-[var(--magic-blue)] to-[var(--magic-pink)] text-white px-8 py-4 rounded-full font-semibold text-lg shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
            Créer ma première histoire gratuitement
          </button>
        </div>
      </div>
    </section>
  )
}

