import os, glob

def migrate_to_offline():
    req_path = 'backend/requirements.txt'
    if os.path.exists(req_path):
        content = open(req_path, 'r', encoding='utf-8').read()
        open(req_path, 'w', encoding='utf-8').write(content.replace('zep-cloud==3.13.0', 'zep-python'))
        
    pyproj_path = 'backend/pyproject.toml'
    if os.path.exists(pyproj_path):
        content = open(pyproj_path, 'r', encoding='utf-8').read()
        open(pyproj_path, 'w', encoding='utf-8').write(content.replace('"zep-cloud==3.13.0"', '"zep-python"'))

    for py_file in glob.glob('backend/app/**/*.py', recursive=True):
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'zep_cloud' in content:
            content = content.replace('from zep_cloud.client import Zep', 'from zep_python import ZepClient as Zep')
            content = content.replace('import zep_cloud', 'import zep_python')
            
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
if __name__ == '__main__':
    migrate_to_offline()
    print("Міграцію завершено! Тепер виконайте: cd backend && uv sync")