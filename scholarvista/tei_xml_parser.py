import logging
import xml.etree.ElementTree as ET
from utils import get_links_from_text

"""
This file contains the TeiXmlParser class, which is used to parse TEI XML files.

The TeiXmlParser class provides methods to extract information from TEI XML files, such as the title, abstract, body text,
figures count, and links.

Example usage:
    parser = TeiXmlParser('path/to/xml/file.xml')
    title = parser.get_title()
    abstract = parser.get_abstract()
    body = parser.get_body()
    figures_count = parser.get_figures_count()
    links = parser.get_links()

"""

logging.basicConfig(filename='logs/error.log', level=logging.ERROR)


class TeiXmlParser:
    def __init__(self, file_path: str) -> None:
        """
        Initializes the TeiXmlParser object with the given file path.

        Args:
            file_path (str): The path to the TEI XML file.

        Raises:
            FileNotFoundError: If the file is not found.
            ET.ParseError: If there is an error parsing the XML file.
        """
        try:
            self.file_path = file_path
            self.namespace = 'http://www.tei-c.org/ns/1.0'
            self.root = ET.parse(self.file_path).getroot()
            self.body = self.__find_element_by_tag('body')
        except FileNotFoundError as e:
            logging.error(f"File not found: {file_path}")
            raise e
        except ET.ParseError as e:
            logging.error(f"Error parsing XML file: {file_path}")
            raise e

    def get_title(self) -> str:
        """
        Returns the text of the title of the document.

        Returns:
            str: The title of the document.
        """
        return self.__find_element_by_tag('title').text

    def get_abstract(self) -> str:
        """
        Returns the text of the abstract of the document.

        Returns:
            str: The abstract of the document.
        """
        return self.__find_element_by_tag('abstract')[0][0].text

    def get_body(self) -> str:
        """
        Returns the text of the body of the document.

        Returns:
            str: The body text of the document.

        Raises:
            AttributeError: If the XML structure is invalid and the body element is missing.
        """
        try:
            body_text = ''
            for paragraph in self.body.iter(self.__wrap_tag_with_namespace('p')):
                if paragraph.text is not None:
                    body_text += (paragraph.text + ' ')
            return body_text
        except AttributeError as e:
            logging.error("Invalid XML structure: missing body element")
            raise e

    def get_figures_count(self) -> int:
        """
        Returns the number of figures in the document.

        Returns:
            int: The number of figures in the document.

        Raises:
            AttributeError: If the XML structure is invalid and the body element is missing.
        """
        try:
            return len(list(self.body.iter(self.__wrap_tag_with_namespace('figure'))))
        except AttributeError as e:
            logging.error("Invalid XML structure: missing body element")
            raise e

    def get_links(self) -> list[str]:
        """
        Returns a list of links found in the document.

        Returns:
            list[str]: A list of links found in the document.

        Raises:
            Exception: If an error occurs while extracting links.
        """
        try:
            links = []
            for elem in self.root.iter():
                if elem.text is None:
                    continue
                links.extend(get_links_from_text(elem.text))
            return links
        except Exception as e:
            logging.error("Error occurred while extracting links")
            raise e

    def __find_element_by_tag(self, tag: str) -> ET.Element:
        """
        Returns the first element with the given tag in the document.

        Args:
            tag (str): The tag name of the element to find.

        Returns:
            ET.Element: The first element with the given tag in the document.
        """
        for elem in self.root.iter(self.__wrap_tag_with_namespace(tag)):
            return elem

    def __wrap_tag_with_namespace(self, tag: str) -> str:
        """
        Wraps the given tag name with the XML namespace.

        Args:
            tag (str): The tag name to wrap.

        Returns:
            str: The wrapped tag name with the XML namespace.
        """
        return f"{{{self.namespace}}}{tag}"
        """
        Wraps the given tag with the TEI namespace.
        """
        return '{' + self.namespace + '}' + tag
