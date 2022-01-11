import constants
from gmail import send_mail
from spreadsheets import Sheet
from docs import get_doc_text
from google_services import google_service


sheet_service = google_service(constants.SHEETS)
doc_service = google_service(constants.DOCS)
gmail_service = google_service(constants.GMAIL)


email_body = get_doc_text(doc_service, constants.HIRING_DOC_ID)
sheet = Sheet(sheet_service, constants.HIRING_SPREADSHEET_ID)

list_of_candidates = sheet.get_values(constants.HIRING_SPREADSHEET_RANGE)

send_mail(list_of_candidates, email_body, gmail_service)
