from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import argparse

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def html_table_to_dataframe(table, type_value):
    rows = []
    headers = []

    # 提取表头
    for th in table.find_all('th'):
        headers.append(th.get_text(strip=True))

    # 如果没有表头，使用第一行作为表头
    if not headers:
        headers = [td.get_text(strip=True) for td in table.find('tr').find_all('td')]

    # 提取表格内容
    for tr in table.find_all('tr')[1:]:
        row = []
        for td in tr.find_all('td'):
            cell_content = td.get_text(strip=True)
            link = td.find('a')
            if link and link.has_attr('href'):
                row.append(cell_content)
                # 在 URL 前面拼接 https://scan.merlinchain.io
                full_url = f"https://scan.merlinchain.io{link['href']}"
                row.append(full_url)
            else:
                row.append(cell_content)
                row.append('')
        row.append(type_value)  # 添加 type 值
        rows.append(row)

    # 为包含 URL 的列创建新的列名
    new_headers = []
    for header in headers:
        new_headers.append(header)
        new_headers.append(f"{header} URL")
    new_headers.append('type')

    df = pd.DataFrame(rows, columns=new_headers)
    
    # 删除空的 URL 列
    df = df.loc[:, (df != '').any(axis=0)]
    
    return df
    
def extract_tables_to_excel(html_content, output_file, type_value):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    
    if not tables:
        print("未在 HTML 文件中找到表格。")
        return
    
    with pd.ExcelWriter(output_file) as writer:
        for i, table in enumerate(tables):
            df = html_table_to_dataframe(table, type_value)
            sheet_name = f'Table_{i+1}'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"表格已成功提取并保存到 {output_file}")

def main():
    parser = argparse.ArgumentParser(description='从HTML文件提取表格到Excel，并添加type列')
    parser.add_argument('html_path', help='HTML文件的路径')
    parser.add_argument('type_value', help='type列的值')
    args = parser.parse_args()

    if not os.path.exists(args.html_path):
        print("文件不存在，请检查文件路径是否正确。")
        return
    
    html_content = read_html_file(args.html_path)
    
    output_file = os.path.splitext(args.html_path)[0] + '_tables.xlsx'
    
    extract_tables_to_excel(html_content, output_file, args.type_value)

if __name__ == "__main__":
    main()