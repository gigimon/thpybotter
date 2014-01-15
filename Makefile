clean:
	@echo Remove all '.pyc' files...
	@find . -name "*.pyc" -exec rm -rf {} \;
	@echo Clean complete!!!
