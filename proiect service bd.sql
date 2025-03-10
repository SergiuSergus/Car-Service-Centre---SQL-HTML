CREATE DATABASE proiect_service;
USE proiect_service;

CREATE TABLE Clienti(ID_Client INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Nume VARCHAR(255) NOT NULL, Prenume VARCHAR(255) NOT NULL, Adresa VARCHAR(255) DEFAULT NULL, Numar_de_telefon VARCHAR(255) UNIQUE, 
Email VARCHAR(255) UNIQUE);

CREATE TABLE Masini(ID_Masina INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Marca VARCHAR(255) NOT NULL, Model VARCHAR(255), An_de_fabricatie DATE, Numar_de_inmatriculare VARCHAR(255) UNIQUE, 
ID_Client INT, CONSTRAINT FK1 FOREIGN KEY (ID_Client) REFERENCES Clienti (ID_Client) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE Programari(ID_Programare INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Data_programari DATETIME, Descriere_serviciu VARCHAR(255), 
ID_Masina INT, CONSTRAINT FK2 FOREIGN KEY (ID_Masina) REFERENCES Masini (ID_Masina) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE Mecanici(ID_Mecanici INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Nume VARCHAR(255) NOT NULL, Prenume VARCHAR(255) NOT NULL, Specializare VARCHAR(255) DEFAULT 'Mecanic_general', Numar_de_telefon VARCHAR(255) UNIQUE);

CREATE TABLE Sarcini(ID_Sarcina INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Descrierea_sarcinii VARCHAR(255) NOT NULL, Stare VARCHAR(255) DEFAULT 'In asteptare', ID_Programare INT, ID_Mecanic INT,
CONSTRAINT FK3 FOREIGN KEY (ID_Programare) REFERENCES Programari (ID_Programare) ON UPDATE CASCADE ON DELETE CASCADE, CONSTRAINT FK4 FOREIGN KEY (ID_Mecanic) REFERENCES Mecanici (ID_Mecanici) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE Piese(ID_Piesa INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Nume VARCHAR(255), Pret FLOAT, Cantitate_stoc INT DEFAULT 1);

CREATE TABLE Facturi(ID_Factura INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Suma_totala FLOAT NOT NULL, Data_emiterii DATETIME, Detalii_plata VARCHAR(255), ID_Programare INT, ID_Piesa INT,
CONSTRAINT FK5 FOREIGN KEY (ID_Programare) REFERENCES Programari (ID_Programare) ON UPDATE CASCADE ON DELETE CASCADE, CONSTRAINT FK6 FOREIGN KEY (ID_Piesa) REFERENCES Piese (ID_Piesa) ON UPDATE CASCADE ON DELETE CASCADE);

DESCRIBE Clienti;
DESCRIBE Masini;
DESCRIBE Programari;
DESCRIBE Mecanici;
DESCRIBE Sarcini;
DESCRIBE Piese;
DESCRIBE Facturi;

DROP DATABASE proiect_service;
