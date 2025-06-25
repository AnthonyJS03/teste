"""
SQL query definitions for the dashboard application.
This module contains all the SQL queries used in the project.
"""

# Status query
status = """
SELECT 
    status AS "Status",
    COUNT(*) AS "Quantidade"
FROM emprestimos
WHERE id_escola = %s
GROUP BY status
"""

# Emprestimo aluno query
emprestimo_aluno = """
SELECT 
    e.id,
    e.data_emprestimo,
    EXTRACT(YEAR FROM e.data_emprestimo) AS ano,
    EXTRACT(MONTH FROM e.data_emprestimo) AS mes,
    l.titulo AS livro,
    a.nome AS aluno
FROM emprestimos e
JOIN livros l ON e.id_livro = l.id
JOIN alunos a ON e.id_aluno = a.id
WHERE e.id_escola = %s
"""

# Datas emprestimo query
datas_emp = """
SELECT 
    e.id,
    e.data_emprestimo,
    e.data_devolucao,
    l.titulo,
    a.nome
FROM emprestimos e
JOIN livros l ON e.id_livro = l.id
JOIN alunos a ON e.id_aluno = a.id
WHERE e.id_escola = %s
"""

# Genero mais emprestados query
genero_m_emprestados = """
SELECT 
    g.nome AS "Gênero",
    COUNT(*) AS "Quantidade",
    EXTRACT(YEAR FROM e.data_emprestimo) AS ano,
    EXTRACT(MONTH FROM e.data_emprestimo) AS mes
FROM emprestimos e
JOIN livros l ON e.id_livro = l.id
JOIN generos g ON l.id_genero = g.id
WHERE e.id_escola = %s
GROUP BY g.nome, ano, mes
"""

# Quantidade de livros query
qtd_livros = """
SELECT 
    COUNT(*) AS quantidade
FROM livros
WHERE id_escola = %s
"""

# Quantidade de livros emprestados query
qtd_livro_emprestado = """
SELECT 
    COUNT(*) AS quantidade
FROM emprestimos
WHERE id_escola = %s
AND data_devolucao IS NULL
"""

# Livros mais emprestados query
livros_m_emprestados = """
SELECT 
    l.titulo,
    COUNT(*) AS quantidade
FROM emprestimos e
JOIN livros l ON e.id_livro = l.id
WHERE e.id_escola = %s
GROUP BY l.titulo
ORDER BY quantidade DESC
"""

# Ranking alunos query
ranking_alunos = """
SELECT 
    a.nome,
    COUNT(*) AS quantidade,
    EXTRACT(YEAR FROM e.data_emprestimo) AS ano,
    EXTRACT(MONTH FROM e.data_emprestimo) AS mes
FROM emprestimos e
JOIN alunos a ON e.id_aluno = a.id
WHERE e.id_escola = %s
GROUP BY a.nome, ano, mes
ORDER BY quantidade DESC
"""

# Livros mais emprestados query (with more details)
livros_mais_emprestados_query = """
SELECT 
    l.titulo,
    COUNT(*) AS quantidade,
    EXTRACT(YEAR FROM e.data_emprestimo) AS ano,
    EXTRACT(MONTH FROM e.data_emprestimo) AS mes
FROM emprestimos e
JOIN livros l ON e.id_livro = l.id
WHERE e.id_escola = %s
GROUP BY l.titulo, ano, mes
ORDER BY quantidade DESC
"""

# Quantidade de emprestimos por mes query
qtd_emprestimo_mes = """
SELECT 
    EXTRACT(YEAR FROM data_emprestimo) AS "Ano",
    EXTRACT(MONTH FROM data_emprestimo) AS "Mês",
    COUNT(*) AS "Quantidade"
FROM emprestimos
WHERE id_escola = %s
GROUP BY "Ano", "Mês"
ORDER BY "Ano", "Mês"
"""

# Livros disponiveis query
livros_disponiveis = """
SELECT 
    l.titulo,
    l.id
FROM livros l
LEFT JOIN emprestimos e ON l.id = e.id_livro AND e.data_devolucao IS NULL
WHERE l.id_escola = %s
AND e.id IS NULL
"""

# Livros geral query
livros_geral = """
SELECT 
    (SELECT COUNT(*) FROM livros WHERE id_escola = %s) AS total_geral,
    (SELECT COUNT(*) FROM emprestimos WHERE id_escola = %s AND data_devolucao IS NULL) AS total_livros_emprestados,
    (SELECT COUNT(*) FROM livros WHERE id_escola = %s) - 
    (SELECT COUNT(*) FROM emprestimos WHERE id_escola = %s AND data_devolucao IS NULL) AS livros_disponiveis
"""

# Quantidade por ano query
quantidade_ano = """
SELECT 
    EXTRACT(YEAR FROM data_emprestimo) AS ano,
    COUNT(*) AS quantidade_emprestimos
FROM emprestimos
WHERE id_escola = %s
GROUP BY ano
ORDER BY ano
"""

# Status alunos query
status_alunos = """
SELECT 
    a.nome,
    l.titulo,
    e.data_emprestimo,
    e.data_prevista_devolucao,
    e.status
FROM emprestimos e
JOIN alunos a ON e.id_aluno = a.id
JOIN livros l ON e.id_livro = l.id
WHERE e.id_escola = %s
AND e.data_devolucao IS NULL
"""

# Acervo geral query
acervo_geral = """
SELECT 
    l.titulo,
    g.nome AS genero,
    l.autor,
    l.editora
FROM livros l
JOIN generos g ON l.id_genero = g.id
WHERE l.id_escola = %s
"""

# Genero total query
genero_total = """
SELECT 
    g.nome AS genero,
    COUNT(*) AS quantidade
FROM livros l
JOIN generos g ON l.id_genero = g.id
WHERE l.id_escola = %s
GROUP BY g.nome
ORDER BY quantidade DESC
"""

# Livros total query
livros_total = """
SELECT 
    l.titulo,
    COUNT(*) AS quantidade_emprestimos,
    EXTRACT(YEAR FROM e.data_emprestimo) AS ano,
    EXTRACT(MONTH FROM e.data_emprestimo) AS mes
FROM emprestimos e
JOIN livros l ON e.id_livro = l.id
WHERE e.id_escola = %s
GROUP BY l.titulo, ano, mes
ORDER BY quantidade_emprestimos DESC
"""

# Total alunos query
total_alunos = """
SELECT 
    a.nome,
    COUNT(*) AS quantidade_emprestimos,
    EXTRACT(YEAR FROM e.data_emprestimo) AS ano,
    EXTRACT(MONTH FROM e.data_emprestimo) AS mes
FROM emprestimos e
JOIN alunos a ON e.id_aluno = a.id
WHERE e.id_escola = %s
GROUP BY a.nome, ano, mes
ORDER BY quantidade_emprestimos DESC
"""

# Pessoas com livro query
pessoas_com_livro = """
SELECT DISTINCT
    a.id,
    a.nome,
    a.telefone
FROM alunos a
JOIN emprestimos e ON a.id = e.id_aluno
WHERE a.id_escola = %s
AND e.data_devolucao IS NULL
ORDER BY a.nome
"""

# Pessoas cadastradas query
pessoas_cadastradas = """
SELECT 
    id,
    nome AS "Nome",
    telefone AS "Telefone"
FROM alunos
WHERE id_escola = %s
ORDER BY nome
"""