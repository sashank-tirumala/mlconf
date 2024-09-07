from typing import List

from mlconf.char import CharStream as chr


def test_tokenizer_peek_and_increment_char(simple_config_str: str):
    def test_with_string(string: str):
        chstream = chr(string)
        chars: List[str] = []
        chars.append(chstream.peek())
        while chstream.peek() != "\0":
            chars.append(chstream.next())
        assert "".join(chars) == string + "\0"

    test_with_string(simple_config_str)
