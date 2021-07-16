# BenchmarkAndStressApp
A very simple DNS and DoH Benchmark and Stress Tester.
Some references if you don't know what DNS and DNS over HTTPS (DoH) are:
- [Domain Name System (DNS)](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [DNS over HTTPS (DoH)](https://searchsecurity.techtarget.com/definition/DNS-over-HTTPS-DoH)

# Changes
## Version 1.1
- New [Test UI](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/NewTestUI.PNG)! Users would now have to ping the nameservers prior to testing, but it would take significantly less time to run a test than before (that is, if you are testing on a large number of nameservers).
- Warning dialog after testing will now be more informative - it will show what valid and blocked domain could not be resolved. For random ones, it will show what domains _could_ be resolved (partly because 99% of those domains could not be resolved anyway - that would not be informative).
- Fixes on Report UI where reports are still being automatically saved, although the user clicked on X button.
- Upon exiting Report UI, user will be asked if they want to save the report or not.
- Added app icon when exporting the code to .exe. Not sure how to make the window icon works without having to make a lot of steps, though.
- Relocated the Warning dialog, so now it won't be fully covered by the report UI anymore.

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
- Python 3.6+
- [PyInstaller](https://pypi.org/project/pyinstaller/)
- and hopefully no other packages are needed.

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

# Using the app
Upon running main.py or opening the app, the following window should appear.

![MainMenu](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/MainMenu.PNG)

From here, you should add nameservers and domains before doing any tests.

Please note that every modification and addition/removal is automatically saved, so you can close the window after finishing adding/modifying/removing.

## Adding nameservers
To add nameservers, simply click the Nameservers button

![NS](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/NameserverMainMenu.PNG)

Then click on Add NS

![AddNS](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/AddNS.PNG)

You can either type an IP or a DoH URL manually, or you can import file(s).
The files should be all .txt files, and each IP and DoH URL should be seperated line by line. Please refer to the [sample file](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/src/main/test/sample_data/sample_ns.txt) as an example.

As a note, if you want to add multiple nameservers, you can seperate each nameserver by a semicolon (;), as follows

![delim](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/delim.PNG)

Regardless of your choice, click "Add Nameservers" to add the desired nameservers.

After adding the nameservers, your screen should look something like this

![filled_ns](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/filled_ns.PNG)

## Adding domains
You can also add domains by clicking on the Domains button on the main menu. You should be greeted with this UI

![DMM](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/DomainMainMenu.PNG)

- Valid domains refer to public domains that usually any nameserver can resolve
- Random domains are randomly generated. For now, they are purely randomly generated, so there might be domains that can actually be resolved.
- Blocked domains refer to domains that can't be accessed normally by any publicly available nameservers.

Click on Add Domains

![do](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/domain_options.PNG)

Adding Valid and Blocked domains is similar to how you would add Nameservers, so please refer to the notes above.
For Random domains, however, for now, you can only specify how many domains to be generated.

I have provided [sample files](https://github.com/HoangTranUnion/BenchmarkAndStressApp/tree/master/src/main/test/sample_data) to import, so you can try as much as you want.

## Testing
To test the nameservers and domains, you can click on the Test button on the main menu.

![Test](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/testUI.PNG)

There are three choices:
- Benchmark for benchmarking all nameservers.
- Stress for stress testing all nameservers.
- Both for both benchmarking and stressing all nameservers.

For any given choice, you can specify the number of domains to use for testing. By default, if the field is left empty, fifty domains will be used for testing.
(Don't worry, if there is no domain in a type, say, Random, there will be no result in that regard.)

For Stress and Both choices, you need to specify the number of instances for each type of domain. By default, if the field is left empty, the number of instances will be 0.

The number of instances here can be used as a indicator for the number of concurrent users for a nameserver. 

As a recommendation, DO NOT set the number of instance to be too high if you are testing on significantly low-end devices - multithreading will consume a significant chunk of your CPU usage. To see the app running, you can just set around 10-100 instances.

Clicking on any choice will spawn a smug little notification.

![smug_start](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/start_test.PNG)

This will let you know that the test is running.
Similarly, when the test ended, another smug notification appears.

![smug_end](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/finish_test.PNG)

After everything, a result screen will appear. If there's any nameserver that cannot be pinged, a warning will appear with all the nameservers that could not be pinged.

Result screen:

![result](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/results_ui.PNG)

Warning screen:

![warning_ns](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/warning_ns_notavail.PNG)

## Saving the results
While you are in the result screen, you can press on Save Report to save the report to a desired folder. The report will be an Excel file, which will look like this:

![result_xls](https://github.com/HoangTranUnion/BenchmarkAndStressApp/blob/master/README_resources/report_xls.PNG)

# Issues
If there is any issues, please open an issue so that I will be notified. Otherwise, if you can't open an issue, you can contact me via Discord, RemineTheCat#9866


