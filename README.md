My machine learning project, recognizing music genres.
In order to run this project correctly, download it and follow these steps:

- Install Anaconda.

If on windows:
- Open Anaconda Prompt from the windows search bar.
- Navigate to the root of this project. (using driver letter in order to switch drivers, and cd {path} in order to navigate to path in this drive). [EXAMPLE](https://riptutorial.com/cmd/example/8646/navigating-in-cmd)
- Run
```
conda env create -f envs/win.yml -n tal
conda activate tal
python init_gui.py
```

If on MacOSX:
- Open terminal.
- Navigate to the root of this project. (using cd {path} in order to navigate to path). [EXAMPLE](https://appletoolbox.com/navigate-folders-using-the-mac-terminal/)
- Run
```
conda env create -f envs/osx.yml -n tal
conda activate tal
python init_gui.py
```

* Note, the MacOSX version has only been tested on the new M1 chip, that is based on the arm64 architecture. It is NOT garunteed to work with other architectures in MacOS, as they probably have different packages.