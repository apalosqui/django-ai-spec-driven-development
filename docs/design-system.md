# Design system (diretrizes)

Visão geral
- Tema escuro, moderno, com gradientes e paleta harmônica.
- Implementação com TailwindCSS via CDN nos templates DTL (quando criados).

Cores e tipografia
- Fundo: `slate-900`/`slate-950`; Texto: `slate-100`.
- Gradiente primário: `from-indigo-500 via-purple-500 to-sky-500`.
- Fonte: `Inter`, fallback `ui-sans-serif, system-ui`.

Componentes (classes sugeridas)
- Botão primário: `inline-flex items-center px-4 py-2 rounded-md bg-gradient-to-r from-indigo-500 to-sky-500 text-white hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-indigo-400`.
- Input padrão: `bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-indigo-400 focus:border-transparent`.
- Card/container: `bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl shadow`.
- Grid responsivo: `grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4`.
- Navbar: `bg-slate-950/70 border-b border-slate-800`.

Exemplo de uso (DTL)
```html
<nav class="bg-slate-950/70 border-b border-slate-800">
  <div class="container mx-auto px-4 py-3 flex justify-between">
    <a href="/" class="text-slate-100 font-semibold">Finanpy</a>
    {% if user.is_authenticated %}
      <a class="inline-flex items-center px-4 py-2 rounded-md bg-gradient-to-r from-indigo-500 to-sky-500 text-white" href="{% url 'logout' %}">Sair</a>
    {% else %}
      <a class="inline-flex items-center px-4 py-2 rounded-md bg-gradient-to-r from-indigo-500 to-sky-500 text-white" href="{% url 'login' %}">Entrar</a>
    {% endif %}
  </div>
</nav>
```

Observação
- Estas diretrizes descrevem o padrão visual a ser aplicado conforme os templates forem implementados. Consulte o `PRD.md` para contexto de UX.
