import unicodedata
import re
import time

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

    def preprocess_text(self, text: str, language: str, update_word_count: bool) -> str:
        """Preprocesses text to remove unwanted characters from it.

        Preprocesses text to remove unwanted characters from it.

        Args:
            text: A string for the text which needs to be processed.
            language: A string for the name of the language the dataset belongs to.
            update_unique_words: A boolean value for updating the word count.

        Returns:
            A string for processed version of input text.
        """
        # Asserts type & values of the arguments.
        assert isinstance(text, str), "Variable text should be of type 'str'."

        # Removes HTML markup components from text provided as input.
        text = self.remove_html_markup(text)

        # Converts text to lowercase characters, & strip leading & trailing whitespace.
        text = text.lower().strip()

        # Replaces unwanted characters in text.
        text = text.replace("##at##-##at##", "-")
        text = text.replace("&apos;", "'")
        text = text.replace("&quot;", '"')
        text = text.replace("&#91;", "")
        text = text.replace("&#93;", "")
        text = text.replace("&#124;", "")
        text = text.replace('"', ' " ')

        # Based on name of the language, removes characters from text.
        if language == "en":
            text = "".join(
                index
                for index in unicodedata.normalize("NFKD", str(text))
                if unicodedata.category(index) != "Mn"
            )
            text = re.sub(r"[^-!$&(),./%0-9:;?a-z€'\"]+", " ", text)

        elif language == "es":
            text = re.sub(r"[^-!$&(),./%0-9:;?ÁÉÍÓÚÑÜáéíóúñü¿¡a-z€'\"]+", " ", text)

        elif language == "fr":
            text = re.sub(r"[^-!$&(),./%0-9:;?!çàâæéèêëîïôöûüù'€\"*]+", " ", text)

        elif language == "de":
            text = re.sub(r"[^-!$&(),./%0-9:;?!äöüßœáéíóúñüa-z'€\"*]+", " ", text)

        # Collapses repeated punctuation.
        text = re.sub(r"\.{2,}", ".", text)

        # Fix ordinal numbers (e.g., 1st, 2nd)
        text = re.sub(r"(\d)th", r"\1 th", text, flags=re.I)
        text = re.sub(r"(\d)st", r"\1 st", text, flags=re.I)
        text = re.sub(r"(\d)rd", r"\1 rd", text, flags=re.I)
        text = re.sub(r"(\d)nd", r"\1 nd", text, flags=re.I)

        # Separate punctuation with spaces
        punctuations = "-!$&(),./%:;?!çàâæéèêëîïôöûüù'€\"*"
        for character in punctuations:
            text = text.replace(character, " " + character + " ")

        # Splits text into list of words as strings.
        text_words = text.split(" ")

        # If no. of words in current text is more than maximum limit, then text is ignored.
        if len(text_words) > self.n_max_words_per_text:
            return ""

        # Iterates across words in text.
        filtered_words = list()
        for word in text_words:
            # If word is not empty, then it is appended to list.
            if word != "":
                filtered_words.append(word)

                # Unique word count is updated for current word.
                if update_word_count:
                    self.unique_word_count[language][word] = 1 + self.unique_word_count[
                        language
                    ].get(word, 0)

        # Converts of list of filtered words into a single string.
        filtered_text = " ".join(filtered_words)
        return filtered_text

    def identify_rare_words(self, language: str) -> None:
        """Identifies rare words for the language in the dataset.

        Identifies rare words for the language in the dataset.

        Args:
            language: A string for the name of the language the dataset belongs to.

        Returns:
            None.
        """
        # Asserts type & values of the arguments.
        assert isinstance(language, str), "Variable language should be of type 'str'."

        # Iterates across unique words in the dataset based on language.
        start_time = time.time()
        for word in self.unique_word_count[language].keys():
            # If count of word is 1, word consists of only alphabets, and length of word is between 8 & 10,
            # then word is added to rare words list.
            if (
                self.unique_word_count[language][word] == 1
                and word.isalpha()
                and not word.isdigit()
                and len(word) > 7
                and len(word) < 11
            ):
                self.rare_words[language].add(word)

        print(
            "Finished identifying rare words for {} language in {} sec.".format(
                language, round(time.time() - start_time, 3)
            )
        )
        print(
            "No. of rare words for {} language in the dataset: {}".format(
                language, len(self.rare_words[language])
            )
        )
        print("")
