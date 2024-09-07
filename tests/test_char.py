from typing import List

from mlconf.char import CharStream as chr


def test_tokenizer_peek_and_increment_char():
    def test_with_string(string: str):
        chstream = chr(string)
        chars: List[str] = []
        chars.append(chstream.peek())
        while chstream.peek() != "\0":
            chars.append(chstream.next())
        assert "".join(chars) == string + "\0"

    string = "name: MLConf\nepochs: 10\nbatch_size: 32\nlearning_rate: 0.001"
    test_with_string(string)
    string2 = "Lorem ipsum dolor sit amet, consectetur adip\niscing elit. Sed do eiusm\nd tempor incididunt u\nt labore et dolore magna aliqua."
    test_with_string(string2)
