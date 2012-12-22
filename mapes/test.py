import json
file = open('mapa_prova.json', 'r')
dades_mapa = json.load(file)
file.close()

for layer in dades_mapa["layers"]:
    print "LAYER:"
    print layer["name"]
    print

raw_input()