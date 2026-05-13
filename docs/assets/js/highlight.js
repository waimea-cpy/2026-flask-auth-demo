document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('code').forEach(block => {
        const parent = block.closest('div[class*="language-"]')
        if (parent) {
            const langClass = Array.from(parent.classList).find(c => c.startsWith('language-'))
            if (langClass) {
                block.classList.add(langClass)
                hljs.highlightElement(block)
                return
            }
        }
        block.classList.add('language-plaintext')
        hljs.highlightElement(block)
    })
})

