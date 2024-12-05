CREATE TABLE Clientes (
  Codigo TEXT,
  Nome TEXT,
  Telefone TEXT,
  Endere�o TEXT,
  FOREIGN KEY (Clientes_id) REFERENCES Veiculo(Clientes_id)
);

CREATE TABLE Veiculo (
  C�digo TEXT,
  Placa TEXT,
  Modelo TEXT,
  Marca TEXT,
  Ano TEXT,
  C�digo Cliente TEXT,
  FOREIGN KEY (Veiculo_id) REFERENCES Ordem Servi�o (OS)(Veiculo_id)
);

CREATE TABLE Ordem Servi�o (OS) (
  N�mero TEXT,
  Data de Emiss�o TEXT,
  Data de Conclus�o TEXT,
  Valor Total TEXT,
  Status TEXT,
  C�digo Ve�culo TEXT,
  C�digo Equipe TEXT,
  FOREIGN KEY (Ordem Servi�o (OS)_id) REFERENCES Servi�o(Ordem Servi�o (OS)_id),
  FOREIGN KEY (Ordem Servi�o (OS)_id) REFERENCES Pe�a(Ordem Servi�o (OS)_id),
  FOREIGN KEY (Ordem Servi�o (OS)_id) REFERENCES Equipe(Ordem Servi�o (OS)_id)
);

CREATE TABLE Equipe (
  C�digo TEXT,
  Nome da Equipe TEXT,
  FOREIGN KEY (Equipe_id) REFERENCES Mec�nico(Equipe_id)
);

CREATE TABLE Servi�o (
  C�digo TEXT,
  Descri��o TEXT,
  Valor por Refer�ncia de M�o de Obra TEXT,
  FOREIGN KEY (Servi�o_id) REFERENCES Tabela Referencia M�o De Obra(Servi�o_id)
);

CREATE TABLE Pe�a (
  C�digo TEXT,
  Descri��o TEXT,
  Valor Unit�rio TEXT
);

CREATE TABLE Mec�nico (
  C�digo TEXT,
  Nome TEXT,
  Endere�o TEXT,
  Especialidade TEXT
);

CREATE TABLE Tabela Referencia M�o De Obra (
  C�digo TEXT,
  Descri��o TEXT,
  Valor Hora TEXT
);