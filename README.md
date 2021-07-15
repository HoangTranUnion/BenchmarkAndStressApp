# BenchmarkAndStressApp
A very simple DNS and DoH Benchmark and Stress Tester

# Requirements:
## To run the code
- Python 3.6+
- [win10toast](https://pypi.org/project/win10toast/)
- [dnspython](https://pypi.org/project/dnspython/) (you will also have to install dnspython[doh] - pip install dnspython[doh])
- [PyQt5](https://pypi.org/project/PyQt5/)
- [numpy](https://pypi.org/project/numpy/)
- [requests](https://pypi.org/project/requests/)
- datetime

## To convert the code into an app
- [PyInstaller](https://pypi.org/project/pyinstaller/)

To install, you can either use
```
pip install <package>
```
or 
```
python -m pip install <package>
```
in the command line

I have also made a script, which is [libraries_setup.py](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/libraries_setup.py) and you can run it, so that you will have the packages automatically, without having to type in the commands above.

# Running the code
Just run main.py, granted packages have been installed.

# Converting the code to app
Just run setup.py, granted PyInstaller has been installed. After the script finished running, go to folder named dist and you will be able to find an app named main.exe in there.
After that, just run the app. The app will not require any packages to be installed to be able to run; however, it is recommended that you keep the build folder and file main.spec intact.

## Minor notes
I am currently fixing the bug where the app's icon does not correctly appear when the app is exported. Other than that, everything should work flawlessly

# Using the app
