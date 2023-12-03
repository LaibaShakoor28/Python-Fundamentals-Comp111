import re
import sys


class Preprocessor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = "out1.py"

    def eliminate_blank_lines(self, lines):
        non_blank_lines = []
        for line in lines:
            if line.strip():
                non_blank_lines.append(line)
        return non_blank_lines

    def remove_comments(self, lines):
        in_multiline_comment = False
        output_lines = []

        for line in lines:
            if not in_multiline_comment:
                if '"""' in line or "'''" in line:
                    in_multiline_comment = not in_multiline_comment
                    if not line.strip().endswith('"""') and not line.strip().endswith("'''"):
                        in_multiline_comment = True
                elif '#' in line:
                    line = line.split('#')[0].rstrip()
                    if line:
                        output_lines.append(line)
                elif line.strip():  # Check if line is not empty
                    output_lines.append(line)
            else:
                if '"""' in line or "'''" in line:
                    in_multiline_comment = not in_multiline_comment
                    if not line.strip().endswith('"""') and not line.strip().endswith("'''"):
                        in_multiline_comment = True
        # output_lines = [line for line in output_lines if line.strip()]
        return output_lines

    def remove_imports_annotations(self, lines):
        filtered_lines = []
        for line in lines:
            if not (line.startswith("import") or line.startswith("@")):
                filtered_lines.append(line)
        return filtered_lines

    def write_to_output(self, lines):
        with open(self.output_file, 'w') as file:
            for line in lines:
                file.write(line.rstrip() + '\n')

    def display_output(self):
        with open(self.output_file, 'r') as file:
            content = file.read()
            print("Pre Processed File: \n"+ content)

    def preprocess_file(self):
        try:
            with open(self.input_file, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("File not found")
            return
        lines = self.eliminate_blank_lines(lines)
        lines = self.remove_comments(lines)

        # lines = self.remove_spaces_tabs(lines)
        lines = self.remove_imports_annotations(lines)

        self.write_to_output(lines)
        self.display_output()

# -------------------------------------------------------------------------------#
# Task 2 starts from here

class Process:
    def process_output_file(self, input_file, output_file):
        # Task 2 starts from here
        lines_list = []
        keywords = {
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield'
        }
        buffer = ""

        # Read contents of out1.py and process
        with open(input_file, 'r') as file:
            while True:
                char = file.read(1)
                if not char:
                    break
                if char == '\n':
                    lines_list.append(buffer.strip())
                    buffer = ""
                buffer += char

        for x in range(len(lines_list)):
            string = lines_list[x]
            words = string.split()
            if not any(word in keywords for word in words):
                string = string.replace(" ", "")

            if "def" not in words:
                if x != (len(lines_list) - 1):
                    string += ";"
                else:
                    string += "$"

            lines_list[x] = string

        final_buffer = ''.join(lines_list)

        self.write_to_output(final_buffer, output_file)
        self.display_output(output_file)

    def write_to_output(self, final_buffer, output_file):
        with open(output_file, 'w') as file:
            file.write(''.join(final_buffer))

    def display_output(self, output_file):
        with open(output_file, 'r') as file:
            content = file.read()
            print("Processed File: \n" + content + "\n")


# -------------------------------------------------------------------------------#
# Task 3 starts from here


class LexicalAnalyzer:
    def generate_lexemes(self, input_file):
        # Read contents of out1.py and process
        final_buffer = ""
        with open(input_file, 'r') as file:
            while True:
                char = file.read(1)
                if not char:
                    break
                if char == '\n':
                    final_buffer = ""
                final_buffer += char
        #regular expressions
        keyword_pattern = r'\b(?:and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b'
        identifier_pattern = r'\b[a-zA-Z_]\w*\b'
        operator_pattern = r'\+|-|\*|\/|%|=|==|!=|<|>|<=|>=|and|or|not|in|is'
        punctuator_pattern = r'{|}|\[|\]|\(|\)|,|;|:|\.'
        literal_pattern = r'\b(?:\d+\.?\d*|".*?"|\'.*?\')\b'

        # Combine patterns into one
        combined_pattern = f'({keyword_pattern}|{identifier_pattern}|{operator_pattern}|{punctuator_pattern}|{literal_pattern})'

        # Extract lexemes using regular expression
        lexemes = re.findall(combined_pattern, final_buffer)

        # Flatten the list and filter out empty strings or whitespace
        #lexemes = [token for token in lexemes if token.strip()]
        filtered_lexemes = []
        for token in lexemes:
            if token.strip():
                filtered_lexemes.append(token)
        self.display_lexemes(lexemes)

    def display_lexemes(self, lexemes):
        for lexeme in lexemes:
            print("Lexeme: " + lexeme)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py in1.py")
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        preprocessor = Preprocessor(input_file)
        preprocessor.preprocess_file()
        ## now process the output file
        processor = Process()
        processor.process_output_file('out1.py', 'out2.py')
        # part 3
        lexical_Analyzer = LexicalAnalyzer()
        lexical_Analyzer.generate_lexemes('out2.py')
