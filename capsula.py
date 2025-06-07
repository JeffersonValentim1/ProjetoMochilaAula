from mip import Model, xsum, INTEGER, BINARY, MAXIMIZE

# Lista de aminoácidos
aminoacidos = [
    "Histidina", "Isoleucina", "Leucina", "Lisina",
    "Metionina", "Fenilalanina", "Treonina", "Triptófano", "Valina"
]

# Vj valores
Vj = [9, 6, 10, 8, 9, 10, 3, 2, 6]

# Doses mínimas (mg por unidade)
Wj_mg = [10, 20, 39, 30, 15, 25, 15, 4, 26]

# Capacidade total da cápsula (mg)
C = 1644
n = len(aminoacidos)

# Modelo
modelo = Model(sense=MAXIMIZE)

# Variáveis de decisão
x = [modelo.add_var(var_type=INTEGER, lb=0) for _ in range(n)]
y = [modelo.add_var(var_type=BINARY) for _ in range(n)]


# Restrição da cápsula
modelo += xsum(Wj_mg[i] * x[i] for i in range(n)) <= C

# Função objetivo
modelo.objective = xsum(Vj[i] * x[i] for i in range(n))

# Resolver
modelo.optimize()

# Mostrar resultados
peso_total = 0
print("Itens selecionados:")
for i in range(n):
    if x[i].x >= 1:
        qnt = int(x[i].x)
        total_mg = Wj_mg[i] * qnt
        peso_total += total_mg
        print(f" - {aminoacidos[i]}: {qnt}x ({total_mg} mg)")

print(f"\nPeso total: {peso_total} mg ({peso_total / C:.2%} da cápsula)")
