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
        "nome": "J. R.",
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
        "nome": "Thiago",
        "status": {},
        "dialogo_bloqueando": [
            "Invadir minha tenda? LOUCO!",
            "Talvez o mano do meu lado deixe, mas EU NÃO!"
        ],
        "dialogo_livre": [
            "Perdão se fui grosseiro, pode entrar se quiser!"
        ]
    },
    "H": {
        "nome": "Diego",
        "status": {},
        "dialogo_bloqueando": [
            "Entrar na MINHA TENDA?",
            "NUNCA! Não importa o que o Thiago diz!",
        ],
        "dialogo_livre": [
            "Não me arrependo de nada, mas você pode entrar.",
        ]
    },
    "I": {
        "nome": "Pedro",
        "status": {},
        "dialogo_bloqueando": [
            "eh... não... duh..."
        ],
        "dialogo_livre": [
            "eh... sim... meh..."
        ]
    },
    "J": {
        "nome": "Carla T.",
        "status": {},
        "dialogo_bloqueando": [
            "Ouvi boatos de que Kauã está em perigo.",
            "Vi no jornal Choquei, deve ser verdade...",
            "Minha tenda? Não, não, não!"
        ],
        "dialogo_livre": [
            "Ouvi boatos de que Você vai ajudar Kauã.",
            "Vi no jornal Choquei, deve ser verdade...",
            "Minha tenda? Pode entrar!",
        ]
    },
    "K": {
        "nome": "Manny",
        "status": {},
        "dialogo_bloqueando": [
            "Perdi meu emprego de ator por causa das bactérias...",
            "Só saio daqui por uma boa causa!",
        ],
        "dialogo_livre": [
            "Oh, você é uma boa pessoa!",
            "Pode entrar na minha tenda!",
        ]
    },

    "L": {
        "nome": "Placa",
        "status": {"importante": False},
        "dialogos": [
            "Abandonei meu lar por causa das bactérias.",
            "Elas tomaram conta da minha loja!",
            "Estou indo recuperar. Quem sabe um dia eu volte.",
            "Atenciosamente,",
            "Kauã."
        ]
    },
    "M": {
        "nome": "Kauã",
        "status": {"importante": False},
        "dialogos": [
            "Olá, Nala...",
            "Não consigo mais me mover por causa das bactérias.",
            "Observe meu casco, está cheio delas!",
            "Preciso que você prossiga sem mim.",
            "Avançe na floresta e derrote as bactérias...",
            "Confio em você!",
            "Você está indo muito bem...",
        ]
    },
    "N": {
        "nome": "Rei Mundiça",
        "dialogos": [
            "Pobre Kauã...",
            "Não tinha bons hábitos, não se cuidava.",
            "Usei ele de isca para atrair você!",
            "Você é forte, mas não o suficiente.",
            "Prepare-se para a batalha final!",
            "HAHAHAHAHAHAHAHA!!!!!"
        ]
    }
}