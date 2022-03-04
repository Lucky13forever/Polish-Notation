import graphviz




teste = [
    "a * ( b - c / d * e ) / f - g * h",

    "- ( a * b )",
    
    "not A or B and ( not C or D )",
    
    "¬ A ^ ( B \/ C ) \/ D ^ ¬ E",
    
    "a - - - - b",
    
    "( a - ( - ( - ( - b ) ) ) )",
    
    "a * b + - c",
    
    "( - b ) * ( - c + b )",
    
    "not A and ( B or C ) or D and not E",
    
    "b * ( - - - c )",
    
    "¬ A ^ ( B \/ C ) \/ D ^ ¬ E",
    
    "( 1 + 2 ) * 3 + 4",

    "1 + 2 + 3 + 4 + 5",
]
prop = teste[7]

contor = 3

dot = graphviz.Digraph(comment='Polish Notation')



lista_noduri = []

# o sa pastrez pt fiecare simbol, simbolul din stanga, si simbolul din dreapta


operators = ["*", "-", "+", "/", "not", "or", "and", "¬", "\/", "^"]

paranthesis = "()"
precendence = {
    "*" : 2,
    "-" : 1,
    "+" : 1,
    "/" : 2,
    "not" : 3,
    "or" : 1,
    "and" : 2,
    "¬" : 3,
    "\/" : 1,
    "^": 2,
}




class Node():
    def __init__(self, nod: int, symbol: str) -> None:
        self.nod = nod
        self.symbol = symbol
        self.st = 0
        self.dr = 0
        self.father = 0


def parcurgere():
    step = []
    step.append( lista_noduri[1] )
    while(step):
        print("?")
        work_node = step[0]

        # dot.node(str(work_node.nod), f'< <FONT COLOR="RED"> {work_node.nod}) </FONT> {work_node.symbol}>')

        step.pop(0)
        

        st = work_node.st
        if(st != 0):
            dot.edge(str(work_node.nod), str(st.nod))
            step.append(st)


        dr = work_node.dr
        if(dr != 0):
            dot.edge(str(work_node.nod), str(dr.nod))
            step.append(dr)




# pastrez fiecare termen intr-o lista
def generare_lista():
    termen = ''
    last_symbol = 'NULL'
    rez = []
    # for i in range(len(prop)):
    #     if prop[i] == ' ':
    #         continue
    #     if prop[i] not in operators and prop[i] not in paranthesis:
    #         termen += prop[i]
        
    #     if prop[i] in operators:

    #         if termen != '':
    #             rez.append(termen)
    #             termen = ''
    #         rez.append(prop[i])

    #     if prop[i] in paranthesis:
    #         if termen != '':
    #             rez.append(termen)
    #             termen = ''
    #         rez.append(prop[i])
    
    # rez.append(termen)
    rez = prop.split(" ")
    return rez

def afisare_lsita():
    for x in rez:
        print(x, end='\n')


# get the index for the least significant symbol in a proposition
# after i found that index, split the proposition in the left part and right part to the symbol
# repeat the process for both of them until the proposition at any given step is ''
 

lista_noduri.append(Node(0, 'NULL'))



