CREATE CATALOG IF NOT EXISTS eleicoes2026_brazil;


CREATE SCHEMA IF NOT EXISTS eleicoes2026_brazil.`01_bronze`;

CREATE SCHEMA IF NOT EXISTS eleicoes2026_brazil.`02_silver`;

CREATE SCHEMA IF NOT EXISTS eleicoes2026_brazil.`03_gold`;


CREATE VOLUME IF NOT EXISTS
eleicoes2026_brazil.`01_bronze`.arquivos;
