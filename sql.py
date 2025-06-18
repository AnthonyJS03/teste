import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Database connection
def get_db_connection(id_escola):
    # This would be your actual database connection string
    connection_string = "sqlite:///biblioteca.db"  # Example connection string
    return create_engine(connection_string)

# Get the database engine
engine = get_db_connection(None)  # Initialize with None, will be updated with actual id_escola

# SQL queries
status = """
    SELECT 
        status AS Status,
        COUNT(*) AS Quantidade
    FROM emprestimos
    WHERE id_escola = ?
    GROUP BY status
"""

emprestimo_aluno = """
    SELECT 
        e.id, 
        e.aluno_id, 
        a.nome AS aluno,
        e.livro_id, 
        l.titulo AS livro,
        l.genero_id,
        g.nome AS genero,
        strftime('%Y', e.data_emprestimo) AS ano,
        strftime('%m', e.data_emprestimo) AS mes,
        e.data_emprestimo,
        e.data_devolucao
    FROM emprestimos e
    JOIN alunos a ON e.aluno_id = a.id
    JOIN livros l ON e.livro_id = l.id
    JOIN generos g ON l.genero_id = g.id
    WHERE e.id_escola = ?
"""

datas_emp = """
    SELECT 
        data_emprestimo,
        data_devolucao
    FROM emprestimos
    WHERE id_escola = ?
"""

genero_m_emprestados = """
    SELECT 
        g.nome AS "Gênero",
        COUNT(*) AS Quantidade,
        strftime('%Y', e.data_emprestimo) AS ano,
        strftime('%m', e.data_emprestimo) AS mes
    FROM emprestimos e
    JOIN livros l ON e.livro_id = l.id
    JOIN generos g ON l.genero_id = g.id
    WHERE e.id_escola = ?
    GROUP BY g.nome, ano, mes
"""

qtd_livros = """
    SELECT 
        COUNT(*) AS quantidade
    FROM livros
    WHERE id_escola = ?
"""

qtd_livro_emprestado = """
    SELECT 
        COUNT(*) AS quantidade
    FROM emprestimos
    WHERE id_escola = ?
"""

livros_m_emprestados = """
    SELECT 
        l.titulo,
        COUNT(*) AS quantidade
    FROM emprestimos e
    JOIN livros l ON e.livro_id = l.id
    WHERE e.id_escola = ?
    GROUP BY l.titulo
    ORDER BY quantidade DESC
"""

ranking_alunos = """
    SELECT 
        a.nome,
        COUNT(*) AS quantidade_emprestimos,
        strftime('%Y', e.data_emprestimo) AS ano,
        strftime('%m', e.data_emprestimo) AS mes
    FROM emprestimos e
    JOIN alunos a ON e.aluno_id = a.id
    WHERE e.id_escola = ?
    GROUP BY a.nome, ano, mes
    ORDER BY quantidade_emprestimos DESC
"""

livros_mais_emprestados_query = """
    SELECT 
        l.titulo,
        COUNT(*) AS quantidade_emprestimos,
        strftime('%Y', e.data_emprestimo) AS ano,
        strftime('%m', e.data_emprestimo) AS mes
    FROM emprestimos e
    JOIN livros l ON e.livro_id = l.id
    WHERE e.id_escola = ?
    GROUP BY l.titulo, ano, mes
    ORDER BY quantidade_emprestimos DESC
"""

qtd_emprestimo_mes = """
    SELECT 
        strftime('%Y', data_emprestimo) AS Ano,
        strftime('%m', data_emprestimo) AS Mês,
        COUNT(*) AS Quantidade
    FROM emprestimos
    WHERE id_escola = ?
    GROUP BY Ano, Mês
"""

livros_disponiveis = """
    SELECT 
        COUNT(*) AS livros_disponiveis
    FROM livros
    WHERE id NOT IN (SELECT livro_id FROM emprestimos WHERE data_devolucao IS NULL)
    AND id_escola = ?
"""

livros_geral = """
    SELECT 
        (SELECT COUNT(*) FROM emprestimos WHERE id_escola = ?) AS total_livros_emprestados,
        (SELECT COUNT(*) FROM livros WHERE id NOT IN (SELECT livro_id FROM emprestimos WHERE data_devolucao IS NULL) AND id_escola = ?) AS livros_disponiveis,
        (SELECT COUNT(*) FROM livros WHERE id_escola = ?) AS total_geral
"""

quantidade_ano = """
    SELECT 
        strftime('%Y', data_emprestimo) AS ano,
        COUNT(*) AS quantidade_emprestimos
    FROM emprestimos
    WHERE id_escola = ?
    GROUP BY ano
"""

status_alunos = """
    SELECT 
        a.nome AS "Nome",
        l.titulo AS "Título",
        e.data_emprestimo AS "Data de empréstimo",
        e.data_devolucao AS "Data de devolução",
        e.status AS "Status"
    FROM emprestimos e
    JOIN alunos a ON e.aluno_id = a.id
    JOIN livros l ON e.livro_id = l.id
    WHERE e.id_escola = ?
"""

acervo_geral = """
    SELECT 
        l.titulo AS "Título",
        g.nome AS "Gênero",
        a.nome AS "Autor"
    FROM livros l
    JOIN generos g ON l.genero_id = g.id
    JOIN autores a ON l.autor_id = a.id
    WHERE l.id_escola = ?
"""

genero_total = """
    SELECT 
        g.nome AS "Gênero",
        COUNT(*) AS "Quantidade"
    FROM livros l
    JOIN generos g ON l.genero_id = g.id
    WHERE l.id_escola = ?
    GROUP BY g.nome
"""

livros_total = """
    SELECT 
        l.titulo,
        COUNT(*) AS quantidade_emprestimos,
        strftime('%Y', e.data_emprestimo) AS ano,
        strftime('%m', e.data_emprestimo) AS mes
    FROM emprestimos e
    JOIN livros l ON e.livro_id = l.id
    WHERE e.id_escola = ?
    GROUP BY l.titulo, ano, mes
    ORDER BY quantidade_emprestimos DESC
"""

total_alunos = """
    SELECT 
        a.nome,
        COUNT(*) AS quantidade_emprestimos,
        strftime('%Y', e.data_emprestimo) AS ano,
        strftime('%m', e.data_emprestimo) AS mes
    FROM emprestimos e
    JOIN alunos a ON e.aluno_id = a.id
    WHERE e.id_escola = ?
    GROUP BY a.nome, ano, mes
    ORDER BY quantidade_emprestimos DESC
"""

pessoas_com_livro = """
    SELECT DISTINCT
        a.id,
        a.nome AS "Nome",
        a.telefone AS "Telefone"
    FROM emprestimos e
    JOIN alunos a ON e.aluno_id = a.id
    WHERE e.data_devolucao IS NULL
    AND e.id_escola = ?
"""

pessoas_cadastradas = """
    SELECT 
        id,
        nome AS "Nome",
        telefone AS "Telefone"
    FROM alunos
    WHERE id_escola = ?
"""