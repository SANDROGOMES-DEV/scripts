document.addEventListener('DOMContentLoaded', () => {
    const btnMenu = document.getElementById('btnMenu');
    const menuDiagonal = document.getElementById('menuDiagonal');

    btnMenu.addEventListener('click', () => {
        // Adiciona ou remove a classe que mostra o menu
        menuDiagonal.classList.toggle('aberto');

        // Opcional: Animação simples no botão (muda a cor ao abrir)
        if (menuDiagonal.classList.contains('aberto')) {
            btnMenu.style.background = '#b21f1f';
        } else {
            btnMenu.style.background = '#333';
        }
    });

    // Fecha o menu se o usuário clicar em um link
    const links = document.querySelectorAll('.nav-link a');
    links.forEach(link => {
        link.addEventListener('click', () => {
            menuDiagonal.classList.remove('aberto');
        });
    });
});
