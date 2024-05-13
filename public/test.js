// Função para modificar o atributo aria-label
function modificarAriaLabel() {
    // Seleciona o botão pelo seletor de classe
    var botao = document.querySelector('.MuiIconButton-root[aria-label="Copy"]');
    
    // Verifica se o botão foi encontrado
    if (botao) {
        console.log("Encontrado");
        // Define o novo valor para o atributo aria-label
        botao.setAttribute('aria-label', 'Copiar');
    } else {
        console.log("Não");
    }
}

function alterarConteudoParagrafo() {
    // Seleciona o elemento <p> pelo seletor de classe
    var paragrafos = document.querySelectorAll('p.MuiTypography-root.MuiTypography-body1.MuiTypography-noWrap.css-3my8qy');

    // Itera sobre todos os parágrafos encontrados
    paragrafos.forEach(function(paragrafo) {
        // Define o novo conteúdo para cada parágrafo
        if(paragrafo.textContent === "You"){
            paragrafo.textContent = "Usuário";
        }
    });

    // Verifica se pelo menos um parágrafo foi encontrado
    if (paragrafos.length === 0) {
        console.log("Nenhum parágrafo encontrado com a classe especificada");
    }
}

// //MuiStack-root css-149sczi
// function alterarConteudoFeedback() {
//     // Seleciona o elemento <p> pelo seletor de classe
//     var paragrafos = document.querySelectorAll('div.MuiStack-root css-149sczi');

//     // Itera sobre todos os parágrafos encontrados
//     paragrafos.forEach(function(paragrafo) {
//         // Define o novo conteúdo para cada parágrafo
//         if(paragrafo.textContent === "Provide additional feedback"){
//             paragrafo.textContent = "Usuário";
//         }
//     });

//     // Verifica se pelo menos um parágrafo foi encontrado
//     if (paragrafos.length === 0) {
//         console.log("Nenhum parágrafo encontrado com a classe especificada");
//     }
// }

// Executa a função a cada 5 segundos
// setInterval(modificarAriaLabel, 5000);
setInterval(alterarConteudoParagrafo, 1000);


