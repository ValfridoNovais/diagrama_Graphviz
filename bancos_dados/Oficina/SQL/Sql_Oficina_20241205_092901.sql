CREATE TABLE Clientes (
  Codigo TEXT,
  Nome TEXT,
  Telefone TEXT,
  Endereço TEXT,
  FOREIGN KEY (Clientes_id) REFERENCES Veiculo(Clientes_id)
);

CREATE TABLE Veiculo (
  Código TEXT,
  Placa TEXT,
  Modelo TEXT,
  Marca TEXT,
  Ano TEXT,
  Código Cliente TEXT,
  FOREIGN KEY (Veiculo_id) REFERENCES Ordem Serviço (OS)(Veiculo_id)
);

CREATE TABLE Ordem Serviço (OS) (
  Número TEXT,
  Data de Emissão TEXT,
  Data de Conclusão TEXT,
  Valor Total TEXT,
  Status TEXT,
  Código Veículo TEXT,
  Código Equipe TEXT,
  FOREIGN KEY (Ordem Serviço (OS)_id) REFERENCES Serviço(Ordem Serviço (OS)_id),
  FOREIGN KEY (Ordem Serviço (OS)_id) REFERENCES Peça(Ordem Serviço (OS)_id),
  FOREIGN KEY (Ordem Serviço (OS)_id) REFERENCES Equipe(Ordem Serviço (OS)_id)
);

CREATE TABLE Equipe (
  Código TEXT,
  Nome da Equipe TEXT,
  FOREIGN KEY (Equipe_id) REFERENCES Mecânico(Equipe_id)
);

CREATE TABLE Serviço (
  Código TEXT,
  Descrição TEXT,
  Valor por Referência de Mão de Obra TEXT,
  FOREIGN KEY (Serviço_id) REFERENCES Tabela Referencia Mão De Obra(Serviço_id)
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