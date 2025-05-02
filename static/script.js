
// Quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    carregarAlunos();
});

// Função para buscar e listar alunos
function carregarAlunos() {
    fetch('/alunos')
        .then(response => response.json())
        .then(alunos => {
            const tabela = document.getElementById('tabela-alunos');
            tabela.innerHTML = '';

            alunos.forEach(aluno => {
                const linha = `
                    <tr>
                        <td>${aluno.idaluno}</td>
                        <td>${aluno.nome}</td>
                        <td>${aluno.email}</td>
                        <td>${aluno.matricula}</td>
                        <td>
                            <a href="/editar_aluno.html?id=${aluno.idaluno}" class="btn btn-warning btn-sm">Editar</a>
                            <button onclick="deletarAluno(${aluno.idaluno})" class="btn btn-danger btn-sm">Excluir</button>
                        </td>
                    </tr>
                `;
                tabela.innerHTML += linha;
            });
        })
        .catch(error => console.error('Erro ao carregar alunos:', error));
}

// Função para deletar aluno
function deletarAluno(id) {
    if (confirm('Tem certeza que deseja excluir este aluno?')) {
        fetch(`/alunos/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensagem);
            carregarAlunos(); // Atualiza a lista
        })
        .catch(error => console.error('Erro ao deletar aluno:', error));
    }
}
