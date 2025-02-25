import win32com.client as win32
from requestApi import coinGrab

labels = ['Coin', 'Buy Price', 'Percent Increase']


class excelWriter:

    def __init__(self) -> None:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        for wb in excel.Workbooks:
            if wb.Name == 'data.xlsx':
                self.eFile = wb

    def create_sheet(self) -> str:
        for sheet in self.eFile.Sheets:
            if sheet.Name == 'coins':
                return sheet

        sheet = self.eFile.Worksheets.Add()
        sheet.Name = 'coins'
        for i in range(0, 5):
            sheet.Cells(1, i+1).Value = labels[i]
        return sheet


