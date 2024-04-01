/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      screens: {
        xs:"480px",
        ss: "620px",
        sm: "768px",
        md: "1060px",
        wide: "1440px",
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