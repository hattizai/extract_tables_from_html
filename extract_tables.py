from bs4 import BeautifulSoup
import pandas as pd
import os

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def html_table_to_markdown(table):
    rows = []
    headers = []

    # 提取表头
    for th in table.find_all('th'):
        headers.append(th.get_text(strip=True))

    # 如果没有表头，使用第一行作为表头
    if not headers:
        headers = [td.get_text(strip=True) for td in table.find('tr').find_all('td')]

    rows.append(headers)

    # 提取表格内容
    for tr in table.find_all('tr')[1:]:
        row = []
        for td in tr.find_all('td'):
            cell_content = td.get_text(strip=True)
            link = td.find('a')
            if link and link.has_attr('href'):
                cell_content = f"[{cell_content}]({link['href']})"
            row.append(cell_content)
        rows.append(row)

    df = pd.DataFrame(rows[1:], columns=rows[0])
    markdown_table = df.to_markdown(index=False)
    return markdown_table

def extract_tables_to_markdown(html_content, output_file):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    
    if not tables:
        print("未在 HTML 文件中找到表格。")
        return
    
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for i, table in enumerate(tables):
            markdown_table = html_table_to_markdown(table)
            md_file.write(f"## 表格 {i+1}\n\n")
            md_file.write(markdown_table)
            md_file.write("\n\n")
    
    print(f"表格已成功提取并保存到 {output_file}")

def main():
    current_dir = os.getcwd()
    
    html_file = input("请输入 HTML 文件名（包括扩展名）：")
    html_path = os.path.join(current_dir, html_file)
    
    if not os.path.exists(html_path):
        print("文件不存在，请检查文件名是否正确。")
        return
    
    html_content = read_html_file(html_path)
    
    output_file = os.path.splitext(html_file)[0] + '_tables.md'
    output_path = os.path.join(current_dir, output_file)
    
    extract_tables_to_markdown(html_content, output_path)

if __name__ == "__main__":
    main()