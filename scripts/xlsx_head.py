import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple


NS = {
    'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def load_shared_strings(z: zipfile.ZipFile) -> List[str]:
    try:
        data = z.read('xl/sharedStrings.xml')
    except KeyError:
        return []
    root = ET.fromstring(data)
    result = []
    for si in root.findall('.//main:si', NS):
        text = ''.join(t.text or '' for t in si.findall('.//main:t', NS))
        result.append(text)
    return result


def map_rid_to_target(z: zipfile.ZipFile) -> Dict[str, str]:
    data = z.read('xl/_rels/workbook.xml.rels')
    root = ET.fromstring(data)
    mapping = {}
    for rel in root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        r_id = rel.attrib['Id']
        target = rel.attrib['Target']
        mapping[r_id] = target
    return mapping


def sheet_index(z: zipfile.ZipFile) -> List[Tuple[str, str]]:
    data = z.read('xl/workbook.xml')
    root = ET.fromstring(data)
    rid_to_target = map_rid_to_target(z)
    sheets = []
    for sh in root.findall('.//main:sheets/main:sheet', NS):
        name = sh.attrib['name']
        rid = sh.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
        target = rid_to_target.get(rid, '')
        sheets.append((name, target))
    return sheets


def read_first_rows(z: zipfile.ZipFile, target: str, shared: List[str], n: int = 4) -> List[List[str]]:
    path = f"xl/{target}"
    data = z.read(path)
    root = ET.fromstring(data)
    rows = []
    for i, row in enumerate(root.findall('.//main:sheetData/main:row', NS)):
        vals = []
        for c in row.findall('main:c', NS):
            t = c.attrib.get('t')
            v = c.find('main:v', NS)
            if v is None:
                vals.append('')
                continue
            txt = v.text or ''
            if t == 's':
                try:
                    idx = int(txt)
                    vals.append(shared[idx])
                except Exception:
                    vals.append(txt)
            else:
                vals.append(txt)
        rows.append(vals)
        if i + 1 >= n:
            break
    return rows


def main(xlsx_path: str):
    p = Path(xlsx_path)
    if not p.exists():
        print('NOT_FOUND', xlsx_path)
        return
    with zipfile.ZipFile(p, 'r') as z:
        shared = load_shared_strings(z)
        sheets = sheet_index(z)
        print('SHEETS:', [name for name, _ in sheets])
        for name, target in sheets:
            try:
                head_rows = read_first_rows(z, target, shared, n=3)
            except KeyError:
                continue
            print('---', name)
            for r in head_rows:
                print('|', ' | '.join(r))


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python scripts/xlsx_head.py <file.xlsx>')
    else:
        main(sys.argv[1])

