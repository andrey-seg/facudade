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
(1,1, 1, "Projeto Bioluz", "Estudo sobre fotossíntese", "2026-01-10", "2026-08-10"),
(2,2, 2, "Física Aplicada", "Experimentos com luz", "2026-02-01", "2026-09-01"),
(3,3, 3, "Laboratório Química", "Reações com papel indicador", "2025-03-0", "2025-08-10"),
(4,4, 4, "Matemática Visual", "Geometria com recursos", "2025-04-01", "2025-09-0"),
(5,5, 5, "Computação Móvel", "Uso de notebooks em aulas", "2025-05-15", "2025-10-15");

SELECT * FROM atividade
insert into atividade values
(1,1, "Coleta de Dados", "2026-06-15", "2026-07-15"),
(2,2, "Experimento 1", "2026-05-10", "2026-08-10"),
(3,3, "Teste de Reações", "2026-05-20", "2026-08-20"),
(4,4, "Aula Prática", "2026-04-10", "2026-09-10"),
(5,5, "Montagem de Ambiente", "2026-05-20", "2026-10-20");

SELECT * FROM aluno_voluntario
insert into aluno_voluntario values
(1,"Beatriz Ramos", "Biologia"),
(2,"Eduardo Costa", "Física"),
(3,"Fernanda Melo", "Química"),
(4,"Lucas Rocha", "Matemática"),
(5,"Rafaela Dias", "Computação");

CREATE TABLE gerenciamento_projeto(
    id_orientador INT UNSIGNED NOT NULL,
    nome_orientador VARCHAR(40) NOT NULL,
    atividade_orientador VARCHAR(80) NOT NULL,
);

SELECT * FROM gerenciamento_projeto
insert into gerenciamento_projeto values
(1, "Ricardo Almeida", "Engenharia")
(2, "Juliana Martins", "Robótica")
(3, "Fernando Oliveira", "Estatística")
(4, "Camila Rodrigues", "Educação")
(5, "Rafael Mendes", "Inteligência Artificial")
(6, "Luciana Ferreira", "Astronomia")
(7, "Gustavo Pereira", "Tecnologia")

/* A) Consulta de atividades com data de término a partir de uma data específica:
Esta consulta retorna todas as atividades que têm uma data de término posterior
a 20 de abril de 2025.*/

SELECT * FROM atividade
WHERE data_fim > '09-02-2000';

/* B) Retorne a unidade e quantidade em estoque de todos os materiais na tabela
Material, cuja quantidade seja superior a 100.*/

SELECT * materiais
WHERE quantidade > 100;

/* C) Consulta para exibir o nome de professores e área de atuação na tabela
Professor, que não são da área de atuação Física.*/

SELECT nome, area_atuacao FROM professor
WHERE area_atuacao <> 'fisica';

/* D) Localizar todos os projetos que estão atualmente em andamento. Um projeto é
considerado "em andamento" se a data atual estiver entre sua data de início e de
fim */

SELECT * FORM Projeto
WHERE data_inicio < data_fim < '04-09-2026';
