import { ref, onMounted } from 'vue'

const theme = ref('light')

export function useTheme() {
  function updateThemeOnHtmlEl(newTheme) {
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  function toggleTheme() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem('theme', theme.value)
    updateThemeOnHtmlEl(theme.value)
  }

  onMounted(() => {
    const savedTheme = localStorage.getItem('theme')
    theme.value = savedTheme ? savedTheme : 'light'
    updateThemeOnHtmlEl(theme.value)
  })

  return { theme, toggleTheme }
}
