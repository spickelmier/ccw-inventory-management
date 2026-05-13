/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        'surface-base':    '#020617',
        'surface-card':    '#0f172a',
        'surface-raised':  '#1e293b',
        'surface-overlay': '#334155',
        'border-subtle':   '#1e293b',
        'border-default':  '#334155',
        'text-primary':    '#f8fafc',
        'text-secondary':  '#94a3b8',
        'text-muted':      '#64748b',
        'accent':          '#6366f1',
        'accent-hover':    '#818cf8',
        'status-success':  '#34d399',
        'status-warning':  '#fbbf24',
        'status-danger':   '#f87171',
        'status-info':     '#60a5fa',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
