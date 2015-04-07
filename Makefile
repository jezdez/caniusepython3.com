.PHONY: dev vm kill provision

dev:
	foreman start

vm:
	vagrant up --provider=virtualbox

kill:
	vagrant destroy -f

provision:
	vagrant provision
