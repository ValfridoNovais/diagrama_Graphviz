CREATE TABLE Clientes (
  Codigo TEXT,
  Nome TEXT,
  Telefone TEXT,
  Endereço TEXT,
  FOREIGN KEY (Clientes) REFERENCES Veiculo(Clientes)
);

CREATE TABLE Veiculo (
  Código TEXT,
  Placa TEXT,
  Modelo TEXT,
  Marca TEXT,
  Ano TEXT,
  Código Cliente TEXT,
  FOREIGN KEY (Veiculo) REFERENCES Ordem Serviço (OS)(Veiculo)
);

CREATE TABLE Ordem Serviço (OS) (
  Número TEXT,
  Data de Emissão TEXT,
  Data de Conclusão TEXT,
  Valor Total TEXT,
  Status TEXT,
  Código Veículo TEXT,
  Código Equipe TEXT,
  FOREIGN KEY (Ordem Serviço (OS)) REFERENCES Equipe(Ordem Serviço (OS)),
  FOREIGN KEY (Ordem Serviço (OS)) REFERENCES Serviço(Ordem Serviço (OS)),
  FOREIGN KEY (Ordem Serviço (OS)) REFERENCES Peça(Ordem Serviço (OS))
);

CREATE TABLE Equipe (
  Código TEXT,
  Nome da Equipe TEXT,
  FOREIGN KEY (Equipe) REFERENCES Mecânico(Equipe)
);

CREATE TABLE Serviço (
  Código TEXT,
  Descrição TEXT,
  Valor por Referência de Mão de Obra TEXT,
  FOREIGN KEY (Serviço) REFERENCES Tabela Referencia Mão De Obra(Serviço)
);

CREATE TABLE Peça (
  Código TEXT,
  Descrição TEXT,
  Valor Unitário TEXT
);

CREATE TABLE Mecânico (
  Código TEXT,
  Nome TEXT,
  Endereço TEXT,
  Especialidade TEXT
);

CREATE TABLE Tabela Referencia Mão De Obra (
  Código TEXT,
  Descrição TEXT,
  Valor Hora TEXT
);