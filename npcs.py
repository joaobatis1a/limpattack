npcs_data = {
    "A": {
        "nome": "Carlos",
        "status": {"importante": True},
        "dialogos": [
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
        "dialogos_bloqueando": [
            "Aaaaai! Meus Olhos! Sujos de lamaaaa!",
            "Não consigo enxergar a passagem, alguém me ajuda!",
            "Ei, você! Procure um sabonete para mim! Preciso enxergar!"
        ],
        "dialogos_entrega": [
            "Oh, como você é gentil! Obrigado por me ajudar!",
            "Perdão por atrapalhar sua jornada, por favor, siga em frente!"
        ],
        "dialogos_livre": [
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
            "THE GUARDIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN",
            "TOME ESTE PRESENTE E SE CUIDE!",
            "AAAAAAAND OOOOOOOOOONE",
        ]
    },
    "F": {
        "nome": "Guardião",
        "status": {"importante": True, "tocha_entregue": False},
        "dialogos_bloqueando": [
            "Você não pode passar sem uma tocha!",
            "Procure uma tocha nas tendas e traga para mim."
        ],
        "dialogos_entrega": [
            "Ótimo, você trouxe a tocha! Agora pode passar.",
            "Vou liberar a passagem para você."
        ],
        "dialogos_livre": [
            "Boa sorte no labirinto escuro!"
        ]
    }   
}