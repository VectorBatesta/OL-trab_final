from gurobipy import Model, GRB
import pandas as pd


#ler e limpar dados
db_graxos = 'db/taco-db-graxos.csv'
db_nutrientes = 'db/taco-db-nutrientes.csv'
db_nutrientes2 = 'db/taco-db-nutrientes-2.csv'
# /\ precisei editar linha 185 do arquivo taco-db-graxos.csv para remover a vírgula que estava no final da linha
# /\ precisei editar linha 473 e 475 do arquivo taco-db-nutrientes.csv para remover a vírgula que estava no final da linha


#concatenar os dois dataframes de nutrientes
dados_nutrientes = pd.read_csv(db_nutrientes)
dados_nutrientes2 = pd.read_csv(db_nutrientes2).iloc[:, 1:]  #remove primeira coluna q é repetida
dadosALL = pd.concat([dados_nutrientes, dados_nutrientes2], axis=1)


#limpar nomes dos alimentos removendo vírgulas
dadosALL["Nome"] = dadosALL["Nome"].str.replace(', ', ' ')




#########################
### NOMES DAS COMIDAS ###
#########################
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

##############
### PREÇOS ###
##############
#preços correspondentes da imagem (mesma ordem dos foods)
prices = [
    0.42, 0.39, 0.28, 0.36, 0.04, 0.36, 2.33, 0.35, 0.25, 0.53, 0.29, 0.30, 0.77, 0.77, 0.25,
    0.93, 0.27, 0.09, 0.89, 3.25, 0.89, 2.93, 0.19, 0.23, 1.35, 1.30, 0.57, 0.69, 1.52, 1.89,
    0.29, 2.33, 3.23, 0.66, 0.99, 0.27, 0.52, 3.33, 0.52, 2.69, 2.69, 0.81, 1.69, 0.68, 0.66, 0.65,
    0.92, 0.99, 1.67, 1.29, 1.60, 2.43, 2.21, 1.25, 2.10
]

#criar um dicionário de preços
price_dict = dict(zip(foods, prices))

################################
### RESTRIÇÕES DE NUTRIENTES ###
################################
# limites mínimos e máximos para cada nutriente
nutrient_requirements = {
    "Energia (kcal)": (1700, 2500),
    "Proteína (g)": (70, 84),
    "Carboidrato (g)": (130, float("inf")), #trocado -1111 pra inf se nao o programa ignora o carboidrado
    "Fibra alimentar (g)": (30, float("inf")),
    "Cálcio (mg)": (1200, 2000),
    "Magnésio (mg)": (420, 770),
    "Manganês (mg)": (2.30, 11),
    "Fósforo (mg)": (700, 3000),
    "Ferro (mg)": (8, 45),
    "Sódio (mg)": (1200, 2300),
    "Potássio (mg)": (4700, float("inf")),
    "Cobre (mg)": (0.90, 10),
    "Zinco (mg)": (11, 40),
    "Vitamina A_1 (Retinol) (mcg)": (900, 3000),
    "Tiamina (mg)": (1.20, float("inf")),
    "Riboflavina (mg)": (1.30, float("inf")),
    "Vitamina B_6 (Piridoxina) (mg)": (1.70, 100),
    "Niacina (mg)": (16, 35),
    "Vitamina C (mg)": (90, 2000)
}




#filtrar e validar os alimentos presentes nos dados
filtered_data = dadosALL[dadosALL["Nome"].isin(foods)].copy()



#atribuir preços aos alimentos com base no dicionário
filtered_data["Preço (R$/100g)"] = filtered_data["Nome"].map(price_dict)



#converter todas as colunas de nutrientes para numérico (ignorando erros para colunas não numéricas)
nutrient_columns = [col for col in filtered_data.columns if col not in ["Nome", "Preço (R$/100g)"]]
filtered_data[nutrient_columns] = filtered_data[nutrient_columns].apply(pd.to_numeric, errors="coerce")



