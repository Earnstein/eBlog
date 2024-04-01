/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      screens: {
        '2xl': {'max': '1535px'},
        'xl': {'max': '1279px'},
        'lg': {'max': '1023px'},
        'md': {'max': '767px'},
        'sm': {'max': '639px'},
      },
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
        "playfair": ["Playfair Display", "serif"],
        'inter': ['Inter', 'sans-serif'],
      }      
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}