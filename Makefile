VERBOSITY=2
TEST_TARGET=`ls -F xassr/apps | grep / | sed -e "s/\// /g" | tr -d '\n'`
test:
	python manage.py test $(TEST_TARGET) -v$(VERBOSITY)
.PHONY: test
