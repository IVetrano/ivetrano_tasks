DROP DATABASE IF EXISTS ivetranotask$default;
CREATE DATABASE ivetranotask$default;
USE ivetranotask$default;

-- Primero creamos la tabla de usuarios (necesaria para las FK de tasks)
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    email VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    role VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci
);

-- Luego creamos la tabla de tareas
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    description VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
    priority TINYINT UNSIGNED,
    status TINYINT UNSIGNED,
    creation_date DATE DEFAULT (CURRENT_DATE),
    end_date DATE,
    was_made_by VARCHAR(50) NOT NULL,
    id_parent INT DEFAULT NULL,
    FOREIGN KEY (was_made_by) REFERENCES users(username),
    FOREIGN KEY (id_parent) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Ahora creamos la tabla de etiquetas
CREATE TABLE IF NOT EXISTS tags (
    name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci PRIMARY KEY,
    colour TINYINT UNSIGNED
);

-- Relación entre tareas y etiquetas
CREATE TABLE IF NOT EXISTS hasTag (
    id_task INT NOT NULL,
    tag_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
    FOREIGN KEY (id_task) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_name) REFERENCES tags(name),
    PRIMARY KEY (id_task, tag_name)
);

-- Relación entre tareas y usuarios asignados
CREATE TABLE IF NOT EXISTS assignedTo (
    id_task INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_task) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users(username),
    PRIMARY KEY (id_task, username)
);

-- Inserción de datos de prueba
INSERT INTO users(username, password, name, email, role) 
VALUES ("ivetrano", "pass123", "Ignacio Vetrano", "ignaciovetrano00@gmail.com", "admin");

INSERT INTO tags(name, colour) VALUES ("Programacion", 0);
INSERT INTO tags(name, colour) VALUES ("Diseño", 1);
INSERT INTO tags(name, colour) VALUES ("Proyectos", 2);

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by)
VALUES ("Programar un CRUD de tareas", 
        "Programar un CRUD de tareas para demostrar mis conocimientos con tecnologías web.",
        0, 1, "2024-12-09", "2025-01-31", "ivetrano");

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by, id_parent)
VALUES ("Programar el backend",
        "Programar el backend con Python, Flask, y MySQL.",
        0, 1, "2024-12-09", "2025-01-31", "ivetrano", 1);

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by, id_parent)
VALUES ("Diseñar la base de datos",
        "Diseñar la base de datos en MySQL para poder gestionar las tareas.",
        0, 2, "2024-12-09", "2024-12-09", "ivetrano", 2);

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by, id_parent)
VALUES ("Programar la API",
        "Programar la API con Python, utilizando Flask.",
        0, 1, "2024-12-09", "2025-01-31", "ivetrano", 2);

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by, id_parent)
VALUES ("Programar el frontend",
        "Programar el frontend con JavaScript y React.",
        0, 0, "2024-12-09", "2025-01-31", "ivetrano", 1);

INSERT INTO tasks(title, description, priority, status, creation_date, end_date, was_made_by, id_parent)
VALUES ("Diseñar el frontend",
        "Diseñar el frontend para que sea agradable, intuitivo y responsive.",
        0, 0, "2024-12-09", "2025-01-31", "ivetrano", 5);

-- Asignación de tareas
INSERT INTO assignedTo(id_task, username) VALUES (1, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (2, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (3, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (4, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (5, "ivetrano");
INSERT INTO assignedTo(id_task, username) VALUES (6, "ivetrano");

-- Asignación de etiquetas
INSERT INTO hasTag(id_task, tag_name) VALUES (1, "Proyectos");
INSERT INTO hasTag(id_task, tag_name) VALUES (2, "Programacion");
INSERT INTO hasTag(id_task, tag_name) VALUES (4, "Programacion");
INSERT INTO hasTag(id_task, tag_name) VALUES (5, "Programacion");
INSERT INTO hasTag(id_task, tag_name) VALUES (3, "Diseño");
INSERT INTO hasTag(id_task, tag_name) VALUES (6, "Diseño");
