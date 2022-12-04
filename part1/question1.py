class Ruban:
    """ représente le ruban d'une machine de Turing """

    def __init__(self, content=None):
        if content is None:
            content = ["#", "#", "#"]
            self.content = content
        else:
            self.content = self.load(content)
        self.reading = 1

    def load(self, content):
        result = ["#"]
        for elm in content[0]:
            result.append(elm)
        result.append("#")
        return result

    def move_left(self):
        if self.reading == 0:
            self.content.insert(0, "#")
        self.reading -= 1
        return self.content[self.reading]

    def move_right(self):
        if self.reading == len(self.content) -1:
            self.content.append("#")
        self.reading += 1
        return self.content[self.reading]

    def read(self):
        return self.content[self.reading]


class Transition:
    """ représente l'état d'une machine de turring """

    def __init__(self, start = None, end = None, read = None, write = None, move = None):
        """
        :param start: str nom d'un etat
        :param end: str nom d'un etat
        :param read: x caracteres x etant le nombre de rubans
        :param write: x caracteres x etant le nombre de rubans
        :param move: x caracteres x etant le nombre de rubans
        """
        if start is None or end is None or read is None or write is None or move is None:
            raise Exception("Erreur dans l'écriture de la transition, argument oublié")
        elif len(read) != len(write) != len(move):
            # todo: utiliser la taille des rubans
            raise Exception("Les transitions doivent prendre en compte tout les rubans")
        self.start = start
        self.end = end
        # transformation des chaines de caractères en listes
        temp1, temp2, temp3 = [], [], []
        for elm in read:
            temp1.append(elm)
        self.read = temp1
        for elm in write:
            temp2.append(elm)
        self.write = temp2
        for elm in move:
            temp3.append(elm)
        self.move = temp3

    def __str__(self):
        print("start", self.start)
        print("end", self.end)
        print("read", self.read)
        print("write", self.write)
        print("move", self.move)
        return "------------------"


class MT:
    """ représente une machine de Turing """

    def __init__(self, etats, rubans, transitions):
        """
        :param etats: liste de chaines de caracteres correspondant a des etats
        :param rubans: liste d'objets rubans
        :param transitions: liste d'objets transition
        """
        if "I" not in etats or "F" not in etats:
            raise Exception("il manque l'état final ou l'état initial")
        self.etats = etats
        self.rubans = rubans
        self.transitions = transitions
        self.current_state = "I"
        self.nb_etat = len(self.etats)
        self.nb_ruban = len(self.rubans)
        self.nb_transitions = len(self.transitions)

    def __str__(self):
        for i in range(self.nb_ruban):
            print("r" + str(i+1) + " : ", self.rubans[i].content)
            print("        " + ("     " * self.rubans[i].reading) + "^")
        print("états :", self.etats)
        return "état courant : " + self.current_state

    def step(self):
        """ fait effectuer un pas de calcul a une machine de Turing déterministe """
        res = []
        for transi in self.transitions:
            if self.current_state == transi.start:
                pass


def create_mt(path):
    """ a partir d'un fichier txt contenant une machine de turing sous forme écrite,
    initialise une machine de turing et la retourne """
    # read the file
    file = open(path, "r")
    res = []
    for line in file:
        if line == "" or line == "\n":
            continue
        else:
            if "\n" in line:
                res.append(line[0:len(line)-1])
            else:
                res.append(line)
    # gestion de la lecture des etats :
    temp_state = []
    etats = res.pop(0)
    if "state" not in etats:
        raise Exception("mauvaise syntaxe, veuillez lire la documentation -> README")
    for elm in etats.replace(" ", "").replace("state", "").replace(":", "").split(","):
        temp_state.append(elm)
    # gestion de la lecture de l'input :
    temp_input = []
    input = res.pop(0)
    if "input" not in input:
        raise Exception("mauvaise syntaxe, veuillez lire la documentation -> README")
    temp_input.append(input.replace(":", "").replace("input", ""))
    # gestion de la lecture des rubans :
    nb_ruban = res.pop(0)
    if "ruban" not in nb_ruban:
        raise Exception("LIS LA DOC PTN ON T'AS DIT")
    temp_rubans = [Ruban(temp_input)]
    for _ in range(int(nb_ruban.replace("ruban", "").replace(":", ""))-1):
        temp_rubans.append(Ruban())
    # gestion de la lecture des transitions :
    temp_transi = []
    while len(res) != 0:
        t1 = res.pop(0).split(",")
        t2 = res.pop(0).split(",")
        temp_transi.append(Transition(t1[0], t2[0], t1[1], t2[1], t2[2]))
    return MT(temp_state, temp_rubans, temp_transi)




machine1 = create_mt("mt1")
machine1.step()
# print(machine1)
