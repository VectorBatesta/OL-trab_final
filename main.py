import pandas as pd

# Read and clean data
db_graxos = 'db/taco-db-graxos.csv'
db_nutrientes = 'db/taco-db-nutrientes.csv'
db_nutrientes2 = 'db/taco-db-nutrientes-2.csv'
# /\ precisei editar linha 185 do arquivo taco-db-graxos.csv para remover a vírgula que estava no final da linha
# /\ precisei editar linha 473 e 475 do arquivo taco-db-nutrientes.csv para remover a vírgula que estava no final da linha

#concatenar os dois arquivos de nutrientes
dados_nutrientes = pd.read_csv(db_nutrientes)
dados_nutrientes2 = pd.read_csv(db_nutrientes2).iloc[:, 1:]  #remove primeira coluna q é repetida

# Concatenate the two nutrient dataframes
dadosALL = pd.concat([dados_nutrientes, dados_nutrientes2], axis=1)

# Clean food names by removing commas
dadosALL["Nome"] = dadosALL["Nome"].str.replace(', ', ' ')


foods = [
    "Abacate cru",
    "Abacaxi cru",
    "Abóbora cabotian cozida",
    "Abobrinha italiana refogada",
    "Alface americana crua",
    "Arroz integral cozido",
    "Atum conserva em óleo",
    "Banana prata crua",
    "Batata inglesa cozida",
    "Batata inglesa frita",
    "Berinjela cozida",
    "Biscoito doce maisena",
    "Biscoito doce recheado com chocolate",
    "Biscoito doce recheado com morango",
    "Biscoito doce wafer recheado de chocolate",
    "Bolo pronto chocolate",
    "Brócolis cru",
    "Café infusão 10%",
    "Canjica com leite integral",
    "Carne bovina contra-filé sem gordura grelhado",
    "Carne bovina fígado grelhado",
    "Chocolate meio amargo",
    "Chuchu cozido",
    "Couve-flor cozida",
    "Farinha láctea de cereais",
    "Feijão broto cru",
    "Feijão carioca cozido",
    "Frango coxa sem pele cozida",
    "Frango sobrecoxa sem pele assada",
    "Iogurte natural",
    "Laranja pêra crua",
    "Lasanha massa fresca cozida",
    "Leite de vaca desnatado UHT",
    "Maçã Argentina com casca crua",
    "Macarrão Trigo cru",
    "Mamão Papaia cru",
    "Mandioca cozida",
    "Manteiga sem sal",
    "Melão cru",
    "Merluza filé assado",
    "Merluza filé frito",
    "Milho verde cru",
    "Mingau tradicional",
    "Óleo de girassol",
    "Ovo de galinha inteiro cozido/10minutos",
    "Ovo de galinha inteiro frito",
    "Pão aveia forma",
    "Pão trigo francês",
    "Pêssego enlatado em calda",
    "Porco pernil assado",
    "Presunto sem capa de gordura",
    "Queijo minas mozarela",
    "Sardinha conserva em óleo",
    "Uva Itália crua",
    "Uva suco concentrado envasado"
]

# Corresponding prices from the image (same order as `foods`)
prices = [
    0.42, 0.39, 0.28, 0.36, 0.04, 0.36, 2.33, 0.35, 0.25, 0.53, 0.29, 0.30, 0.77, 0.77, 0.25,
    0.93, 0.27, 0.09, 0.89, 3.25, 0.89, 2.93, 0.19, 0.23, 1.35, 1.30, 0.57, 0.69, 1.52, 1.89,
    0.29, 2.33, 3.23, 0.66, 0.99, 0.27, 0.52, 3.33, 0.52, 2.69, 2.69, 0.81, 1.69, 0.68, 0.66, 0.65,
    0.92, 0.99, 1.67, 1.29, 1.60, 2.43, 2.21, 1.25, 2.10
]

# Create a price dictionary
price_dict = dict(zip(foods, prices))

# Filter and validate
filtered_data = dadosALL[dadosALL["Nome"].isin(foods)].copy()






filtered_data["Preço (R$/100g)"] = filtered_data["Nome"].map(price_dict)



# Check for missing matches
missing = set(foods) - set(filtered_data["Nome"])
if missing:
    print(f"Warning: Missing foods {missing} - check name formatting")


# Display results
print(filtered_data[["Nome", "Preço (R$/100g)"]])

