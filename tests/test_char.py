from typing import List


import mlconf.char as chr


def test_tokenizer_peek_and_increment_char():
    def test_with_string(string: str):
        lines = chr.get_lines(string)
        chars: List[str] = []
        char = chr.peek(lines, 0, 0)
        chars.append(char.value)
        while char.value != "\0":
            char = chr.next(lines, char.row, char.col)
            chars.append(char.value)
        assert "".join(chars) == string + "\0"

    string = "name: MLConf\nepochs: 10\nbatch_size: 32\nlearning_rate: 0.001"
    test_with_string(string)
    string2 = "Lorem ipsum dolor sit amet, consectetur adip\niscing elit. Sed do eiusm\nd tempor incididunt u\nt labore et dolore magna aliqua."
    test_with_string(string2)
