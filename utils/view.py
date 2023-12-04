from typing import Optional


__all__ = ("StringView",)


class ViewError(Exception):
    ...


class UnexpectedQuoteError(ViewError):
    def __init__(self, quote: str, /) -> None:
        self.quote: str = quote
        super().__init__(f"Unexpected quote mark, {quote!r}, in non-quoted string")


class ExpectedClosingQuoteError(ViewError):
    def __init__(self, close_quote: str, /) -> None:
        self.close_quote: str = close_quote
        super().__init__(f"Expected closing {close_quote}.")


class InvalidEndOfQuotedStringError(ViewError):
    def __init__(self, char: str, /) -> None:
        self.char: str = char
        super().__init__(f"Expected space after closing quotation but received {char!r}")


_quotes = {
    '"': '"',
    "‘": "’",
    "‚": "‛",
    "“": "”",
    "„": "‟",
    "⹂": "⹂",
    "「": "」",
    "『": "』",
    "〝": "〞",
    "﹁": "﹂",
    "﹃": "﹄",
    "＂": "＂",
    "｢": "｣",
    "«": "»",
    "‹": "›",
    "《": "》",
    "〈": "〉",
}


_all_quotes = set(_quotes.keys()) | set(_quotes.values())


# thanks danny
class StringView:
    __slots__ = ("index", "buffer", "end", "previous")

    def __init__(self, buffer: str, /) -> None:
        self.index: int = 0
        self.buffer: str = buffer
        self.end: int = len(buffer)
        self.previous: int = 0

    @property
    def current(self) -> Optional[str]:
        return None if self.eof else self.buffer[self.index]

    @property
    def eof(self) -> bool:
        return self.index >= self.end

    def undo(self) -> None:
        """Undo the last read operation. Cannot undo skip_ws or skip_string. Cannot undo more than once."""
        self.index = self.previous

    def skip_ws(self) -> bool:
        """Skip whitespace. Returns True if any whitespace was skipped."""
        pos = 0
        while not self.eof:
            try:
                current = self.buffer[self.index + pos]
                if not current.isspace():
                    break
                pos += 1
            except IndexError:
                break

        self.previous = self.index
        self.index += pos
        return self.previous != self.index

    def skip_string(self, string: str, /) -> bool:
        """Skip a string. Returns True if the string was skipped."""
        strlen = len(string)
        if self.buffer[self.index : self.index + strlen] == string:
            self.previous = self.index
            self.index += strlen
            return True
        return False

    def read_rest(self) -> str:
        """Read and return the rest of the string."""
        result = self.buffer[self.index :]
        self.previous = self.index
        self.index = self.end
        return result

    def read(self, n: int, /) -> str:
        """Read and return the next n characters."""
        result = self.buffer[self.index : self.index + n]
        self.previous = self.index
        self.index += n
        return result

    def get(self) -> Optional[str]:
        """Get the next character. Returns None if EOF is reached."""
        try:
            result = self.buffer[self.index]
        except IndexError:
            return None

        self.previous = self.index
        self.index += 1
        return result

    def get_word(self) -> str:
        """Get the next word. A word is defined as a sequence of non-whitespace characters."""
        pos = 0
        while not self.eof:
            try:
                current = self.buffer[self.index + pos]
                if current.isspace():
                    break
                pos += 1
            except IndexError:
                break
        self.previous = self.index
        result = self.buffer[self.index : self.index + pos]
        self.index += pos
        return result

    def get_quoted_word(self) -> Optional[str]:
        """Get the next quoted word. A quoted word is defined as a sequence of characters inside a quote. Returns None if EOF is reached."""
        current = self.current
        if current is None:
            return None

        close_quote = _quotes.get(current)
        is_quoted = bool(close_quote)
        if is_quoted:
            result = []
            _escaped_quotes = (current, close_quote)
        else:
            result = [current]
            _escaped_quotes = _all_quotes

        while not self.eof:
            current = self.get()
            if not current:
                if is_quoted:
                    # unexpected EOF
                    raise ExpectedClosingQuoteError(close_quote)
                return "".join(result)

            # currently we accept strings in the format of "hello world"
            # to embed a quote inside the string you must escape it: "a \"world\""
            if current == "\\":
                next_char = self.get()
                if not next_char:
                    # string ends with \ and no character after it
                    if is_quoted:
                        # if we're quoted then we're expecting a closing quote
                        raise ExpectedClosingQuoteError(close_quote)
                    # if we aren't then we just let it through
                    return "".join(result)

                if next_char in _escaped_quotes:
                    # escaped quote
                    result.append(next_char)
                else:
                    # different escape character, ignore it
                    self.undo()
                    result.append(current)
                continue

            if not is_quoted and current in _all_quotes:
                # we aren't quoted
                raise UnexpectedQuoteError(current)

            # closing quote
            if is_quoted and current == close_quote:
                next_char = self.get()
                valid_eof = not next_char or next_char.isspace()
                if not valid_eof:
                    raise InvalidEndOfQuotedStringError(next_char)  # type: ignore # this will always be a string

                # we're quoted so it's okay
                return "".join(result)

            if current.isspace() and not is_quoted:
                # end of word found
                return "".join(result)

            result.append(current)

    def __repr__(self) -> str:
        return f"<StringView pos: {self.index} prev: {self.previous} end: {self.end} eof: {self.eof}>"
