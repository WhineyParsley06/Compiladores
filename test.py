import unittest
import sys
from io import StringIO
from lexer import Lexer


class TestLexer(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.lexer = Lexer()
    
    def tokenize_text(self, text):
        """Función auxiliar para tokenizar texto y devolver lista de tokens"""
        return list(self.lexer.tokenize(text))
    
    # ===========================================
    # TESTS POSITIVOS (10)
    # ===========================================
    
    def test_positive_01_keywords(self):
        """Test positivo: Palabras reservadas básicas"""
        text = "if else while for function return"
        tokens = self.tokenize_text(text)
        expected_types = ['IF', 'ELSE', 'WHILE', 'FOR', 'FUNCTION', 'RETURN']
        
        self.assertEqual(len(tokens), 6)
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_positive_02_data_types(self):
        """Test positivo: Tipos de datos y valores booleanos"""
        text = "integer float boolean string true false"
        tokens = self.tokenize_text(text)
        expected_types = ['INTEGER', 'FLOAT', 'BOOLEAN', 'STRING', 'TRUE', 'FALSE']
        
        self.assertEqual(len(tokens), 6)
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_positive_03_logical_operators(self):
        """Test positivo: Operadores lógicos"""
        text = "&& || !"
        tokens = self.tokenize_text(text)
        expected_types = ['LAND', 'LOR', 'NOT']
        
        self.assertEqual(len(tokens), 3)
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_positive_04_relational_operators(self):
        """Test positivo: Operadores relacionales"""
        text = "== != < <= > >="
        tokens = self.tokenize_text(text)
        expected_types = ['EQ', 'NE', 'LT', 'LE', 'GT', 'GE']
        
        self.assertEqual(len(tokens), 6)
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_positive_05_punctuation_symbols(self):
        """Test positivo: Signos de puntuación y símbolos"""
        text = "( ) [ ] { } ; , : = + - * / %"
        tokens = self.tokenize_text(text)
        expected_types = ['(', ')', '[', ']', '{', '}', ';', ',', ':', '=', '+', '-', '*', '/', '%']
        
        self.assertEqual(len(tokens), 15)
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_positive_06_integer_literals(self):
        """Test positivo: Literales enteros"""
        text = "0 123 456789"
        tokens = self.tokenize_text(text)
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, 'INT_LITERAL')
        self.assertEqual(tokens[0].value, 0)
        self.assertEqual(tokens[1].type, 'INT_LITERAL')
        self.assertEqual(tokens[1].value, 123)
        self.assertEqual(tokens[2].type, 'INT_LITERAL')
        self.assertEqual(tokens[2].value, 456789)
    
    def test_positive_07_float_literals(self):
        """Test positivo: Literales flotantes"""
        text = "3.14 .5 123.456 1e5 2.5e-10"
        tokens = self.tokenize_text(text)
        
        self.assertEqual(len(tokens), 5)
        for token in tokens:
            self.assertEqual(token.type, 'FLOAT_LITERAL')
        
        self.assertAlmostEqual(tokens[0].value, 3.14)
        self.assertAlmostEqual(tokens[1].value, 0.5)
        self.assertAlmostEqual(tokens[2].value, 123.456)
        self.assertAlmostEqual(tokens[3].value, 1e5)
        self.assertAlmostEqual(tokens[4].value, 2.5e-10)
    
    def test_positive_08_char_literals(self):
        """Test positivo: Literales de carácter"""
        text = "'a' 'Z' '1' '\\n' '\\t'"
        tokens = self.tokenize_text(text)
        
        self.assertEqual(len(tokens), 5)
        for token in tokens:
            self.assertEqual(token.type, 'CHAR_LITERAL')
        
        self.assertEqual(tokens[0].value, 'a')
        self.assertEqual(tokens[1].value, 'Z')
        self.assertEqual(tokens[2].value, '1')
        self.assertEqual(tokens[3].value, '\n')
        self.assertEqual(tokens[4].value, '\t')
    
    def test_positive_09_string_literals(self):
        """Test positivo: Literales de cadena"""
        text = '"hello" "world" "Hello World" "line1\\nline2"'
        tokens = self.tokenize_text(text)
        
        self.assertEqual(len(tokens), 4)
        for token in tokens:
            self.assertEqual(token.type, 'STRING_LITERAL')
        
        self.assertEqual(tokens[0].value, 'hello')
        self.assertEqual(tokens[1].value, 'world')
        self.assertEqual(tokens[2].value, 'Hello World')
        self.assertEqual(tokens[3].value, 'line1\nline2')
    
    def test_positive_10_increment_decrement(self):
        """Test positivo: Operadores incremento y decremento"""
        text = "++ --"
        tokens = self.tokenize_text(text)
        expected_types = ['INC', 'DEC']
        
        self.assertEqual(len(tokens), 2)
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    # ===========================================
    # TESTS NEGATIVOS (10)
    # ===========================================
    
    def test_negative_01_invalid_characters(self):
        """Test negativo: Caracteres inválidos"""
        # Capturar stderr para los mensajes de error
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            tokens = self.tokenize_text("x @ y")
            # Deberíamos obtener solo x e y, @ debería generar error
            token_values = [t.value for t in tokens if hasattr(t, 'value')]
            self.assertIn('x', token_values)
            self.assertIn('y', token_values)
            
            # Verificar que se imprimió mensaje de error
            error_output = captured_output.getvalue()
            self.assertIn("Bad character", error_output)
            self.assertIn("@", error_output)
        finally:
            sys.stdout = old_stdout
    
    def test_negative_02_incomplete_operators(self):
        """Test negativo: Operadores incompletos"""
        text = "= ! < >"  # Operadores de un carácter en lugar de los de dos
        tokens = self.tokenize_text(text)
        
        # Estos deberían ser reconocidos como tokens individuales, no como los operadores compuestos
        expected_types = ['=', 'NOT', 'LT', 'GT']
        
        self.assertEqual(len(tokens), 4)
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_negative_03_unterminated_string(self):
        """Test negativo: Cadena sin terminar"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # String sin comillas de cierre
            tokens = self.tokenize_text('"hello world')
            # Esto debería causar un error o comportamiento inesperado
            
            # El lexer podría no generar token STRING_LITERAL válido
            string_tokens = [t for t in tokens if t.type == 'STRING_LITERAL']
            # Si genera un token, no debería ser la cadena completa esperada
            if string_tokens:
                self.assertNotEqual(string_tokens[0].value, 'hello world')
        finally:
            sys.stdout = old_stdout
    
    def test_negative_04_unterminated_char(self):
        """Test negativo: Carácter literal sin terminar"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # Char literal sin comilla de cierre
            tokens = self.tokenize_text("'a")
            
            # No debería generar un CHAR_LITERAL válido
            char_tokens = [t for t in tokens if t.type == 'CHAR_LITERAL']
            self.assertEqual(len(char_tokens), 0)
        finally:
            sys.stdout = old_stdout
    
    def test_negative_05_invalid_float_format(self):
        """Test negativo: Formato de flotante inválido"""
        text = "3..14 .e5 e10"  # Formatos inválidos de flotantes
        tokens = self.tokenize_text(text)
        
        # Ninguno de estos debería ser reconocido como FLOAT_LITERAL válido
        float_tokens = [t for t in tokens if t.type == 'FLOAT_LITERAL']
        # Algunos podrían ser reconocidos parcialmente, pero no como los valores esperados
        for token in float_tokens:
            self.assertNotEqual(token.value, 3.14)  # No debería parsearse como 3.14
    
    def test_negative_06_invalid_escape_sequences(self):
        """Test negativo: Secuencias de escape inválidas en strings"""
        text = '"\\z" "\\q"'  # Secuencias de escape no válidas
        tokens = self.tokenize_text(text)
        
        # Debería generar tokens STRING_LITERAL, pero con las secuencias sin procesar
        string_tokens = [t for t in tokens if t.type == 'STRING_LITERAL']
        self.assertEqual(len(string_tokens), 2)
        
        # Las secuencias inválidas no deberían convertirse a caracteres especiales
        for token in string_tokens:
            self.assertIn('\\', token.value)  # Debería mantener el backslash
    
    def test_negative_07_keywords_as_parts_of_identifiers(self):
        """Test negativo: Palabras clave como parte de identificadores (válido)"""
        text = "ifx whiley forloop"  # Identificadores que contienen keywords
        tokens = self.tokenize_text(text)
        
        # Estos deberían ser identificadores, NO keywords
        self.assertEqual(len(tokens), 3)
        for token in tokens:
            self.assertEqual(token.type, 'ID')
        
        # Verificar que NO son las keywords
        keyword_types = ['IF', 'WHILE', 'FOR']
        for token in tokens:
            self.assertNotIn(token.type, keyword_types)
    
    def test_negative_08_numbers_starting_with_zero(self):
        """Test negativo: Números que inician con cero (caso límite)"""
        text = "01 00123"  # Números que empiezan con 0
        tokens = self.tokenize_text(text)
        
        # Deberían ser reconocidos como enteros, pero verificar valores
        int_tokens = [t for t in tokens if t.type == 'INT_LITERAL']
        self.assertEqual(len(int_tokens), 2)
        
        # Los valores pueden ser diferentes de lo esperado visualmente
        self.assertEqual(int_tokens[0].value, 1)    # No 01
        self.assertEqual(int_tokens[1].value, 123)  # No 00123
    
    def test_negative_09_mixed_quotes_in_strings(self):
        """Test negativo: Comillas mixtas en strings"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            text = '"hello\' \\"world"'  # Mezcla de comillas simples y dobles
            tokens = self.tokenize_text(text)
            
            string_tokens = [t for t in tokens if t.type == 'STRING_LITERAL']
            # Debería manejar las comillas internas correctamente o generar error
            if string_tokens:
                # La comilla simple dentro no debería cerrar el string
                self.assertNotEqual(len(string_tokens), 2)
        finally:
            sys.stdout = old_stdout
    
    def test_negative_10_operators_without_spaces(self):
        """Test negativo: Operadores sin espacios que podrían confundirse"""
        text = "x<y>z x<=y>=z"  # Operadores adyacentes sin espacios
        tokens = self.tokenize_text(text)
        
        # Verificar que se separen correctamente
        token_types = [t.type for t in tokens]
        
        # Primer grupo: x < y > z
        expected_first = ['ID', 'LT', 'ID', 'GT', 'ID']
        # Segundo grupo: x <= y >= z  
        expected_second = ['ID', 'LE', 'ID', 'GE', 'ID']
        
        expected_all = expected_first + expected_second
        self.assertEqual(len(tokens), len(expected_all))
        
        for i, expected_type in enumerate(expected_all):
            self.assertEqual(tokens[i].type, expected_type)


if __name__ == '__main__':
    unittest.main(verbosity=2)