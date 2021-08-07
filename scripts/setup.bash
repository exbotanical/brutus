#!/usr/bin/env bash

# pipenv install

cat > .git/hooks/pre-commit <<END
#!/usr/bin/env bash

pipenv run lint
pipenv run test
END

chmod u+x .git/hooks/pre-commit
