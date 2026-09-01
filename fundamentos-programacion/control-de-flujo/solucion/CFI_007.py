for candidato in range(2,101,1):
    es_primo = True

    for divisor in range(candidato-1,1,-1):
        if candidato % divisor == 0:
            es_primo = False
            break

    if es_primo:
        print(candidato)