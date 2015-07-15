all:
	./SimpleServer.py

test:
	./kidneyexchange.py

clean:
	-rm gurobi.log *.pyc *.lp
