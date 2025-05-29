# este arquivo define o comportamento dos npcs do jogo
# cada npc tem um simbolo unico usado no mapa
# cada npc possui nome, status e dialogos
# dialogos podem ser diferentes dependendo do estado do npc
# comentarios em minusculo e sem acento para facilitar entendimento

npcs_data = {
    "A": {
        "nome": "Carlos",  # nome do npc
        "status": {"importante": True},  # status do npc, se e importante ou nao
        "dialogos": [  # dialogos do npc
            "Caramba, isso tá demorando pra crescer...",
            "Os tomates do Will vão crescer mais rápido que isso!",
        ]
    },
    "B": {
        "nome": "Will",
        "status": {"importante": False},
        "dialogos": [
            "Meu Deus, que demora pra crescer...",
            "Os tomates do Carlos vão crescer mais rápido que isso!",
        ]
    },
    "C": {
        "nome": "Piu",
        "status": {"importante": True},
        "dialogos_bloqueando": [  # dialogos que aparecem quando algo esta bloqueando o npc
            "Aaaaai! Meus Olhos! Sujos de lamaaaa!",
            "Não consigo enxergar a passagem, alguém me ajuda!",
            "Ei, você! Procure um sabonete para mim! Preciso enxergar!"
        ],
        "dialogos_entrega": [  # dialogos de agradecimento ao receber ajuda
            "Oh, como você é gentil! Obrigado por me ajudar!",
            "Perdão por atrapalhar sua jornada, por favor, siga em frente!"
        ],
        "dialogos_livre": [  # dialogos quando o npc esta livre
            "Olhinhos, olhinhos... Enxergo, enxergo... Piu!"
        ]
    },
    "D": {
        "nome": "Rosa",
        "status": {"importante": False},
        "dialogos": [
            "Oh, meu jardim! Finalmente terminei de plantar!",
            "Estava com muita dor no pé por causa da bactéria do pé!",
            "Mas passei Álcool, estou usando Talco e agora estou ótima!",
            "Vá ver o meu jardim, está lindo!",
        ]
    },
    "E": {
        "nome": "Kaiki",
        "status": {"importante": False, "presente_entregue": False},
        "dialogos": [
            "THE GUARDIAAAAAAAAAAAAAAAAAAAAAN!",
            "TOME ESTE PRESENTE E SE CUIDE!",
            "AAAAAAAND OOOOOOOOOONE",
        ]
    },
    "F": {
        "nome": "Bob",
        "status": {"importante": True, "tocha_entregue": False},
        "dialogos_bloqueando": [
            "Acabei de chegar da floresta, tá muito escuro lá dentro!",
            "Estive com Kauã agora há pouco, ele quer sua ajuda...",
            "Procure uma tocha na aldeia e volte aqui, por favor!",
        ],
        "dialogos_entrega": [
            "Ótimo, você trouxe a tocha! Kauã precisa atravessar a floresta.",
            "A loja dele fica do outro lado da aldeia, mas...",
            "O caminho está cheio de bactérias! A loja dele foi invadida!",
            "Confio que você consegue combater os maus-hábitos.",
            "Boa sorte, Nala!",
        ],
        "dialogos_livre": [
            "Tome cuidado com as bactérias, Nala.",
            "Sempre use o ataque certo contra elas!",
        ]
    },
    "G": {
        "nome": "Tigre Branco",
        "status": {},
        "dialogo_bloqueando": [
            "Desculpe, não posso deixar você passar ainda.",
            "Fale com o Bob primeiro!"
        ],
        "dialogo_livre": [
            "Agora você pode entrar na tenda. Boa sorte!"
        ]
    },
    "H": {
        "nome": "NPC H",
        "status": {},
        "dialogo_bloqueando": [
            "Estamos em reunião, volte depois de falar com o Bob."
        ],
        "dialogo_livre": [
            "A passagem está livre, pode entrar!"
        ]
    },
    "I": {
        "nome": "NPC I",
        "status": {},
        "dialogo_bloqueando": [
            "Aguardando instruções do Bob..."
        ],
        "dialogo_livre": [
            "Pode passar, a tenda está aberta!"
        ]
    },
    "J": {
        "nome": "NPC J",
        "status": {},
        "dialogo_bloqueando": [
            "Só liberamos a entrada após o Bob autorizar."
        ],
        "dialogo_livre": [
            "Bem-vindo à tenda!"
        ]
    },
    "K": {
        "nome": "NPC K",
        "status": {},
        "dialogo_bloqueando": [
            "Fale com o Bob para liberar a passagem."
        ],
        "dialogo_livre": [
            "Aproveite sua visita à tenda!"
        ]
    }
}