# direction stands for
# from which part of the symbol prop was created
# for example
# a * (b - c)
# prop [a] has direction left
# prop [b, -, c] has direction right
# father is the parent node
def calculare_imp_simbol(prop: list, direction: str, father: str):
    # open a paranthesis + 100

    # print(f"Proposition is {prop}\n\n\n")
    global contor
    display_prop = ' '.join(prop)

    if len(prop) == 1 and prop[0] in paranthesis:
        return   

    dot.node(f'text_{contor}',f'<<FONT COLOR="RED" SIZE="100"> Current proposition is: </FONT>  <BR/> <BR/> {display_prop}>', shape="plaintext")
    contor += 1
    
    
    
    minim = 20000
    adaug = 0
    importance = 0
    index = -1

    show_importance = []
    show_importance.append('<')

    imp_index_contor = 0
    imp_index = -1
    imp_x = -1
    imp_importance = -1


    for i in range(len(prop)):
        x = prop[i]
        
        if x == '':
            continue
        if x in operators:
            imp_index_contor += 1
            
            importance = precendence[ x ] + adaug

            show_importance.append( f'<FONT COLOR="BLACK"> The importance of {x} is {importance} </FONT> <BR/>')
            # NOTE u changed here
            if minim >= importance:
                if x == imp_x and x == '-':
                    continue

                minim = importance
                index = i
                imp_index = imp_index_contor
                imp_x = x
                imp_importance = importance

        
        if x in paranthesis:
            if x == '(':
                adaug += 100
            else:
                adaug -= 100


    if imp_index != -1:
        show_importance[imp_index] = f'<FONT COLOR="BLUE"> The importance of {imp_x} is {imp_importance} </FONT> <BR/>'
        pass
    
    show_importance.append('>')
    
    
    display_show_importance = ''.join(show_importance)
    

    # print(display_show_importance)
    dot.node(f'text_{contor}',f'{display_show_importance}', shape="plaintext")
    contor += 1

    # if i found a symbol
    if index != -1:
        k = len(lista_noduri)
        new_nod = Node(k, prop[index])


        lista_noduri.append(new_nod)
        dot.node(f'{new_nod.nod}', f'< <FONT COLOR="RED"> {new_nod.nod}) </FONT> {new_nod.symbol}  >')



        # steps
        dot.node(f'text_{contor}',f'The least significant operator is {prop[index]} \n \n => We create node {new_nod.nod}) {prop[index]}', shape="plaintext")
        contor += 1

        if father != 0:
            dot.node(f'text_{contor}',f'We connect {lista_noduri[father].nod}) {lista_noduri[father].symbol}  with  {new_nod.nod}) {prop[index]}', shape="plaintext")
            contor += 1

        # split in left and right part
        left = prop[:index]
        right = prop[index + 1:]

        if left != []:
            calculare_imp_simbol(left, "left", new_nod.nod)
        if right != []:
            calculare_imp_simbol(right, "right", new_nod.nod)
    
    else:
        # if no symbol was found, then it means i found a variable, and prop has a length of 1, has only 1 element
        # if the direction is left, i take prop[-1]
        # if the direction is right, i take prop[0]
        # i need the direction because i could put paranthesis by mistake in the graph
        # so the direction prevents this from happening


        if direction == "left":
            aux = prop[-1]
        if direction == "right":
            aux = prop[0]
        k = len(lista_noduri)

        if aux in paranthesis:
            return

        new_nod = Node(k, aux)


        # steps
        # steps
        dot.node(f'text_{contor}',f'The variable is {aux}', shape="plaintext")
        contor += 1

        if father != 0:
            dot.node(f'text_{contor}',f'We connect {lista_noduri[father].nod}) {lista_noduri[father].symbol}  with  {new_nod.nod}) {aux}', shape="plaintext")
            contor += 1


        lista_noduri.append(new_nod)
        dot.node(f'{new_nod.nod}', f'< <FONT COLOR="RED"> {new_nod.nod}) </FONT> {new_nod.symbol}>')

    if direction == "left":
        lista_noduri[father].st = new_nod
    if direction == "right":
        lista_noduri[father].dr = new_nod










rez = generare_lista()

calculare_imp_simbol(rez, "start", 0)
parcurgere()

def give_polish_notation():
    rez = ''
    for nod in lista_noduri:
        if nod.symbol != 'NULL':
            rez += nod.symbol
    return rez

def add_steps():
    global contor
    dot.node(f'text_1',f'<<FONT COLOR="RED" SIZE="100"> Starting proposition is: </FONT>  <BR/> <BR/> {prop}>', shape="plaintext")


    dot.node(f'text_2',f'<<FONT COLOR="RED" SIZE="100"> Rules are as follows: </FONT>  <BR/> <BR/> 1) I calculate the importance of each operator, and at each step I choose the one with the least importance  <BR/> <BR/> 2) Then I split my propositon to the left of the operator, and to the right of the operator  <BR/> <BR/> 3) I repeat step 1, 2 until my current proposition is empty <BR/> <BR/> 4) When connecting nodes, I always connect them first as left child, then as right child <BR/> <BR/> 5) When opening a paranthesis I increase the importance with 100 >', shape="plaintext")
   

    dot.node(f'text_{contor}', f'<<FONT COLOR="RED" SIZE="100"> Polish notation is: <BR/> <BR/> <BR/> </FONT> {give_polish_notation()} <BR/> >', shape='plaintext')    
    contor += 1
    
    dot.node(f'text_{contor}', f'<<FONT COLOR="RED" SIZE="100"> Tree representation is: </FONT>  <BR/> <BR/> >', shape='plaintext')    
    contor += 1
    for i in range(1, contor):
        
        if i == contor - 1:
            dot.edge(f'text_{i}', str(lista_noduri[1].nod), label='', color="white")
            continue   
        dot.edge(f'text_{i}', f'text_{i+1}', label='', color="white")

        



add_steps()




dot.render('doctest-owutput/polish-notation.gv', view=True)