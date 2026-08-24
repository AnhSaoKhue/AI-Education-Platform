import os
import zipfile
import shutil
import subprocess

def bundle_all():
    base_dir = os.getcwd()
    public_dir = os.path.join(base_dir, 'public')
    deploy_dir = os.path.join(base_dir, 'deploy')
    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(deploy_dir, exist_ok=True)

    # 1. Run generate_doc.py to produce latest Prompt_He_Thong_Anh_Sao_Khue.doc
    if os.path.exists('generate_doc.py'):
        try:
            subprocess.run(['python3', 'generate_doc.py'], check=True)
            print("Generated latest Prompt_He_Thong_Anh_Sao_Khue.doc")
        except Exception as e:
            print("Error running generate_doc.py:", e)

    # 2. Sync latest Code.gs and standalone html files
    if os.path.exists('Code.gs'):
        shutil.copy('Code.gs', os.path.join(public_dir, 'Code.gs'))
        shutil.copy('Code.gs', os.path.join(deploy_dir, 'Code.gs'))
    
    if os.path.exists('index.html'):
        shutil.copy('index.html', os.path.join(public_dir, 'index-single.html'))
        shutil.copy('index.html', os.path.join(public_dir, 'index_standalone.html'))
        shutil.copy('index.html', os.path.join(deploy_dir, 'index.html'))
    
    # remove old uppercase file if exists in public
    old_pub_index = os.path.join(public_dir, 'Index.html')
    if os.path.exists(old_pub_index):
        try:
            os.remove(old_pub_index)
        except Exception:
            pass

    if os.path.exists('AITeacherPlatform.html'):
        shutil.copy('AITeacherPlatform.html', os.path.join(public_dir, 'AITeacherPlatform.html'))

    # 3. Build Apps Script ZIP with lowercase index.html & Code.gs
    apps_script_zip_path = os.path.join(public_dir, 'apps_script_anh_sao_khue.zip')
    with zipfile.ZipFile(apps_script_zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        if os.path.exists('Code.gs'):
            z.write('Code.gs', 'Code.gs')
        if os.path.exists('AITeacherPlatform.html'):
            z.write('AITeacherPlatform.html', 'index.html')
            z.write('AITeacherPlatform.html', 'AITeacherPlatform.html')
        elif os.path.exists('index.html'):
            z.write('index.html', 'index.html')
        if os.path.exists('README.md'):
            z.write('README.md', 'README.md')
        if os.path.exists('README_HUONG_DAN_SU_DUNG.md'):
            z.write('README_HUONG_DAN_SU_DUNG.md', 'README_HUONG_DAN_SU_DUNG.md')
    print("Created:", apps_script_zip_path)

    # 4. Build Full Project Source ZIP (clean, ignoring internal build artifacts and zips)
    ignored_dirs = {'node_modules', '.git', 'dist', '.cache', '.upm', '.local', '.aistudio', '.vite', '.vscode', '__pycache__'}
    
    def add_directory_to_zip(zip_obj, folder_path, exclude_zips=True):
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith('.')]
            for f in files:
                if exclude_zips and (f.endswith('.zip') or f.endswith('.tar.gz') or f.endswith('.log')):
                    continue
                full_p = os.path.join(root, f)
                rel_p = os.path.relpath(full_p, folder_path)
                zip_obj.write(full_p, rel_p)

    # Main source zip
    main_zip_path = os.path.join(public_dir, 'anh-sao-khue-source-code.zip')
    with zipfile.ZipFile(main_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        add_directory_to_zip(zf, base_dir, exclude_zips=True)
    print("Created:", main_zip_path)

    # Duplicate to all standard alias names for compatibility
    aliases = [
        os.path.join(public_dir, 'project-source.zip'),
        os.path.join(public_dir, 'project-source-code.zip'),
        os.path.join(public_dir, 'AI_Teacher_Management_PRO_FINAL_SOURCE.zip'),
        os.path.join(public_dir, 'AI_Teacher_Management_PRO_ALL_IN_ONE_PACKAGE.zip'),
        os.path.join(public_dir, 'AI_Teacher_Management_PRO_AnhSaoKhue_Source.zip'),
        os.path.join(public_dir, 'ai_lesson_plans_anh_sao_khue.zip'),
        os.path.join(public_dir, 'Netlify_Deploy_Ready_Static.zip'),
        os.path.join(base_dir, 'anh-sao-khue-source-code.zip'),
        os.path.join(base_dir, 'project-source.zip'),
        os.path.join(base_dir, 'ai_lesson_plans_anh_sao_khue.zip'),
    ]
    for alias in aliases:
        shutil.copy(main_zip_path, alias)

    shutil.copy(apps_script_zip_path, os.path.join(base_dir, 'apps_script_anh_sao_khue.zip'))

    print("All ZIP packages and source distributions updated successfully!")

if __name__ == '__main__':
    bundle_all()

