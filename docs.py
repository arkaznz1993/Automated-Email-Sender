def read_paragraph_element(element: object):
    """Returns the text in the given ParagraphElement.

    Args:
        element: a ParagraphElement from a Google Doc.

    Returns:
        The text from a paragraph element
    """

    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_structural_elements(elements: list):
    """Recurses through a list of Structural Elements to read a document's text where text may be
    in nested elements.

    Args:
        elements: A list of Structural Elements.

    Returns:
        The entire document's text
    """

    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def get_doc_text(service: object, doc_id: str):
    """Accesses the Google Doc file and
    calls the read_structural_elements(doc_content) method

    Args:
        service: Google Docs service object
        doc_id: The id of the doc file

    Returns:
        The entire text from the Google Doc file
    """
    doc = service.documents().get(documentId=doc_id).execute()
    doc_content = doc.get('body').get('content')
    return read_structural_elements(doc_content)
