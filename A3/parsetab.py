
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightEQUALSleftORleftANDleftEQNOTleftLTGTLEGEleftPLUSMINUSleftTIMESDIVIDErightUMINUSrightAMPERSANDSTARleftIFXleftELSEID NUMBER COMMENT LPAREN RPAREN LBRACE RBRACE SEMICOLON AMPERSAND COMMA PLUS MINUS TIMES DIVIDE EQUALS INT VOID MAIN IF ELSE WHILE LT GT LE GE EQ NOT AND OR\n\tstart : function\n\t\n\tfunction : VOID MAIN LPAREN RPAREN LBRACE statements RBRACE\n\ttype : INT\n\t\t| VOID\t\t\n\t\n\tvar : ID\n\t\n\tconst : NUMBER\n\t\n\tpointer : TIMES pointer %prec STAR\n\t\t\t| TIMES address %prec STAR\n\t\t\t| TIMES var %prec STAR\n\t\n\taddress : AMPERSAND pointer\n\t\t\t| AMPERSAND address\n\t\t\t| AMPERSAND var\n\t\n\tstatements :  statement statements\n\t\t\t\t| COMMENT statements\n\t\t\t\t| declaration statements\n\t\t\t\t|\n\tstatement : assignment\n\t\t\t| ifstatement\n\t\t\t| whilestatement\n\t\n\tdeclaration : type idlist SEMICOLON\n\t\n\tidlist : pointer COMMA idlist \n\t\t\t| ID COMMA idlist\n\t\t\t| ID\n\t\t\t| pointer\n\t\n\tassignment : pointer EQUALS expression SEMICOLON\n\t\t\t\t| var EQUALS expression SEMICOLON\n\t\n\tcondition :\texpression LT expression\n\t\t\t\t| expression GT expression\n\t\t\t\t| expression LE expression\n\t\t\t\t| expression GE expression\n\t\t\t\t| expression EQ expression\n\t\t\t\t| condition AND condition\n\t\t\t\t| condition OR condition\n\t\t\t\t| NOT condition\n\t\t\t\t| LPAREN condition RPAREN\n\t\n\tcontrolbody : LBRACE statements RBRACE\n\t\t\t| statement\n\t\t\t| SEMICOLON\n\t\n\tifstatement : IF LPAREN condition RPAREN controlbody %prec IFX\n\t\t\t\t| IF LPAREN condition RPAREN controlbody ELSE controlbody\n\t\n\twhilestatement : WHILE LPAREN condition RPAREN controlbody\n\t\n\texpression : expression PLUS expression\n\t\t\t\t| expression MINUS expression\n\t\t\t\t| expression TIMES expression\n\t\t\t\t| expression DIVIDE expression\n\t\t\t\t| pointer\n\t\t\t\t| address\n\t\t\t\t| const\n\t\t\t\t| var\n\t\t\t\t| LPAREN expression RPAREN\n\t\n\texpression : MINUS expression %prec UMINUS\n\t'
    
