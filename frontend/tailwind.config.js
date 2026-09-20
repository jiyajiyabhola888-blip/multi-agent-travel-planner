/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary Brand: Sophisticated Blush, Baby Pink, Soft Rose, Warm Reddish-Pink
        brand: {
          50: '#FFF1F2',
          100: '#FFE4E6',
          200: '#FECDD3',
          300: '#FDA4AF',
          400: '#FB7185',
          500: '#F43F5E',
          600: '#E11D48',
          700: '#BE123C',
          800: '#9F1239',
          900: '#881337',
          950: '#4C0519',
        },
        rose: {
          50: '#FFF5F7',
          100: '#FDF2F8',
          200: '#FCE7F3',
          300: '#FBCFE8',
          400: '#F9A8D4',
          500: '#F472B6',
          600: '#EC4899',
          700: '#DB2777',
          800: '#BE185D',
          900: '#9D174D',
        },
        blush: {
          50: '#FFF5F7',
          100: '#FFE9EE',
          200: '#FFD3DC',
          300: '#FFB2C3',
          400: '#FF84A1',
          500: '#F43F5E',
          600: '#E11D48',
          700: '#BE123C',
        },
        // Secondary: Cream, Pure White & Very Light Pink
        cream: {
          50: '#FFFAF7',
          100: '#FFF5F0',
          200: '#FAEFEA',
          300: '#F5E6DF',
          400: '#E8D5CD',
        },
        surface: {
          50: '#FFFDFD',
          100: '#FFF5F7',
          200: '#FDEEF2',
          300: '#F9E2E8',
        },
        // Neutral Charcoal & Deep Slate Text
        navy: {
          900: '#0F172A',
          800: '#1E293B',
          700: '#334155',
          600: '#475569',
          500: '#64748B',
        },
        charcoal: {
          900: '#111827',
          800: '#1F2937',
          700: '#374151',
          600: '#4B5563',
        }
      },
      borderRadius: {
        'xl': '0.875rem',
        '2xl': '1.25rem',
        '3xl': '1.75rem',
        '4xl': '2.25rem',
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(225, 29, 72, 0.05)',
        'soft-lg': '0 10px 30px -4px rgba(225, 29, 72, 0.08)',
        'soft-xl': '0 20px 40px -6px rgba(225, 29, 72, 0.12)',
        'glow-pink': '0 0 25px -5px rgba(244, 63, 94, 0.3)',
        'glow-rose': '0 0 30px -5px rgba(251, 113, 133, 0.35)',
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Outfit', 'Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
