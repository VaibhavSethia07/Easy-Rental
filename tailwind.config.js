module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "60vh": "60vh",
        "75vh": "75vh",
      },

      borderRadius: {
        xxl: "1.5rem",
      },

      keyframes: {
        messageFadeIn: {
          '0%': { opacity: '0'},
          '5%': { opacity: '1'},
          '95%': { opacity: '1'},
          '100%': { opacity: '0'},
        }
      },

      animation: {
        'messageFadeIn': 'messageFadeIn 2s ease-in-out forwards'
      },
    },
    variants: {},
    plugins: [],
  }
}
