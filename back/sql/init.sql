CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    description VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    priority UNSIGNED TINYINT,
    status UNSIGNED TINYINT,
    creation_date DATE,
    end_date DATE,
    was_made_by VARCHAR(50) NOT NULL,
    FOREIGN KEY (was_made_by) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50),
    password VARCHAR(50),
    name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    surname VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    email VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    role UNSIGNED TINYINT
);

CREATE TABLE IF NOT EXISTS tags (
    name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci PRIMARY KEY,
    colour UNSIGNED TINYINT
);

CREATE TABLE IF NOT EXISTS subtasks (
    id_subtask INT NOT NULL,
    id_task INT NOT NULL,
    FOREIGN KEY (id_subtask) REFERENCES tasks(id),
    FOREIGN KEY (id_task) REFERENCES tasks(id),
    PRIMARY KEY (id_subtask, id_task)
);

CREATE TABLE IF NOT EXISTS hasTag (
    id_task INT NOT NULL,
    tag_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
    FOREIGN KEY (id_task) REFERENCES tasks(id),
    FOREIGN KEY (tag_name) REFERENCES tags(name),
    PRIMARY KEY (id_task, tag_name)
);

CREATE TABLE IF NOT EXISTS assignedTo (
    id_task INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_task) REFERENCES tasks(id),
    FOREIGN KEY (username) REFERENCES users(username)
    PRIMARY KEY (id_task, username)
);


# Inserto valores de ejemplo
INSERT INTO users(username, password, name, surname, email, role) 
VALUES ("ivetrano", "pass123", "Ignacio", "Vetrano", "ignaciovetrano00@gmail.com", 0);

INSERT INTO tags(name, colour) VALUES ("Programacion", 0);
INSERT INTO tags(name, colour) VALUES ("Diseño", 1);
INSERT INTO tags(name, colour) VALUES ("Proyectos", 2);

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
VALUES ("Programar un CRUD de tareas", 
"Programar un CRUD de tareas para demostrar mis conocimientos con tecnologias web.",
0, 1, "2024-12-09", "2025-01-31", "ivetrano");

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
VALUES ("Programar el backend",
"Programar el backend con Python, Flask, y MySQL.",
0, 1, "2024-12-09", "2025-01-31", "ivetrano");

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
VALUES ("Diseñar la base de datos",
"Diseñar la base de datos en MySQL para poder gestionar las tareas.",
0, 2, "2024-12-09", "2024-12-09", "ivetrano");

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
VALUES ("Programar la API",
"Programar la API con Python, utilizando Flask.",
0, 1, "2024-12-09", "2025-01-31", "ivetrano");

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
VALUES ("Programar el frontend",
"Programar el frontend con Javasript y React.",
0, 0, "2024-12-09", "2025-01-31", "ivetrano");

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
VALUES ("Diseñar el frontend",
"Diseñar el frontend para que sea agradable, intuitivo, y responsive.",
0, 0, "2024-12-09", "2025-01-31", "ivetrano");


INSERT INTO subtasks(id_subtask, id_task) VALUES (2, 1);
INSERT INTO subtasks(id_subtask, id_task) VALUES (5, 1);
INSERT INTO subtasks(id_subtask, id_task) VALUES (3, 2);
INSERT INTO subtasks(id_subtask, id_task) VALUES (4, 2);
INSERT INTO subtasks(id_subtask, id_task) VALUES (6, 5);

INSERT INTO assignedTo(id_task, username) VALUES (1, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (2, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (3, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (4, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (5, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (6, "ivetrano");

INSERT INTO hasTag(id_task, tag_name) VALUES (1, "Proyectos");
INSERT INTO hasTag(id_task, tag_name) VALUES (2, "Programacion");
INSERT INTO hasTag(id_task, tag_name) VALUES (4, "Programacion");
INSERT INTO hasTag(id_task, tag_name) VALUES (5, "Programacion");
INSERT INTO hasTag(id_task, tag_name) VALUES (3, "Diseño");
INSERT INTO hasTag(id_task, tag_name) VALUES (6, "Diseño");