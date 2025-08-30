import { createClient } from '@supabase/supabase-js'

// Configuration Supabase - À remplacer par vos vraies clés
const supabaseUrl = 'https://your-project.supabase.co'
const supabaseAnonKey = 'your-anon-key'

// Pour le développement, nous utiliserons des valeurs par défaut
// En production, ces valeurs devront être configurées via des variables d'environnement
const supabaseUrlDev = import.meta.env.VITE_SUPABASE_URL || supabaseUrl
const supabaseKeyDev = import.meta.env.VITE_SUPABASE_ANON_KEY || supabaseAnonKey

export const supabase = createClient(supabaseUrlDev, supabaseKeyDev)

// Schéma de base de données pour référence
export const DATABASE_SCHEMA = {
  users: {
    id: 'uuid PRIMARY KEY',
    email: 'text UNIQUE NOT NULL',
    created_at: 'timestamp with time zone DEFAULT now()',
    subscription_plan: 'text DEFAULT \'free\'', // 'free', 'starter', 'family'
    subscription_status: 'text DEFAULT \'active\'', // 'active', 'cancelled', 'expired'
    free_credits_used: 'integer DEFAULT 0',
    free_credits_total: 'integer DEFAULT 3'
  },
  stories: {
    id: 'uuid PRIMARY KEY',
    user_id: 'uuid REFERENCES users(id)',
    title: 'text NOT NULL',
    content: 'text NOT NULL',
    audio_url: 'text',
    pdf_url: 'text',
    character_name: 'text',
    character_type: 'text',
    theme: 'text',
    moral: 'text',
    voice_type: 'text',
    created_at: 'timestamp with time zone DEFAULT now()'
  },
  subscriptions: {
    id: 'uuid PRIMARY KEY',
    user_id: 'uuid REFERENCES users(id)',
    paypal_subscription_id: 'text UNIQUE',
    plan_type: 'text NOT NULL', // 'starter', 'family'
    status: 'text NOT NULL', // 'active', 'cancelled', 'expired'
    created_at: 'timestamp with time zone DEFAULT now()',
    expires_at: 'timestamp with time zone'
  }
}

