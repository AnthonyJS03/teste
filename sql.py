import sqlalchemy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection parameters from environment variables
# Default values are provided as fallbacks
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "biblioteca")

# Create database connection string
connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine for database connections
engine = sqlalchemy.create_engine(connection_string)

# Define SQL queries used in the application
status = """
    SELECT 
        CASE WHEN status = 'EM_ATRASO' THEN 'ATRASADO' ELSE status END AS "Status",
        COUNT(*) AS "Quantidade"
    FROM emprestimo
    WHERE id_escola = %s AND devolvido = false
    GROUP BY status
"""

emprestimo_aluno = """
    SELECT 
        e.id, 
        a.nome as aluno,
        l.titulo as livro,
        EXTRACT(YEAR FROM e.data_emprestimo) as ano,
        EXTRACT(MONTH FROM e.data_emprestimo) as mes
    FROM emprestimo e
    JOIN aluno a ON e.id_aluno = a.id
    JOIN livro l ON e.id_livro = l.id
    WHERE e.id_escola = %s
"""

datas_emp = """
    SELECT 
        e.id, 
        e.data_emprestimo,
        e.data_devolucao_prevista
    FROM emprestimo e
    WHERE e.id_escola = %s
"""

genero_m_emprestados = """
    SELECT 
        g.nome as "Gênero",
        COUNT(*) as "Quantidade",
        EXTRACT(YEAR FROM e.data_emprestimo) as ano,
        EXTRACT(MONTH FROM e.data_emprestimo) as mes
    FROM emprestimo e
    JOIN livro l ON e.id_livro = l.id
    JOIN genero g ON l.id_genero = g.id
    WHERE e.id_escola = %s
    GROUP BY g.nome, ano, mes
"""

qtd_livros = """
    SELECT COUNT(*) as quantidade
    FROM livro
    WHERE id_escola = %s
"""

qtd_livro_emprestado = """
    SELECT COUNT(*) as quantidade
    FROM emprestimo
    WHERE id_escola = %s AND devolvido = false
"""

livros_m_emprestados = """
    SELECT 
        l.titulo,
        COUNT(*) as quantidade
    FROM emprestimo e
    JOIN livro l ON e.id_livro = l.id
    WHERE e.id_escola = %s
    GROUP BY l.titulo
    ORDER BY quantidade DESC
"""

ranking_alunos = """
    SELECT 
        a.nome,
        COUNT(*) as quantidade,
        EXTRACT(YEAR FROM e.data_emprestimo) as ano,
        EXTRACT(MONTH FROM e.data_emprestimo) as mes
    FROM emprestimo e
    JOIN aluno a ON e.id_aluno = a.id
    WHERE e.id_escola = %s
    GROUP BY a.nome, ano, mes
    ORDER BY quantidade DESC
"""

livros_mais_emprestados_query = """
    SELECT 
        l.titulo,
        COUNT(*) as quantidade,
        EXTRACT(YEAR FROM e.data_emprestimo) as ano,
        EXTRACT(MONTH FROM e.data_emprestimo) as mes
    FROM emprestimo e
    JOIN livro l ON e.id_livro = l.id
    WHERE e.id_escola = %s
    GROUP BY l.titulo, ano, mes
    ORDER BY quantidade DESC
"""

qtd_emprestimo_mes = """
    SELECT 
        EXTRACT(YEAR FROM data_emprestimo) as "Ano",
        EXTRACT(MONTH FROM data_emprestimo) as "Mês",
        COUNT(*) as "Quantidade"
    FROM emprestimo
    WHERE id_escola = %s
    GROUP BY "Ano", "Mês"
"""

livros_disponiveis = """
    SELECT COUNT(*) as disponiveis
    FROM livro l
    WHERE l.id_escola = %s
    AND l.id NOT IN (
        SELECT id_livro FROM emprestimo WHERE devolvido = false AND id_escola = %s
    )
"""

livros_geral = """
    SELECT 
        (SELECT COUNT(*) FROM livro WHERE id_escola = %s) as total_geral,
        (SELECT COUNT(*) FROM emprestimo WHERE devolvido = false AND id_escola = %s) as total_livros_emprestados,
        (
            SELECT COUNT(*) FROM livro l
            WHERE l.id_escola = %s
            AND l.id NOT IN (
                SELECT id_livro FROM emprestimo WHERE devolvido = false AND id_escola = %s
            )
        ) as livros_disponiveis
"""

quantidade_ano = """
    SELECT 
        EXTRACT(YEAR FROM data_emprestimo) as ano,
        COUNT(*) as quantidade_emprestimos
    FROM emprestimo
    WHERE id_escola = %s
    GROUP BY ano
"""

status_alunos = """
    SELECT 
        a.nome,
        l.titulo,
        e.data_emprestimo,
        e.data_devolucao_prevista,
        CASE
            WHEN e.status = 'EM_ATRASO' THEN 'Em atraso'
            ELSE 'Em dia'
        END as status
    FROM emprestimo e
    JOIN aluno a ON e.id_aluno = a.id
    JOIN livro l ON e.id_livro = l.id
    WHERE e.id_escola = %s AND e.devolvido = false
"""

acervo_geral = """
    SELECT 
        l.titulo,
        g.nome as genero,
        CASE
            WHEN l.id IN (SELECT id_livro FROM emprestimo WHERE devolvido = false AND id_escola = %s) THEN 'Emprestado'
            ELSE 'Disponível'
        END as status
    FROM livro l
    JOIN genero g ON l.id_genero = g.id
    WHERE l.id_escola = %s
"""

genero_total = """
    SELECT 
        g.nome as genero,
        COUNT(*) as quantidade
    FROM livro l
    JOIN genero g ON l.id_genero = g.id
    WHERE l.id_escola = %s
    GROUP BY g.nome
"""

livros_total = """
    SELECT 
        l.titulo,
        COUNT(*) as quantidade_emprestimos,
        EXTRACT(YEAR FROM e.data_emprestimo) as ano,
        EXTRACT(MONTH FROM e.data_emprestimo) as mes
    FROM emprestimo e
    JOIN livro l ON e.id_livro = l.id
    WHERE e.id_escola = %s
    GROUP BY l.titulo, ano, mes
    ORDER BY quantidade_emprestimos DESC
"""

total_alunos = """
    SELECT 
        a.nome,
        COUNT(*) as quantidade_emprestimos,
        EXTRACT(YEAR FROM e.data_emprestimo) as ano,
        EXTRACT(MONTH FROM e.data_emprestimo) as mes
    FROM emprestimo e
    JOIN aluno a ON e.id_aluno = a.id
    WHERE e.id_escola = %s
    GROUP BY a.nome, ano, mes
    ORDER BY quantidade_emprestimos DESC
"""

pessoas_com_livro = """
    SELECT DISTINCT
        a.id,
        a.nome,
        a.telefone
    FROM aluno a
    JOIN emprestimo e ON a.id = e.id_aluno
    WHERE e.id_escola = %s AND e.devolvido = false
"""

pessoas_cadastradas = """
    SELECT 
        id,
        nome,
        telefone
    FROM aluno
    WHERE id_escola = %s
"""