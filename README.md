# Docker Prusaslicer

Monitors a folder for .stl files and uses Prusa Slicer to create .gcode files to send to the printer.

This is a docker image on Ubuntu with Python and Prusa Slicer, and uses `watchdog` to monitor the directory.

## Usage
1. The container exposes two mount points `/configs/` and `/prints/`. Use `/configs` to place `.ini` files exported from Prusa Slicer GUI. The container will monitor `/prints` as the folder for inputs (and generating .gcode files from the .stls)
2. In the `/prints` folder create a subfolder with the `.stl` files you want to slice (ex: `/prints/project1/`)
3. To get the slicer to merge all the `.stl` files and create a `.gcode`: create a empty file with the name of the config you want to use (from the `/configs/` folder) and ending in `/slice` (ex: `touch /prints/project1/pla-supports.slice`)
4. A new `.gcode` file is created based on the config specified and can be sent to the printer

## License

![GitHub License](https://img.shields.io/github/license/vkhurana/docker-prusaslicer)  

## Build Status

[Code and Pipline is on GitHub](https://github.com/vkhurana/docker-prusaslicer):  
![GitHub Last Commit](https://img.shields.io/github/last-commit/vkhurana/docker-prusaslicer?logo=github)  
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vkhurana/docker-prusaslicer/.github/workflows/publish-docker-image.yml?logo=github)
## Container Images

Docker container images are published on [Docker Hub](https://hub.docker.com/r/vkhurana/docker-prusaslicer).  
Images are tagged using `latest`

![Docker Pulls](https://img.shields.io/docker/pulls/vkhurana/docker-prusaslicer?logo=docker)  
![Docker Image Version](https://img.shields.io/docker/v/vkhurana/docker-prusaslicer/latest?logo=docker)

## Docker Commands
Sample usage with ephemeral container:  
Interactive:  
`docker run --name="docker-slicer-inst" -v /home/vivek/code/tmp/slicer-tst/configs/:/configs -v /home/vivek/code/tmp/slicer-tst/prints/:/prints -it --rm docker-slicer`  

Detached:  
`docker run --name="docker-slicer-inst" -v /home/vivek/code/tmp/slicer-tst/configs/:/configs -v /home/vivek/code/tmp/slicer-tst/prints/:/prints -d --rm docker-slicer`  

## Docker Build
`docker build -t docker-slicer .`

## Background Info

This is a stateless container.

## Notes

- Runs on `Python 3`
- Pulls `Pusa Slicer` from Github and `OpenScad` from APT
