import ply.lex as lex
import ply.yacc as yacc

# Лексер
tokens = (
    'INCLUDE',
    'IOSTREAM',
    'INT',
    'MAIN',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'STD_COUT',
    'OUTPUT_OPERATOR',
    'STRING',
    'STD_ENDL',
    'SEMICOLON',
    'RETURN',
    'ZERO',
)

# Регулярные выражения для токенов
t_INCLUDE = r'\#include'
t_IOSTREAM = r'<iostream>'
t_INT = r'int'
t_MAIN = r'main'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_STD_COUT = r'std::cout'
t_OUTPUT_OPERATOR = r'<<'
t_STRING = r'\"[^\"]*\"'  # Регулярное выражение для строки в кавычках
t_STD_ENDL = r'std::endl'
t_SEMICOLON = r';'
t_RETURN = r'return'
t_ZERO = r'0'

# Игнорируем пробелы, табуляции и символы новой строки
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Обработка ошибок лексера
def t_error(t):
    print(f"Недопустимый символ: {t.value[0]}")
    t.lexer.skip(1)

# Создаем лексер
lexer = lex.lex()

# Парсер
def p_program(p):
    '''program : include_directive main_function'''
    p[0] = ('program', p[1], p[2])

def p_include_directive(p):
    '''include_directive : INCLUDE IOSTREAM'''
    p[0] = ('include_directive', p[1], p[2])

def p_main_function(p):
    '''main_function : INT MAIN LPAREN RPAREN LBRACE statements RBRACE'''
    p[0] = ('main_function', p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_statements(p):
    '''statements : statement statement
                  | empty'''
    if len(p) == 3:
        p[0] = ('statements', p[1], p[2])
    else:
        p[0] = ('empty',)

def p_statement(p):
    '''statement : output_statement
                 | return_statement'''
    p[0] = ('statement', p[1])

def p_output_statement(p):
    '''output_statement : STD_COUT OUTPUT_OPERATOR STRING OUTPUT_OPERATOR STD_ENDL SEMICOLON'''
    p[0] = ('output_statement', p[1], p[2], p[3], p[4], p[5], p[6])

def p_return_statement(p):
    '''return_statement : RETURN ZERO SEMICOLON'''
    p[0] = ('return_statement', p[1], p[2], p[3])

def p_empty(p):
    '''empty : '''
    p[0] = ('empty',)

# Обработка ошибок парсера
def p_error(p):
    print("Синтаксическая ошибка в программе")

# Создаем парсер
parser = yacc.yacc()

# Пример корректной программы
code = """
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""

lexer.input(code)
for token in lexer:
    print(token)

result = parser.parse(code)
print(result)