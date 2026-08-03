import pandas as pd

def check_excel():
    file_path = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website/Sunnyward_Products_Database.xlsx"
    xl = pd.ExcelFile(file_path)
    print(f"Sheet names in the original Excel file: {xl.sheet_names}")
    
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        print(f"\nColumns in {sheet}:")
        print(df.columns.tolist())

if __name__ == "__main__":
    check_excel()
