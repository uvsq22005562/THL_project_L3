
class Mt:
    """ Structure d'encapsulation, représente toutes les machines de
    Turing dans leur globalité. """

    def __init__(self, idt):
        self.id = idt

    def __str__(self):
        pass

    def step(self):
        pass

    def run(self):
        pass

    def change_input(self, tape):
        pass


class MtSimple(Mt):
    """ Structure représentant les machines de Turing ne faisant aucun appel
    à une autre machine. """

    def __init__(self, idt, mt_path):
        super().__init__(idt)
        # lecture du fichier :
        mt_file = open(mt_path, "r")
        lines = []  # toutes les lignes possédant du contenu
        for line in mt_file:
            if line == "" or line == "\n":
                continue
            else:
                if "\n" in line:
                    lines.append(line[0:len(line) - 1])
                else:
                    lines.append(line)
        # création des états :
        self.state = []
        state_line = lines.pop(0)
        for state in state_line.replace(" ", "").replace("state", "").replace(":", "").split(","):
            self.state.append(state)
        self.current_state = "I"
        # lecture de l'input :
        input_line = lines.pop(0).replace(":", "").replace("input", "")
        # création des rubans :
        tape_line = lines.pop(0)
        self.tape = [Tape(input_line)]
        for _ in range(int(tape_line.replace("ruban", "").replace(":", "")) - 1):
            self.tape.append(Tape())
        # création des transitions :
        self.transition = []
        while len(lines) != 0:
            t1 = lines.pop(0).split(",")
            t2 = lines.pop(0).split(",")
            self.transition.append(Transition(t1[0], t2[0], t1[1:(1 + len(self.tape))], t2[1:(1 + len(self.tape))], t2[(1 + len(self.tape)):(1 + 2 * len(self.tape))]))

    def __str__(self):
        for i in range(len(self.tape)):
            print("r" + str(i+1) + " : ", self.tape[i].content)
            print("        " + ("     " * self.tape[i].head) + "^")
        print("états :", self.state)
        return "état courant : " + self.current_state

    def step(self):
        for possible_transition in self.transition:
            if possible_transition.start_eq(self.current_state):
                possible = True
                for i in range(len(self.tape)):
                    if (self.tape[i].read() != possible_transition.get_read(i) and possible_transition.get_read(i) != "_")\
                            or (possible_transition.get_read(i) == "_" and self.tape[i].read == "#"):
                        possible = False
                if possible:
                    # execution de la transition
                    for i in range(len(self.tape)):
                        if possible_transition.get_write(i) == "_":
                            pass
                        else:
                            self.tape[i].write(possible_transition.get_write(i))
                        if possible_transition.get_move(i) == ">":
                            self.tape[i].move_right()
                        elif possible_transition.get_move(i) == "<":
                            self.tape[i].move_left()
                    self.current_state = possible_transition.get_end()
                    return True
        return False

    def dead_transi(self):
        tocheck = []
        for elm in self.transition:
            if elm.get_start() != "I": # car on regarde les prédécesseurs (choix)
                tocheck.append(elm)
        # sélections de tout les couples prédécesseur / successeur dans les transitions de la mt
        couples = []
        for elm in tocheck:
            for transi in self.transition:
                if transi.get_end() == elm.get_start() and transi != elm:
                    couples.append([transi, elm])
        for elm in couples:
            if elm[0].move == ["S"] and elm[0].get_read(0) == elm[0].get_write(0):
                print("transi a del", elm[0])
                # ajout de la nouvelle transition:
                self.transition.append(Transition(elm[0].get_start(), elm[1].get_end(), elm[0].get_read(0), elm[1].get_write(0), elm[1].get_move(0)))
                print("remplacé par :", self.transition[len(self.transition) - 1])
                for x in range(len(self.transition)):
                    if self.transition[x] == elm[0] or self.transition[x] == elm[1]:
                        del self.transition[x]
                        return True


    def run(self):
        ctrl = True
        count = 0
        print("======== ETAT INITIAL ===========")
        print(self)
        print("================================= \n\n\n")
        while ctrl:
            ctrl = self.step()
            count += 1
            print("========", "PAS N°" + str(count), "===============" + ("=" * (1 - count // 10)))
            print(self)
            print("================================= \n\n\n")
        if self.current_state == "F":
            return "mot accepté"
        else:
            return "mot rejeté"

    def change_input(self, tape):
        self.tape[0] = tape


class MtComplex(Mt):
    """ Structure représentant les machines de Turing faisant appel à une ou plusieurs
    autres machines. """

    def __init__(self, idt, mt_path, submt_path):
        super().__init__(idt)
        # gestion de la machine principale
        # lecture du fichier :
        mt_file = open(mt_path, "r")
        lines = []  # toutes les lignes possédant du contenu
        for line in mt_file:
            if line == "" or line == "\n":
                continue
            else:
                if "\n" in line:
                    lines.append(line[0:len(line) - 1])
                else:
                    lines.append(line)
        # création des états :
        self.state = []
        state_line = lines.pop(0)
        for state in state_line.replace(" ", "").replace("state", "").replace(":", "").split(","):
            self.state.append(state)
        self.current_state = "I"
        # lecture de l'input :
        input_line = lines.pop(0).replace(":", "").replace("input", "")
        # création des rubans :
        tape_line = lines.pop(0)
        self.tape = [Tape(input_line)]
        for _ in range(int(tape_line.replace("ruban", "").replace(":", "")) - 1):
            self.tape.append(Tape())
        # nombre de sous machines :
        self.submt_number = lines.pop(0).replace("sous_machines", "").replace(" ", "").replace(":", "")
        # création des transitions :
        self.transition = []
        while len(lines) != 0:
            t1 = lines.pop(0).split(",")
            t2 = lines.pop(0).split(",")
            if "*" in t1[0]: # cas de l'appel a une sous machine
                self.transition.append(Transition(t1[0].replace("*", ""),
                                                  "I" + ("+" * int(t2[1].replace("M", ""))),
                                                  t1[1], "_", t2[2]))
                self.transition.append(Transition("F" + ("+" * int(t2[1].replace("M", ""))),
                                                  t2[0].replace("*", ""),
                                                  "_", "_", t2[2]))
            else:
                self.transition.append(Transition(t1[0], t2[0], t1[1], t2[1], t2[2]))
        # gestion des machines appelés :
        for i in range(len(submt_path)):
            # lecture du fichier :
            mt_file = open(submt_path[i], "r")
            lines = []  # toutes les lignes possédant du contenu
            for line in mt_file:
                if line == "" or line == "\n":
                    continue
                else:
                    if "\n" in line:
                        lines.append(line[0:len(line) - 1])
                    else:
                        lines.append(line)
            # création des états :
            state_line = lines.pop(0)
            for state in state_line.replace(" ", "").replace("state", "").replace(":", "").split(","):
                self.state.append(state + ("+" * (i+1)))
            del lines[0:2]
            # création des transitions :
            while len(lines) != 0:
                t1 = lines.pop(0).split(",")
                t2 = lines.pop(0).split(",")
                self.transition.append(Transition(t1[0] + ("+" * (i+1)), t2[0] + ("+" * (i+1)), t1[1], t2[1], t2[2]))

    def __str__(self):
        for i in range(len(self.tape)):
            print("r" + str(i+1) + " : ", self.tape[i].content)
            print("        " + ("     " * self.tape[i].head) + "^")
        print("états :", self.state)
        return "état courant : " + self.current_state

    def step(self):
        for possible_transition in self.transition:
            if possible_transition.start_eq(self.current_state):
                possible = True
                for i in range(len(self.tape)):
                    if self.tape[i].read() != possible_transition.get_read(i) \
                            and possible_transition.get_read(i) != "_":
                        possible = False
                if possible:
                    # execution de la transition
                    print("transition choisie : ", possible_transition)
                    for i in range(len(self.tape)):
                        if possible_transition.get_write(i) != "_":
                            self.tape[i].write(possible_transition.get_write(i))
                        if possible_transition.get_move(i) == ">":
                            self.tape[i].move_right()
                        elif possible_transition.get_move(i) == "<":
                            self.tape[i].move_left()
                    self.current_state = possible_transition.get_end()
                    return True
        return False

    def run(self):
        ctrl = True
        count = 0
        print("======== ETAT INITIAL ===========")
        print(self)
        print("================================= \n\n\n")
        while ctrl:
            ctrl = self.step()
            count += 1
            print("========", "PAS N°" + str(count), "===============" + ("=" * (1 - count // 10)))
            print(self)
            print("================================= \n\n\n")
        if self.current_state == "F":
            return "mot accepté"
        else:
            return "mot rejeté"

    def change_input(self, tape):
        self.tape[0] = tape


class Tape:
    """ Structure représentant un Ruban d'une machine de Turing. """

    def __init__(self, content=None):
        if content is None:
            content = ["#", "#", "#"]
            self.content = content
        else:
            self.content = self.load(content)
        self.head = 1

    def load(self, content):
        result = ["#"]
        for elm in content:
            result.append(elm)
        result.append("#")
        return result

    def move_left(self):
        if self.head == 0:
            self.content.insert(0, "#")
        else:
            self.head -= 1

    def move_right(self):
        if self.head == len(self.content) - 1:
            self.content.append("#")
        self.head += 1

    def read(self):
        return self.content[self.head]

    def write(self, to_write):
        self.content[self.head] = to_write


class Transition:
    """ Structure représentant une transition d'une machine de Turing """

    def __init__(self, start, end, read, write, move):
        self.start = start
        self.end = end
        self.read, self.write, self.move = [], [], []
        for binary in read:
            self.read.append(binary)
        for binary in write:
            self.write.append(binary)
        for movement in move:
            self.move.append(movement)

    def __str__(self):
        return str([self.start, self.end, self.read]) + str([self.write, self.move])

    def get_read(self, tape_idt):
        return self.read[tape_idt]

    def get_write(self, tape_idt):
        return self.write[tape_idt]

    def get_move(self, tape_idt):
        return self.move[tape_idt]

    def start_eq(self, state):
        return self.start == state

    def get_end(self):
        return self.end

    def get_start(self):
        return self.start


# m2 = MtComplex(2, "part1/mt1", ["part1/mt2", "part1/mt3"])
# print(m2.run())
left = MtSimple(1, "machines/LEFT")
# left.run()
search_1 = MtSimple(2, "machines/SEARCH_1")
# search_1.run()
erase = MtSimple(3, "machines/ERASE")
# erase.run()
copy = MtSimple(4, "machines/COPY")
# copy.run()
multiply = MtSimple(5, "machines/MULTIPLY")
for elm in multiply.transition:
    print(elm.start, elm.end)
    print(elm.read)
    print(elm.write)
    print("===================")

multiply.run()