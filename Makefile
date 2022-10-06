#//////////////////////////////////////////////////////////////
#//   ____                                                   //
#//  | __ )  ___ _ __  ___ _   _ _ __   ___ _ __ _ __   ___  //
#//  |  _ \ / _ \ '_ \/ __| | | | '_ \ / _ \ '__| '_ \ / __| //
#//  | |_) |  __/ | | \__ \ |_| | |_) |  __/ |  | |_) | (__  //
#//  |____/ \___|_| |_|___/\__,_| .__/ \___|_|  | .__/ \___| //
#//                             |_|             |_|          //
#//////////////////////////////////////////////////////////////
#//                                                          //
#//  Furaffinity, 2022                                       //
#//  Created: 06, October, 2022                              //
#//  Modified: 06, October, 2022                             //
#//  file: -                                                 //
#//  -                                                       //
#//  Source:                                                 //
#//  OS: ALL                                                 //
#//  CPU: ALL                                                //
#//                                                          //
#//////////////////////////////////////////////////////////////

PYTHON := python

.PHONY: install
install:
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: format
format:
	isort --multi-line=3 .
	black .

.PHONY: lint
lint: 
	find . -name '*.py' -exec python -m pylint {} \;
	find . -name '*.py' -exec python -m flake8 --select=DUO {} \;

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
