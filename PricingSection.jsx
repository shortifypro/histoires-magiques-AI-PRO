import { Button } from '@/components/ui/button.jsx'
import { Check, Star, Crown, Users } from 'lucide-react'

export default function PricingSection() {
  const plans = [
    {
      name: "Gratuit",
      price: "0",
      period: "pour toujours",
      description: "Parfait pour découvrir la magie",
      features: [
        "3 histoires gratuites à l'inscription",
        "Fichiers MP3 et PDF",
        "Voix française de qualité",
        "Histoires de 3-5 minutes"
      ],
      buttonText: "Commencer gratuitement",
      buttonVariant: "outline",
      popular: false,
      icon: Star,
      color: "var(--magic-mint)"
    },
    {
      name: "Starter",
      price: "12",
      period: "par mois",
      description: "Idéal pour une famille",
      features: [
        "Histoires illimitées",
        "Toutes les voix disponibles",
        "Personnalisation avancée",
        "Bibliothèque personnelle",
        "Support prioritaire"
      ],
      buttonText: "Choisir Starter",
      buttonVariant: "default",
      popular: true,
      icon: Crown,
      color: "var(--magic-pink)"
    },
    {
      name: "Family",
      price: "24",
      period: "par mois",
      description: "Pour les grandes familles",
      features: [
        "Tout du plan Starter",
        "Jusqu'à 5 profils enfants",
        "Histoires plus longues (10 min)",
        "Musiques de fond variées",
        "Accès anticipé aux nouveautés"
      ],
      buttonText: "Choisir Family",
      buttonVariant: "default",
      popular: false,
      icon: Users,
      color: "var(--magic-blue)"
    }
  ]

  return (
    <section className="py-20 lg:py-32 bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50">
      <div className="container mx-auto px-4">
        {/* En-tête de section */}
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-5xl font-bold mb-6">
            <span className="text-[var(--magic-blue)]">Choisissez votre</span>{' '}
            <span className="text-[var(--magic-pink)]">aventure</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Commencez gratuitement et découvrez la magie. Aucun engagement, 
            annulation possible à tout moment.
          </p>
        </div>

        {/* Plans tarifaires */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => {
            const IconComponent = plan.icon
            return (
              <div 
                key={plan.name}
                className={`relative bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border-2 ${
                  plan.popular 
                    ? 'border-[var(--magic-pink)] scale-105' 
                    : 'border-gray-100 hover:border-gray-200'
                }`}
              >
                {/* Badge populaire */}
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="bg-gradient-to-r from-[var(--magic-pink)] to-[var(--magic-purple)] text-white px-6 py-2 rounded-full text-sm font-semibold shadow-lg">
                      ⭐ Le plus populaire
                    </div>
                  </div>
                )}

                {/* Icône du plan */}
                <div className="text-center mb-6">
                  <div 
                    className="w-16 h-16 mx-auto rounded-2xl flex items-center justify-center mb-4"
                    style={{ backgroundColor: `${plan.color}20` }}
                  >
                    <IconComponent 
                      className="w-8 h-8" 
                      style={{ color: plan.color }}
                    />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-800">{plan.name}</h3>
                  <p className="text-gray-600 mt-2">{plan.description}</p>
                </div>

                {/* Prix */}
                <div className="text-center mb-8">
                  <div className="flex items-baseline justify-center">
                    <span className="text-4xl font-bold text-gray-800">{plan.price}€</span>
                    <span className="text-gray-600 ml-2">/{plan.period}</span>
                  </div>
                </div>

                {/* Fonctionnalités */}
                <div className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <div key={featureIndex} className="flex items-start space-x-3">
                      <div 
                        className="flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center mt-0.5"
                        style={{ backgroundColor: plan.color }}
                      >
                        <Check className="w-3 h-3 text-white" />
                      </div>
                      <span className="text-gray-700 text-sm leading-relaxed">{feature}</span>
                    </div>
                  ))}
                </div>

                {/* Bouton d'action */}
                <Button 
                  className={`w-full py-3 rounded-full font-semibold transition-all duration-300 ${
                    plan.popular
                      ? 'bg-gradient-to-r from-[var(--magic-pink)] to-[var(--magic-purple)] text-white shadow-lg hover:shadow-xl transform hover:scale-105'
                      : plan.buttonVariant === 'outline'
                      ? 'border-2 border-gray-300 text-gray-700 hover:border-[var(--magic-blue)] hover:text-[var(--magic-blue)] bg-white'
                      : 'bg-[var(--magic-blue)] text-white hover:bg-[var(--magic-blue)]/90 shadow-lg hover:shadow-xl'
                  }`}
                >
                  {plan.buttonText}
                </Button>
              </div>
            )
          })}
        </div>

        {/* Garantie et informations supplémentaires */}
        <div className="text-center mt-16">
          <div className="inline-flex items-center space-x-2 bg-white/60 backdrop-blur-sm px-6 py-3 rounded-full border border-white/40 mb-4">
            <span className="text-sm text-gray-700">🛡️ Garantie satisfait ou remboursé 30 jours</span>
          </div>
          <p className="text-gray-600 text-sm max-w-2xl mx-auto">
            Tous nos plans incluent un support client réactif et des mises à jour régulières. 
            Changez ou annulez votre abonnement à tout moment depuis votre espace personnel.
          </p>
        </div>
      </div>
    </section>
  )
}

