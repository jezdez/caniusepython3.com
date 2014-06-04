.PHONY: deploy-prod deploy-dev install clean

deploy-prod:
	ansible-playbook caniusepython3.yml -i inventory/prod.ini --ask-vault-pass

deploy-dev:
	ansible-playbook caniusepython3.yml -i inventory/dev.ini

install:
	ansible-galaxy install -r roles.txt -p roles --force

clean:
	rm -rf roles/Ansibles.*
	rm -rf roles/Stouts.*
