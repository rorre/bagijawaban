/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,py}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: ["dracula"],
  },
};
