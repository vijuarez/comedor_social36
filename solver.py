def optimize(data):
    from gurobipy import Model, GRB
    from collections import OrderedDict

    # Create a new model
    m = Model("ComedorSocial")

    m.Params.outputFlag = 0

    # Create variables
    X = [[m.addVar(vtype=GRB.INTEGER, name=f"Alimento_{a}CompradoDia{i}") for a in range(data['alimentos'])] for i in range(data['dias'])]
    Y = [[m.addVar(vtype=GRB.INTEGER, name=f"Alimento_{a}UsadoDia{i}") for a in range(data['alimentos'])] for i in range(data['dias'])]
    I = [[m.addVar(vtype=GRB.INTEGER, name=f"Alimento_{a}AlmacenadoDia{i}") for a in range(data['alimentos'])] for i in range(data['dias'])]
    extra = [m.addVar(vtype=GRB.INTEGER, name=f"DineroExtraDia{i}") for i in range(data['dias'])]
    surplus = [m.addVar(vtype=GRB.INTEGER, name=f"SurplusElDía{i}") for i in range(data['dias'] + 1)]
    # Set objective
    m.setObjective(sum(extra[i] for i in range(data['dias'])), GRB.MINIMIZE)
    # Add constraint
    m.addConstr(surplus[0] == 0, f'Surplus inicial')

    for a in range(data['alimentos']):
        m.addConstr(I[0][a] == 0, f"Inventario inicial del alimento {a}")

    for i in range(data['dias']):
        m.addConstr(sum(data['costo_alimento'][a] * X[i][a] for a in range(data['alimentos'])) + (data['sueldo_fijo'] / 30.5) <= extra[i] + data['donaciones_monetarias'][i] + data['visitas'][i] * data['entrada'] + surplus[i],
                    f"Límite de gastos en el día {i}")
        m.addConstr(surplus[i + 1] <= extra[i] + data['donaciones_monetarias'][i] + data['visitas'][i] * data['entrada'] + surplus[i] - (sum(data['costo_alimento'][a] * X[i][a] for a in range(data['alimentos'])) + (data['sueldo_fijo'] / 30.5)),
                    f"Surplus en el día {i}")
        m.addConstr(sum(I[i][a] * data['volumen_alimentos'][a] for a in range(data['alimentos'])) <= data['vol_max'],
                    f"Límite de almacenamiento día {i}")
        m.addConstr(sum(Y[i][a] * data['proteina'][a] for a in range(data['alimentos'])) >= data['visitas'][i],
                    f"Una proteina mínimo por comida día {i}")
        m.addConstr(sum(Y[i][a] * data['carbohidrato'][a] for a in range(data['alimentos'])) >= data['visitas'][i],
                    f"Un carbohidrato mínimo por comida día {i}")
        m.addConstr(sum(Y[i][a] * data['verdura'][a] for a in range(data['alimentos'])) >= data['visitas'][i],
                    f"Una verdura mínimo por comida día {i}")
        m.addConstr(sum(Y[i][a] * data['fruta'][a] for a in range(data['alimentos'])) >= data['visitas'][i],
                    f"Una fruta mínimo por comida día {i}")
        m.addConstr(extra[i] >= 0, f"Naturaleza de Z en dia {i}")
        m.addConstr(surplus[i] >= 0, f"Naturaleza de s en dia {i}")
        for a in range(data['alimentos']):
            m.addConstr(Y[i][a] <= X[i][a] + I[max(0, i - 1)][a] + data['cantidad_alimento'][a][i],
                    f"No se puede usar más de lo que se tiene ")
            m.addConstr(I[i][a] <= X[i][a] + (I[i - 1][a] if i else 0) + data['cantidad_alimento'][a][i] - Y[i][a],
                    f'No se puede guardar más de lo que no se usa')
            m.addConstr(X[i][a] >= 0, f"Naturaleza de X en dia {i} y alimento {a}")
            m.addConstr(Y[i][a] >= 0, f"Naturaleza de Y en dia {i} y alimento {a}")
            m.addConstr(I[i][a] >= 0, f"Naturaleza de I en dia {i} y alimento {a}")

    m.optimize()

    final = OrderedDict()

    for v in m.getVars():
        final[v.VarName] = v.X

    return final