import Header from './components/Header.jsx'
import HeroSection from './components/HeroSection.jsx'
import HowItWorksSection from './components/HowItWorksSection.jsx'
import PricingSection from './components/PricingSection.jsx'
import Footer from './components/Footer.jsx'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main>
        <HeroSection />
        <HowItWorksSection />
        <PricingSection />
      </main>
      <Footer />
    </div>
  )
}

export default App
