# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(
                   script="main.py", 
                   icon="bases/icone.ico",
                    target_name="Sonic da DeepWeb.exe"
                   ) ]
cx_Freeze.setup(
    name = "Sonic da DeepWeb",
    options={
        "build_exe":{
            "packages":["pygame", "pytmx", "pyttsx3"],
            "include_files":["bases","recursos"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
