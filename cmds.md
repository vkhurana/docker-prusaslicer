interactive:  
`docker run --name="docker-slicer-inst" -v /home/vivek/code/tmp/slicer-tst/configs/:/configs -v /home/vivek/code/tmp/slicer-tst/prints/:/prints -it --rm docker-slicer`  

detached:  
`docker run --name="docker-slicer-inst" -v /home/vivek/code/tmp/slicer-tst/configs/:/configs -v /home/vivek/code/tmp/slicer-tst/prints/:/prints -d --rm docker-slicer`  

in container:  
`/slic3r/slic3r-dist/prusa-slicer`  

build:  
`docker build -t docker-slicer .`