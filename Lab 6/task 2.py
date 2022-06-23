import httplib2
from googleapiclient.discovery import build
from datetime import date
from pathlib import Path
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF
import sys

from tkinter import *
from tkinter.ttk import Combobox
import os
from oauth2client.service_account import ServiceAccountCredentials


def get_service_sacc():
    creds_json = os.path.dirname(__file__) + "/credentials.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


print(sys.path)

service = get_service_sacc()
sheet = service.spreadsheets()

sheet_id = "18q0EJw_-bNDGfeRsB5Q7EKqre3TsQcyVW1WzhCTjb5w"

resp = sheet.values().batchGet(spreadsheetId=sheet_id, ranges="name1!B4:B5").execute()
values = resp['valueRanges'][0]['values']
m, v = int(values[0][0]), int(values[1][0])
result = (m * v ** 2) / 2

cell_update = sheet.values().update(
    spreadsheetId=sheet_id,
    range="name1!B3",
    valueInputOption="RAW",
    body={'values': [[result]]}).execute()

print(m, v)
print(result)

pdf = Document()

page = Page()
pdf.append_page(page)

layout = SingleColumnLayout(page)

layout.add(Paragraph("Hello World!"))

pdf_name = "1к123иewнетичrtyеская энytrергия"


def clicked():
    pdf_name = txt.get()
    today = date.today()
    path = (f"{today} - {pdf_name}.pdf")

    with open(Path(path), "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
    url = 'https://docs.google.com/spreadsheets/export?format=pdf&id=' + sheet_id
    print(url)

#########################
Iwindow = Tk()
Iwindow.geometry('400x400')
Iwindow.title("Choose variables")
txt = Entry(Iwindow, width=20)
txt.grid(column=1, row=1)
txt2 = Entry(Iwindow, width=20)
txt2.grid(column=1, row=2)
txt3 = Entry(Iwindow, width=20)
txt3.grid(column=1, row=3)
btn = Button(Iwindow, text="Don't touch!", command=clicked)
btn.grid(column=2, row=5)
Iwindow.mainloop()