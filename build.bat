pyinstaller -F -n VCT -w --hidden-import mpv --add-data "src2;src2" --icon="src2/resource/main_icon.png" "src2/main.py"

echo "or use: pyinstaller .\VCT.spec"