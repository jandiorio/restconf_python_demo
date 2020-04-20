.PHONY: netdev

dev:
		docker run --name yang-explorer -p 8088:8088 -d dmfigol/yang-explorer
		docker container run -it -v ~/development:/development wwt01/alpine-network-dev
