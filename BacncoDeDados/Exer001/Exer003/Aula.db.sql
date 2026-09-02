CREATE DATABASE gerenciamento_projetos;
USE gerenciamento_projetos;

CREATE TABLE professor (
    id_professor   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome_professor VARCHAR(60) NOT NULL,
    area_atuacao   VARCHAR(30) DEFAULT 'Tecnologia',
    PRIMARY KEY (id_professor),
    UNIQUE (nome_professor)
);

CREATE TABLE recurso (
    id_recurso INT UNSIGNED NOT NULL auto_increment,
    nome VARCHAR(50) NOT NULL,
    tipo ENUM('equipamento', 'material') NOT NULL,
    PRIMARY KEY (id_recurso),
    INDEX idx_tipo_recurso (tipo)
);

CREATE TABLE equipamento (
    id_equipamento INT UNSIGNED NOT NULL,
    numero_serie   VARCHAR(40) NOT NULL,
    garantia_anos  INT DEFAULT 1,
    PRIMARY KEY (id_equipamento),
    UNIQUE (numero_serie),
    INDEX idx_numero_serie (numero_serie),
    CHECK (garantia_anos >= 0),
    FOREIGN KEY (id_equipamento) REFERENCES recurso (id_recurso)
);

CREATE TABLE material (
    id_material INT UNSIGNED NOT NULL,
    unidade     VARCHAR(20) DEFAULT 'Unidade',
    quantidade  INT DEFAULT 1,
    PRIMARY KEY (id_material),
    CHECK (quantidade > 0),
    FOREIGN KEY (id_material) REFERENCES recurso (id_recurso)
);

CREATE TABLE projeto (
    id_projeto    INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_professor  INT UNSIGNED NOT NULL,
    id_recurso    INT UNSIGNED NOT NULL,
    titulo        VARCHAR(38) NOT NULL,
    descricao     TEXT,
    data_inicio   DATE NOT NULL,
    data_fim      DATE NOT NULL,
    PRIMARY KEY (id_projeto),
    INDEX idx_titulo_projeto (titulo),
    INDEX idx_projeto_professor (id_professor),
    INDEX idx_projeto_recurso (id_recurso),
    FOREIGN KEY (id_professor) REFERENCES professor (id_professor),
    FOREIGN KEY (id_recurso)   REFERENCES recurso (id_recurso),
    CHECK (data_fim > data_inicio)
);

CREATE TABLE atividade (
    id_atividade   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_projeto     INT UNSIGNED NOT NULL,
    nome_atividade VARCHAR(60) NOT NULL,
    data_inicio    DATE NOT NULL,
    data_fim       DATE NOT NULL,
    PRIMARY KEY (id_atividade),
    INDEX idx_nome_atividade (nome_atividade),
    INDEX idx_atividade_projeto (id_projeto),
    FOREIGN KEY (id_projeto) REFERENCES projeto (id_projeto),
    CHECK (data_fim >= data_inicio)
);

CREATE TABLE aluno_voluntario (
    id_aluno   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome_aluno VARCHAR(60) NOT NULL,
    curso      VARCHAR(30) DEFAULT 'Informática',
    PRIMARY KEY (id_aluno),
    UNIQUE (nome_aluno),
    INDEX idx_curso_aluno (curso)
);

CREATE TABLE atividade_aluno (
    id_atividade INT UNSIGNED NOT NULL,
    id_aluno     INT UNSIGNED NOT NULL,
    PRIMARY KEY (id_atividade, id_aluno),
    INDEX idx_atividade_aluno (id_aluno),
    FOREIGN KEY (id_atividade) REFERENCES atividade (id_atividade),
    FOREIGN KEY (id_aluno)     REFERENCES aluno_voluntario (id_aluno)
);

-- para 22/08
-- a) Adicionar a coluna e-mail na tabela professor do tipo string de tamanho 40
ALTER TABLE professor ADD email VARCHAR(30);
ALTER TABLE professor MODIFY email VARCHAR(40); -- errei

-- b) Alterar o atributo área de atuação para especialidade da tabela professor mudar o tipo para VARCHAR(50).
ALTER TABLE professor CHANGE area_atuacao especialidade VARCHAR(50);

-- c) Alterar apenas o tipo de dados da coluna numero_serie do tipo string de tamanho (40) para string de tamanho (60) na tabela equipamento.
ALTER TABLE equipamento MODIFY numero_serie VARCHAR(60);

-- d) Excluir o atributo e-mail da tabela professor.
ALTER TABLE professor DROP email;

-- e) Criar um índice chamado idx_nome_professor na tabela professor para o atributo nome do professor.
CREATE INDEX idx_nome_professor ON professor (nome_professor);

-- f) Adicionar o atributo status com valor padrão 'Ativo' na tabela professor.
ALTER TABLE professor ADD status VARCHAR(15) DEFAULT 'Ativo';

-- g) Excluir o atributo status da tabela professor
ALTER TABLE professor DROP status;

SELECT * FROM professor;
insert into professor values
(1,"Ana Lima", "Biologia",),
(2,"Carlos Souza", "Física",),
(3,"Marina Torres", "Química",),
(4,"João Silva", "Matemática",),
(5,"Patrícia Gomes", "Computação")

select * from recurso
insert into recurso values
(1,"Microscópio", "Equipamento"),
(2,"Projetor", "Equipamento"),
(3,"Papel A4", "Material"),
(4,"Caneta", "Material"),
(5,"Notebook", "Equipamento");

SELECT * FROM equipamento;
insert into equipamento values
(1, 'MIC12345', 2),
(2, 'PRO67934', 3),
(5, 'NOTE0937', 1);

select * from material
insert into material values
(1, "Resma", 20),
(2, "Unidade", 100);

select * from projeto
insert into projeto values
(1,1, 1, Projeto Bioluz, Estudo sobre fotossíntese, 2026-01-10, 2026-08-10),
(2,2, 2, Física Aplicada, Experimentos com luz, 2026-02-01, 2026-09-01),
(3,3, 3, Laboratório Química, Reações com papel indicador, 2025-03-0, 2025-08-10),
(4,4, 4, Matemática Visual, Geometria com recursos, 2025-04-01, 2025-09-0),
(5,5, 5, Computação Móvel, Uso de notebooks em aulas, 2025-05-15, 2025-10-15);
