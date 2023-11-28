CREATE TABLE activations (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	class_name VARCHAR NOT NULL,
	config VARCHAR NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE flags (
	id INTEGER NOT NULL,
	name VARCHAR(30) NOT NULL,
	status BOOLEAN NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name)
)

CREATE TABLE flags_activations (
	flag_id INTEGER,
	activation_id INTEGER,
	FOREIGN KEY(flag_id) REFERENCES flags (id),
	FOREIGN KEY(activation_id) REFERENCES activations (id)
)