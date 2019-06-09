.PHONY: build download-static copy-static preprocess build-docset install clean

tfjs_version = 1.1.2

build: download-static preprocess build-docset xml

download-static: copy-static
	@wget -nc -np --compression=gzip --domains=js.tensorflow.org -e robots=off --adjust-extension -r 'https://js.tensorflow.org/api/latest/' && wget https://js.tensorflow.org/css/api.css -O js.tensorflow.org/api.css && wget https://js.tensorflow.org/css/layout.css -O js.tensorflow.org/layout.css

copy-static:
	@cp dashing.json icon*.png js.tensorflow.org/.

preprocess preprocess:
	@export TFJS_VERSION="${tfjs_version}" && ./preprocess.sh js.tensorflow.org

build-docset:
	@cd js.tensorflow.org && dashing build && cd ../

install:
	open js.tensorflow.org/TensorFlow.js.docset

tarball:
	tar -czvf docset-tfjs-v${tfjs_version}.tar.gz js.tensorflow.org/TensorFlow.js.docset

xml:
	@echo '<entry><version>${tfjs_version}</version><url>https://github.com/mnmly/dash-docset-tfjs/releases/download/${tfjs_version}/docset-tfjs-v${tfjs_version}.tar.gz</url></entry>' > TensorFlow-js.xml

clean:
	rm -rf *.css js.tensorflow.org *.tar.gz
