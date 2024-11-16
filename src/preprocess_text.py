from bs4 import BeautifulSoup


class PreprocessText(object):

    def __init__(self, language: str, n_max_words_per_text: int) -> None:
        """Creates object attributes for the PreprocessText class.

        Creates object attributes for the PreprocessText class.

        Args:
            language: A string for the name of the european language the text belongs to.
            n_max_words_per_text: An integer for the maximum no. of the words in a text.

        Returns:
            None.
        """
        # Asserts type & values of the arguments.
        assert isinstance(language, str), "Variable language should be of type 'str'."
        assert language in [
            "es",
            "fr",
            "de",
        ], "Variable language should have value as 'es', 'fr', or 'de'."
        assert isinstance(
            n_max_words_per_text, int
        ), "Variable n_max_words_per_text should be of type 'int'."

        # Initializes class variables.
        self.language = language
        self.n_max_words_per_text = 50
        self.unique_word_count = {"en": dict(), language: dict()}
        self.rare_words = {"en": set(), self.language: set()}

    def remove_html_markup(self, text: str) -> str:
        """Removes HTML markup components from text.

        Removes HTML markup components from text.

        Args:
            text: A string for the text which needs to be processed.

        Returns:
            A string for the processed text without HTML markup components.
        """
        # Asserts type & values of the arguments.
        assert isinstance(text, str), "Variable text should be of type 'str'."

        # Creates an object for BeautifulSoup.
        soup = BeautifulSoup(text, "lxml")

        # Get the text content of all visible elements.
        text = soup.get_text(strip=True)

        # Remove any leading or trailing spaces.
        text = text.strip()

        # Replace consecutive whitespace characters with a single space.
        return " ".join(text.split())
