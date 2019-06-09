.PHONY: build download-static copy-static preprocess build-docset install clean

tfjs_version = 1.1.2

build: download-static preprocess build-docset

download-static:
	@wget -nc -np --compression=gzip --domains=js.tensorflow.org -e robots=off --adjust-extension -r 'https://js.tensorflow.org/api/latest/' && wget https://js.tensorflow.org/css/api.css -O js.tensorflow.org/api.css && wget https://js.tensorflow.org/css/layout.css -O js.tensorflow.org/layout.css

copy-static: download-static
	@cp dashing.json icon*.png js.tensorflow.org/.

preprocess: copy-static
	./preprocess.sh js.tensorflow.org

build-docset: preprocess
	@cd js.tensorflow.org && dashing build && cd ../

install:
	open js.tensorflow.org/TensorFlow.js.docset

tarball:
	tar -czvf docset-tfjs-v${tfjs_version}.tar.gz js.tensorflow.org/TensorFlow.js.docset
	
clean:
	rm -rf *.css js.tensorflow.org *.tar.gz