_lr_action_items = {'VOID':([0,7,12,13,14,17,18,23,52,76,77,84,85,86,87,98,101,102,],[2,9,9,-19,9,-17,9,-18,-20,-25,-26,-38,-41,-37,9,-39,-36,-40,]),'NUMBER':([25,26,29,38,41,43,47,49,62,64,66,67,68,69,70,71,72,73,74,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'WHILE':([7,12,13,14,17,18,23,52,63,76,77,80,84,85,86,87,98,100,101,102,],[10,10,-19,10,-17,10,-18,-20,10,-25,-26,10,-38,-41,-37,10,-39,10,-36,-40,]),'MINUS':([20,25,26,29,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,55,56,57,59,61,62,64,66,67,68,69,70,71,72,73,74,75,82,89,90,91,92,93,94,95,96,97,],[-5,41,41,41,-8,-9,-7,41,-6,-46,41,-49,41,-47,-48,41,74,41,74,74,-11,-12,-10,-51,74,41,41,41,41,41,41,41,41,41,41,41,74,-50,74,-45,74,74,-44,74,74,-42,-43,]),'RBRACE':([7,8,12,13,14,17,18,23,27,28,33,52,76,77,84,85,86,87,98,99,101,102,],[-16,24,-16,-19,-16,-17,-16,-18,-14,-13,-15,-20,-25,-26,-38,-41,-37,-16,-39,101,-36,-40,]),'COMMENT':([7,12,13,14,17,18,23,52,76,77,84,85,86,87,98,101,102,],[12,12,-19,12,-17,12,-18,-20,-25,-26,-38,-41,-37,12,-39,-36,-40,]),'LE':([20,35,36,37,39,40,42,44,45,48,55,56,57,59,61,82,90,93,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,72,-11,-12,-10,-51,72,-50,-45,-44,-42,-43,]),'RPAREN':([5,20,35,36,37,39,40,42,44,45,46,55,56,57,58,59,60,61,65,75,81,82,83,88,89,90,91,92,93,94,95,96,97,],[6,-5,-8,-9,-7,-6,-46,-49,-47,-48,63,-11,-12,-10,80,-51,81,82,-34,82,-35,-50,-32,-33,-28,-45,-31,-27,-44,-30,-29,-42,-43,]),'SEMICOLON':([20,30,31,32,35,36,37,39,40,42,44,45,50,51,55,56,57,59,63,78,79,80,82,90,93,96,97,100,],[-5,52,-24,-23,-8,-9,-7,-6,-46,-49,-47,-48,76,77,-11,-12,-10,-51,84,-21,-22,84,-50,-45,-44,-42,-43,84,]),'LT':([20,35,36,37,39,40,42,44,45,48,55,56,57,59,61,82,90,93,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,69,-11,-12,-10,-51,69,-50,-45,-44,-42,-43,]),'PLUS':([20,35,36,37,39,40,42,44,45,48,50,51,55,56,57,59,61,75,82,89,90,91,92,93,94,95,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,73,73,73,-11,-12,-10,-51,73,73,-50,73,-45,73,73,-44,73,73,-42,-43,]),'COMMA':([20,31,32,35,36,37,55,56,57,],[-5,53,54,-8,-9,-7,-11,-12,-10,]),'$end':([1,3,24,],[-1,0,-2,]),'GT':([20,35,36,37,39,40,42,44,45,48,55,56,57,59,61,82,90,93,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,66,-11,-12,-10,-51,66,-50,-45,-44,-42,-43,]),'DIVIDE':([20,35,36,37,39,40,42,44,45,48,50,51,55,56,57,59,61,75,82,89,90,91,92,93,94,95,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,67,67,67,-11,-12,-10,-51,67,67,-50,67,-45,67,67,-44,67,67,67,67,]),'EQUALS':([11,15,20,35,36,37,55,56,57,],[26,29,-5,-8,-9,-7,-11,-12,-10,]),'ELSE':([13,17,23,76,77,84,85,86,98,101,102,],[-19,-17,-18,-25,-26,-38,-41,-37,100,-36,-40,]),'GE':([20,35,36,37,39,40,42,44,45,48,55,56,57,59,61,82,90,93,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,71,-11,-12,-10,-51,71,-50,-45,-44,-42,-43,]),'AMPERSAND':([19,25,26,29,34,38,41,43,47,49,62,64,66,67,68,69,70,71,72,73,74,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'LPAREN':([4,10,21,25,26,29,38,41,43,47,49,62,64,66,67,68,69,70,71,72,73,74,],[5,25,38,43,49,49,43,49,43,43,49,43,43,49,49,49,49,49,49,49,49,49,]),'TIMES':([7,9,12,13,14,16,17,18,19,20,22,23,25,26,29,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,59,61,62,63,64,66,67,68,69,70,71,72,73,74,75,76,77,80,82,84,85,86,87,89,90,91,92,93,94,95,96,97,98,100,101,102,],[19,-4,19,-19,19,19,-17,19,19,-5,-3,-18,19,19,19,19,-8,-9,-7,19,-6,-46,19,-49,19,-47,-48,19,70,19,70,70,-20,19,19,-11,-12,-10,-51,70,19,19,19,19,19,19,19,19,19,19,19,19,70,-25,-26,19,-50,-38,-41,-37,19,70,-45,70,70,-44,70,70,70,70,-39,19,-36,-40,]),'EQ':([20,35,36,37,39,40,42,44,45,48,55,56,57,59,61,82,90,93,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,68,-11,-12,-10,-51,68,-50,-45,-44,-42,-43,]),'ID':([7,9,12,13,14,16,17,18,19,22,23,25,26,29,34,38,41,43,47,49,52,53,54,62,63,64,66,67,68,69,70,71,72,73,74,76,77,80,84,85,86,87,98,100,101,102,],[20,-4,20,-19,20,32,-17,20,20,-3,-18,20,20,20,20,20,20,20,20,20,-20,32,32,20,20,20,20,20,20,20,20,20,20,20,20,-25,-26,20,-38,-41,-37,20,-39,20,-36,-40,]),'IF':([7,12,13,14,17,18,23,52,63,76,77,80,84,85,86,87,98,100,101,102,],[21,21,-19,21,-17,21,-18,-20,21,-25,-26,21,-38,-41,-37,21,-39,21,-36,-40,]),'AND':([20,35,36,37,39,40,42,44,45,46,55,56,57,58,59,60,65,81,82,83,88,89,90,91,92,93,94,95,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,62,-11,-12,-10,62,-51,62,-34,-35,-50,-32,62,-28,-45,-31,-27,-44,-30,-29,-42,-43,]),'LBRACE':([6,63,80,100,],[7,87,87,87,]),'INT':([7,12,13,14,17,18,23,52,76,77,84,85,86,87,98,101,102,],[22,22,-19,22,-17,22,-18,-20,-25,-26,-38,-41,-37,22,-39,-36,-40,]),'NOT':([25,38,43,47,62,64,],[47,47,47,47,47,47,]),'MAIN':([2,],[4,]),'OR':([20,35,36,37,39,40,42,44,45,46,55,56,57,58,59,60,65,81,82,83,88,89,90,91,92,93,94,95,96,97,],[-5,-8,-9,-7,-6,-46,-49,-47,-48,64,-11,-12,-10,64,-51,64,-34,-35,-50,-32,-33,-28,-45,-31,-27,-44,-30,-29,-42,-43,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'function':([0,],[1,]),'condition':([25,38,43,47,62,64,],[46,58,60,65,83,88,]),'statements':([7,12,14,18,87,],[8,27,28,33,99,]),'idlist':([16,53,54,],[30,78,79,]),'controlbody':([63,80,100,],[85,98,102,]),'assignment':([7,12,14,18,63,80,87,100,],[17,17,17,17,17,17,17,17,]),'address':([19,25,26,29,34,38,41,43,47,49,62,64,66,67,68,69,70,71,72,73,74,],[35,44,44,44,55,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'whilestatement':([7,12,14,18,63,80,87,100,],[13,13,13,13,13,13,13,13,]),'start':([0,],[3,]),'expression':([25,26,29,38,41,43,47,49,62,64,66,67,68,69,70,71,72,73,74,],[48,50,51,48,59,61,48,75,48,48,89,90,91,92,93,94,95,96,97,]),'statement':([7,12,14,18,63,80,87,100,],[14,14,14,14,86,86,14,86,]),'declaration':([7,12,14,18,87,],[18,18,18,18,18,]),'var':([7,12,14,18,19,25,26,29,34,38,41,43,47,49,62,63,64,66,67,68,69,70,71,72,73,74,80,87,100,],[15,15,15,15,36,42,42,42,56,42,42,42,42,42,42,15,42,42,42,42,42,42,42,42,42,42,15,15,15,]),'const':([25,26,29,38,41,43,47,49,62,64,66,67,68,69,70,71,72,73,74,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'type':([7,12,14,18,87,],[16,16,16,16,16,]),'pointer':([7,12,14,16,18,19,25,26,29,34,38,41,43,47,49,53,54,62,63,64,66,67,68,69,70,71,72,73,74,80,87,100,],[11,11,11,31,11,37,40,40,40,57,40,40,40,40,40,31,31,40,11,40,40,40,40,40,40,40,40,40,40,11,11,11,]),'ifstatement':([7,12,14,18,63,80,87,100,],[23,23,23,23,23,23,23,23,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> function','start',1,'p_start','assign3.py',102),
  ('function -> VOID MAIN LPAREN RPAREN LBRACE statements RBRACE','function',7,'p_function','assign3.py',109),
  ('type -> INT','type',1,'p_function','assign3.py',110),
  ('type -> VOID','type',1,'p_function','assign3.py',111),
  ('var -> ID','var',1,'p_var','assign3.py',118),
  ('const -> NUMBER','const',1,'p_const','assign3.py',124),
  ('pointer -> TIMES pointer','pointer',2,'p_pointer','assign3.py',131),
  ('pointer -> TIMES address','pointer',2,'p_pointer','assign3.py',132),
  ('pointer -> TIMES var','pointer',2,'p_pointer','assign3.py',133),
  ('address -> AMPERSAND pointer','address',2,'p_address','assign3.py',139),
  ('address -> AMPERSAND address','address',2,'p_address','assign3.py',140),
  ('address -> AMPERSAND var','address',2,'p_address','assign3.py',141),
  ('statements -> statement statements','statements',2,'p_statements','assign3.py',147),
  ('statements -> COMMENT statements','statements',2,'p_statements','assign3.py',148),
  ('statements -> declaration statements','statements',2,'p_statements','assign3.py',149),
  ('statements -> <empty>','statements',0,'p_statements','assign3.py',150),
  ('statement -> assignment','statement',1,'p_statements','assign3.py',151),
  ('statement -> ifstatement','statement',1,'p_statements','assign3.py',152),
  ('statement -> whilestatement','statement',1,'p_statements','assign3.py',153),
  ('declaration -> type idlist SEMICOLON','declaration',3,'p_declaration','assign3.py',170),
  ('idlist -> pointer COMMA idlist','idlist',3,'p_idlist','assign3.py',176),
  ('idlist -> ID COMMA idlist','idlist',3,'p_idlist','assign3.py',177),
  ('idlist -> ID','idlist',1,'p_idlist','assign3.py',178),
  ('idlist -> pointer','idlist',1,'p_idlist','assign3.py',179),
  ('assignment -> pointer EQUALS expression SEMICOLON','assignment',4,'p_assignment','assign3.py',185),
  ('assignment -> var EQUALS expression SEMICOLON','assignment',4,'p_assignment','assign3.py',186),
  ('condition -> expression LT expression','condition',3,'p_condition','assign3.py',192),
  ('condition -> expression GT expression','condition',3,'p_condition','assign3.py',193),
  ('condition -> expression LE expression','condition',3,'p_condition','assign3.py',194),
  ('condition -> expression GE expression','condition',3,'p_condition','assign3.py',195),
  ('condition -> expression EQ expression','condition',3,'p_condition','assign3.py',196),
  ('condition -> condition AND condition','condition',3,'p_condition','assign3.py',197),
  ('condition -> condition OR condition','condition',3,'p_condition','assign3.py',198),
  ('condition -> NOT condition','condition',2,'p_condition','assign3.py',199),
  ('condition -> LPAREN condition RPAREN','condition',3,'p_condition','assign3.py',200),
  ('controlbody -> LBRACE statements RBRACE','controlbody',3,'p_controlbody','assign3.py',223),
  ('controlbody -> statement','controlbody',1,'p_controlbody','assign3.py',224),
  ('controlbody -> SEMICOLON','controlbody',1,'p_controlbody','assign3.py',225),
  ('ifstatement -> IF LPAREN condition RPAREN controlbody','ifstatement',5,'p_ifstatement','assign3.py',236),
  ('ifstatement -> IF LPAREN condition RPAREN controlbody ELSE controlbody','ifstatement',7,'p_ifstatement','assign3.py',237),
  ('whilestatement -> WHILE LPAREN condition RPAREN controlbody','whilestatement',5,'p_whilestatement','assign3.py',246),
  ('expression -> expression PLUS expression','expression',3,'p_expression','assign3.py',253),
  ('expression -> expression MINUS expression','expression',3,'p_expression','assign3.py',254),
  ('expression -> expression TIMES expression','expression',3,'p_expression','assign3.py',255),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','assign3.py',256),
  ('expression -> pointer','expression',1,'p_expression','assign3.py',257),
  ('expression -> address','expression',1,'p_expression','assign3.py',258),
  ('expression -> const','expression',1,'p_expression','assign3.py',259),
  ('expression -> var','expression',1,'p_expression','assign3.py',260),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression','assign3.py',261),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','assign3.py',278),
]