#verificar se a conversão foi bem-sucedida
print(filtered_data.dtypes)
input("[pressione enter para continuar]")


#verificar alimentos faltantes na filtragem
missing = set(foods) - set(filtered_data["Nome"])
if missing:
    print(f"aviso: alimentos faltantes {missing} - verifique a formatação dos nomes")
    input("[pressione enter para SAIR]")
    exit()



#exibir resultados: alimentos, preços, energia e proteína
print(filtered_data[["Nome", "Preço (R$/100g)", "Energia (kcal)", "Proteína (g)"]])
input("[pressione enter para continuar]")



#carregar os dados limpos para o dataframe final
df = filtered_data.copy()



#criar o modelo de otimização
model = Model("Nutrient Optimization")



#variáveis de decisão: quantidade (em gramas) de cada alimento a consumir, limitada a 1000 gramas (1 kg) por alimento
food_vars = {food: model.addVar(lb=0, ub=1000, vtype=GRB.CONTINUOUS, name=food) for food in df["Nome"]}



#objetivo: minimizar o custo total
#a divisão por 100 converte o preço de R$/100g para R$/g
model.setObjective(
    sum(food_vars[food] * df.loc[df["Nome"] == food, "Preço (R$/100g)"].values[0] / 100 for food in df["Nome"]),
    GRB.MINIMIZE
)




# para cada nutriente, adicionar restrições de mínimo e máximo
for nutrient, (min_val, max_val) in nutrient_requirements.items():
    if nutrient in df.columns:
        model.addConstr(
            sum(
                food_vars[food] * df.loc[df["Nome"] == food, nutrient].values[0] / 100
                for food in df["Nome"]
                if not pd.isna(df.loc[df["Nome"] == food, nutrient].values[0])
            ) >= min_val,
            name=f"min_{nutrient}"
        )
        
        if max_val != float("inf"):
            model.addConstr(
                sum(
                    food_vars[food] * df.loc[df["Nome"] == food, nutrient].values[0] / 100
                    for food in df["Nome"]
                    if not pd.isna(df.loc[df["Nome"] == food, nutrient].values[0])
                ) <= max_val,
                name=f"max_{nutrient}"
            )


#resolver o modelo de otimização
model.optimize()





# ░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████▓▒░░▒▓███████▓▒░  
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░         ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░         ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
# ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
#exibir resultados da otimização
if model.status == GRB.OPTIMAL:
    print("\n   dieta ótima encontrada:")
    for food in df["Nome"]:
        quantity = food_vars[food].x
        if quantity > 0:
            # Get price from dataframe column
            price = df.loc[df["Nome"] == food, "Preço (R$/100g)"].values[0]
            cost = (price * quantity) / 100
            print(f"{food:<35} {quantity:>7.2f} gramas {'':>5} (R${price:>6.2f}/100g, {'':>2} Total: R${cost:>6.2f})")
    print(f"\ncusto total: R${model.objVal:.2f}")
    input("[pressione enter para continuar]")

    
    #calcular e imprimir a ingestão total de cada nutriente com seus limites
    print("\n{:<34} {:>10} {:>10} {:>10}".format("Nutriente", "Total", "Mínimo", "Máximo")) #<--formatação loca do deepzika
    for nutrient, (min_val, max_val) in nutrient_requirements.items():
        if nutrient in df.columns:
            total_nutrient = sum(
                food_vars[food].x * (df.loc[df["Nome"] == food, nutrient].values[0] if not pd.isna(df.loc[df["Nome"] == food, nutrient].values[0]) else 0) / 100
                for food in df["Nome"]
            )
        print("{:<34} {:>10.2f} {:>10} {:>10}".format( #<--formatação loca do deepzika
            f"{nutrient}:", 
            total_nutrient, 
            min_val, 
            max_val
        ))
    input("[pressione enter para terminar código]")
else:
    print("\n#\n#\n#\nnenhuma solução ótima encontrada.\n#\n#\n#")
    input("[pressione enter para SAIR]")



