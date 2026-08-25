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
    id_recurso INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome       VARCHAR(50) NOT NULL,
    tipo       ENUM('equipamento', 'material') NOT NULL,
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
/* a) Adicionar a coluna e-mail na tabela professor do tipo string de tamanho 40 */
ALTER TABLE professor ADD email varchar(45)

/*b) Alterar o atributo área de atuação para especialidade da tabela professor mudar o tipo para VARCHAR(50).*/
ALTER TABLE professor CHANGE  area_atuacao especialidade VARCHAR(50)

/*c) Alterar apenas o tipo de dados da coluna numero_serie do tipo string de tamanho (40) para string de tamanho (60) na tabela equipamento.*/
ALTER TABLE equipamento MODIFY numero_serie VARCHAR(60)

/*d) Excluir o atributo e-mail da tabela professor.*/
ALTER TABLE professor DROP email

/*e) Criar um índice chamado idx_nome_professor na tabela professor para o atributo nome do professor.*/
CREATE INDEX idx_nome_professor ON professor (nome_professor)

/*f) Adicionar o atributo status com valor padrão 'Ativo' na tabela professor*/
ALTER TABLE professor ADD status VARCHAR(15) DEFAULT 'ativo'

/*g) Excluir o atributo status da tabela professor*/
ALTER TABLE professor DROP status